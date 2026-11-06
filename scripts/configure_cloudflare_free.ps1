# Local provisioning only. No provider calls, plan changes or service restart.
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$PrivateDirectory,
    [Parameter(Mandatory = $true)][string]$AudienceReviewReference,
    [Parameter(Mandatory = $true)][string]$FreePlanReviewReference
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

if ([string]::IsNullOrWhiteSpace($AudienceReviewReference) -or
    [string]::IsNullOrWhiteSpace($FreePlanReviewReference) -or
    $AudienceReviewReference.Length -gt 500 -or $FreePlanReviewReference.Length -gt 500) {
    throw 'Real audience/model and Workers Free review references are required.'
}
$root = [IO.Path]::GetFullPath($PrivateDirectory)
# Refuse existing folders: never change permissions on unrelated user files.
if (Test-Path -LiteralPath $root) { throw 'Choose a NEW private directory outside Git.' }
$parent = [IO.DirectoryInfo][IO.Path]::GetDirectoryName($root)
if (-not $parent.Exists) { throw 'The parent directory must already exist.' }
for ($node = $parent; $null -ne $node; $node = $node.Parent) {
    if (($node.Attributes -band [IO.FileAttributes]::ReparsePoint) -or
        (Test-Path -LiteralPath (Join-Path $node.FullName '.git'))) {
        throw 'Private configuration cannot be inside Git or a reparse/symlink path.'
    }
}
$sid = [Security.Principal.WindowsIdentity]::GetCurrent().User
$acl = New-Object Security.AccessControl.DirectorySecurity
$acl.SetOwner($sid)
$acl.SetAccessRuleProtection($true, $false)
$rule = New-Object Security.AccessControl.FileSystemAccessRule(
    $sid, 'FullControl', 'ContainerInherit,ObjectInherit', 'None', 'Allow'
)
$acl.AddAccessRule($rule)
$null = New-Item -ItemType Directory -Path $root
# No credential exists until the folder's protected ACL has been applied.
Set-Acl -LiteralPath $root -AclObject $acl
$verified = Get-Acl -LiteralPath $root
if (-not $verified.AreAccessRulesProtected -or
    $verified.GetOwner([Security.Principal.SecurityIdentifier]).Value -ne $sid.Value) {
    throw 'Private folder protection could not be verified. No token was requested.'
}
$account = Read-Host 'Cloudflare Account ID (32 lowercase hex characters)'
if ($account -cnotmatch '^[a-f0-9]{32}$') { throw 'Invalid Account ID.' }
if ((Read-Host 'After verifying the dashboard plan, type Workers Free') -cne 'Workers Free') {
    throw 'Workers Free was not confirmed. No credential was saved.'
}
$secret = Read-Host 'Workers AI scoped API token (hidden; never paste it in chat)' -AsSecureString
$pointer = [IntPtr]::Zero
$token = $null
try {
    $pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secret)
    $token = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
    if ($token.Length -lt 8 -or $token.Length -gt 512 -or
        $token -match '\s' -or $token.StartsWith('AQ.') -or $token.StartsWith('AIza')) {
        throw 'Invalid provider token. Nothing was saved.'
    }
    $config = [ordered]@{
        provider = 'cloudflare'
        model = '@cf/meta/llama-3.3-70b-instruct-fp8-fast'
        api_keys = @($token)
        account_id = $account
        free_only = $true
        audience_review_reference = $AudienceReviewReference
        free_plan_review_reference = $FreePlanReviewReference
    }
    $path = Join-Path $root 'cloudflare-free.json'
    # CreateNew refuses replacement; the file inherits only this user's access.
    $stream = [IO.File]::Open($path, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write)
    try {
        $writer = New-Object IO.StreamWriter($stream, (New-Object Text.UTF8Encoding($false)))
        try { $writer.Write(($config | ConvertTo-Json -Depth 4)) }
        finally { $writer.Dispose() }
    } finally { $stream.Dispose() }
    Write-Output "Private configuration saved: $path"
    Write-Output 'Not connected yet. Validate locally, then use a controlled backend restart.'
} finally {
    if ($pointer -ne [IntPtr]::Zero) { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer) }
    $token = $null
    $config = $null
    $secret.Dispose()
}
