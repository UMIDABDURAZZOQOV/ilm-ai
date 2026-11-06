"""Exercise the Windows provisioning helper with synthetic input only."""

import json
import os
from pathlib import Path
import subprocess

import pytest


pytestmark = pytest.mark.skipif(os.name != "nt", reason="Windows ACL provisioning")
SCRIPT = Path(__file__).resolve().parents[1] / "scripts/configure_cloudflare_free.ps1"


def run_helper(path, *, account="a" * 32, plan="Workers Free", review="review-1"):
    # Input values here are test data. Actual provisioning uses hidden Read-Host.
    wrapper = """
$ErrorActionPreference='Stop'
function Read-Host {
    param([string]$Prompt, [switch]$AsSecureString)
    if ($AsSecureString) {
        return ConvertTo-SecureString 'synthetic-test-token-only' -AsPlainText -Force
    }
    if ($Prompt.StartsWith('Cloudflare Account')) { return $env:TEST_CF_ACCOUNT }
    return $env:TEST_CF_PLAN
}
try {
    & $env:TEST_CF_SCRIPT -PrivateDirectory $env:TEST_CF_DIRECTORY `
      -AudienceReviewReference $env:TEST_CF_REVIEW -FreePlanReviewReference 'free-review-1'
} catch { Write-Output 'provisioning_refused'; exit 1 }
"""
    environment = dict(
        os.environ,
        TEST_CF_SCRIPT=str(SCRIPT),
        TEST_CF_DIRECTORY=str(path),
        TEST_CF_ACCOUNT=account,
        TEST_CF_PLAN=plan,
        TEST_CF_REVIEW=review,
    )
    return subprocess.run(
        [
            "powershell.exe",
            "-NoProfile",
            "-NonInteractive",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            wrapper,
        ],
        env=environment,
        capture_output=True,
        text=True,
        timeout=30,
    )


def test_private_free_config_without_network_or_secret_output(tmp_path):
    path = tmp_path / "private"
    result = run_helper(path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "synthetic-test-token-only" not in result.stdout + result.stderr
    config = path / "cloudflare-free.json"
    data = json.loads(config.read_text(encoding="utf-8"))
    assert data["free_only"] is True
    assert data["api_keys"] == ["synthetic-test-token-only"]
    from services.study_help_provider import load_provider
    from services.cloudflare_study_help import CloudflareEvidenceSelector

    assert isinstance(load_provider(config), CloudflareEvidenceSelector)
    # Verify the actual folder and inherited file ACL; not only source text.
    check = subprocess.run(
        [
            "powershell.exe",
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            "$sid=[Security.Principal.WindowsIdentity]::GetCurrent().User.Value; "
            "foreach($p in @($env:TEST_CF_DIRECTORY,(Join-Path $env:TEST_CF_DIRECTORY 'cloudflare-free.json'))) { "
            "$acl=Get-Acl -LiteralPath $p; "
            "foreach($ace in $acl.Access) { "
            "if($ace.IdentityReference.Translate([Security.Principal.SecurityIdentifier]).Value -ne $sid) {exit 2} } }; "
            "if(-not (Get-Acl -LiteralPath $env:TEST_CF_DIRECTORY).AreAccessRulesProtected) {exit 3}",
        ],
        env=dict(os.environ, TEST_CF_DIRECTORY=str(path)),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert check.returncode == 0, check.stdout + check.stderr


@pytest.mark.parametrize(
    "change", [{"account": "../invalid"}, {"plan": "Workers Paid"}, {"review": " "}]
)
def test_invalid_or_unreviewed_config_never_saves_a_token(tmp_path, change):
    path = tmp_path / "private"
    result = run_helper(path, **change)
    assert result.returncode != 0
    assert not (path / "cloudflare-free.json").exists()
    assert "synthetic-test-token-only" not in result.stdout + result.stderr


def test_existing_directory_is_never_modified(tmp_path):
    result = run_helper(tmp_path)
    assert result.returncode != 0
    assert list(tmp_path.iterdir()) == []


def test_git_directory_is_rejected(tmp_path):
    (tmp_path / ".git").mkdir()
    result = run_helper(tmp_path / "private")
    assert result.returncode != 0
    assert not (tmp_path / "private").exists()
