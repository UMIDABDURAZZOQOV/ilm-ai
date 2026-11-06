# Local provisioning only. No provider calls, plan changes or service restart.
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$PrivateDirectory,
    [Parameter(Mandatory = $true)][string]$AudienceReviewReference,
    [Parameter(Mandatory = $true)][string]$TrialReviewReference,
    [ValidateRange(1,8)][int]$KeyCount = 1
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

if ([string]::IsNullOrWhiteSpace($AudienceReviewReference) -or
    [string]::IsNullOrWhiteSpace($TrialReviewReference) -or
    $AudienceReviewReference.Length -gt 500 -or $TrialReviewReference.Length -gt 500) {
    throw 'Real audience/model and NVIDIA trial review references are required.'
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
# This script never calls an API, purchases capacity or starts the server.
if ((Read-Host 'Type Internal NVIDIA Trial after reviewing its evaluation-only terms') -cne 'Internal NVIDIA Trial') {
    throw 'Internal evaluation was not confirmed. No credential saved.'
}
$keys = New-Object 'System.Collections.Generic.List[string]'
$config = $null
try {
    for ($number = 1; $number -le $KeyCount; $number++) {
        $secret = Read-Host "NVIDIA Build API key $number of $KeyCount (hidden)" -AsSecureString
        $pointer = [IntPtr]::Zero
        $token = $null
        try {
            $pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secret)
            $token = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
            if (-not $token.StartsWith('nvapi-') -or $token.Length -lt 8 -or
                $token.Length -gt 512 -or $token -match '\s' -or $keys.Contains($token)) {
                throw 'Unsupported or duplicate key. Use a new NVIDIA Build key; no file was saved.'
            }
            $keys.Add($token)
        } finally {
            if ($pointer -ne [IntPtr]::Zero) { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer) }
            $token = $null
            $secret.Dispose()
        }
    }
    $config = [ordered]@{
        provider = 'nvidia_trial'
        model = 'meta/muse-glimmer-30b'
        api_keys = @($keys)
        audience_review_reference = $AudienceReviewReference
        free_only = $true
        usage = 'internal_evaluation'
        trial_review_reference = $TrialReviewReference
    }
    $path = Join-Path $root 'nvidia-trial.json'
    $stream = [IO.File]::Open($path, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write)
    try {
        $writer = New-Object IO.StreamWriter($stream, (New-Object Text.UTF8Encoding($false)))
        try { $writer.Write(($config | ConvertTo-Json -Depth 4)) }
        finally { $writer.Dispose() }
    } finally { $stream.Dispose() }
    Write-Output "Private configuration saved: $path"
    Write-Output 'Internal Beta only. No live API call, production activation or server restart performed.'
} finally {
    $config = $null
    $keys.Clear()
}
