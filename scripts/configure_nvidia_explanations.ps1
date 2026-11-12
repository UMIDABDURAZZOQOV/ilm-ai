# Private local provisioning only: no API, billing, deployment or DB action.
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$PrivateDirectory,
    [ValidateSet('internal_evaluation','authorized_hosted_application')]
    [string]$Usage='internal_evaluation',
    [Parameter(Mandatory=$true)][string]$UsageReviewReference,
    [Parameter(Mandatory=$true)][string]$AudienceReviewReference,
    [Parameter(Mandatory=$true)][string]$DataProcessingReviewReference,
    [Parameter(Mandatory=$true)][string]$FreePlanReviewReference
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
foreach ($reference in @($UsageReviewReference,$AudienceReviewReference,$DataProcessingReviewReference,$FreePlanReviewReference)) {
    if ([string]::IsNullOrWhiteSpace($reference) -or $reference.Length -gt 500) {
        throw 'Actual usage, audience, data-processing and free-plan review references are required.'
    }
}
$root=[IO.Path]::GetFullPath($PrivateDirectory)
if (Test-Path -LiteralPath $root) { throw 'Choose a NEW private directory outside Git.' }
$parent=[IO.DirectoryInfo][IO.Path]::GetDirectoryName($root)
if (-not $parent.Exists) { throw 'The parent directory must already exist.' }
for ($node=$parent; $null -ne $node; $node=$node.Parent) {
    if (($node.Attributes -band [IO.FileAttributes]::ReparsePoint) -or
        (Test-Path -LiteralPath (Join-Path $node.FullName '.git'))) {
        throw 'Private configuration cannot be inside Git or a reparse/symlink path.'
    }
}
$sid=[Security.Principal.WindowsIdentity]::GetCurrent().User
$acl=New-Object Security.AccessControl.DirectorySecurity
$acl.SetOwner($sid)
$acl.SetAccessRuleProtection($true,$false)
$rule=New-Object Security.AccessControl.FileSystemAccessRule(
    $sid,'FullControl','ContainerInherit,ObjectInherit','None','Allow'
)
$acl.AddAccessRule($rule)
$null=New-Item -ItemType Directory -Path $root
Set-Acl -LiteralPath $root -AclObject $acl
$verified=Get-Acl -LiteralPath $root
if (-not $verified.AreAccessRulesProtected -or
    $verified.GetOwner([Security.Principal.SecurityIdentifier]).Value -ne $sid.Value) {
    throw 'Private folder protection could not be verified. No token was requested.'
}
$confirmation=if ($Usage -eq 'internal_evaluation') { 'Internal NVIDIA Text Evaluation' } else { 'Authorized Hosted NVIDIA Text' }
if ((Read-Host "After reviewing the actual service terms, type $confirmation") -cne $confirmation) {
    throw 'Usage was not confirmed. No credential saved.'
}
$secret=$null
$pointer=[IntPtr]::Zero
$token=$null
$config=$null
try {
    $secret=Read-Host 'NVIDIA API key (hidden; one authorized key only)' -AsSecureString
    $pointer=[Runtime.InteropServices.Marshal]::SecureStringToBSTR($secret)
    $token=[Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
    if ($token -notmatch '^nvapi-[A-Za-z0-9_-]{20,500}$') {
        throw 'Unsupported key format. No file was saved.'
    }
    $config=[ordered]@{
        provider='nvidia_explanation'
        model='meta/muse-glimmer-30b'
        api_key=$token
        usage=$Usage
        audience='adults_only'
        free_only=$true
        audience_review_reference=$AudienceReviewReference
        data_processing_review_reference=$DataProcessingReviewReference
        free_plan_review_reference=$FreePlanReviewReference
    }
    if ($Usage -eq 'internal_evaluation') { $config['trial_review_reference']=$UsageReviewReference }
    else { $config['hosted_use_review_reference']=$UsageReviewReference }
    $path=Join-Path $root 'nvidia-explanations.json'
    $stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write)
    try {
        $writer=New-Object IO.StreamWriter($stream,(New-Object Text.UTF8Encoding($false)))
        try { $writer.Write(($config | ConvertTo-Json -Depth 4)) }
        finally { $writer.Dispose() }
    } finally { $stream.Dispose() }
    Write-Output "Private configuration saved: $path"
    Write-Output 'No live request, paid activation, deployment or server restart performed.'
} finally {
    if ($pointer -ne [IntPtr]::Zero) { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer) }
    if ($null -ne $secret) { $secret.Dispose() }
    $token=$null
    $config=$null
}
