"""Provision fake NVIDIA keys in an owned Windows test folder only."""

import json
import os
from pathlib import Path
import subprocess

import pytest


pytestmark = pytest.mark.skipif(os.name != "nt", reason="Windows ACL helper")
SCRIPT = Path(__file__).resolve().parents[1] / "scripts/configure_nvidia_trial.ps1"


def provision(path, count=8, prefix="nvapi-", confirmation="Internal NVIDIA Trial"):
    wrapper = """
$ErrorActionPreference='Stop'
$global:testKeyNumber=0
function Read-Host {
  param([string]$Prompt,[switch]$AsSecureString)
  if ($AsSecureString) {
    $global:testKeyNumber++
    return ConvertTo-SecureString ($env:TEST_NV_PREFIX+'synthetic-only-'+$global:testKeyNumber) -AsPlainText -Force
  }
  return $env:TEST_NV_CONFIRM
}
try {
 & $env:TEST_NV_SCRIPT -PrivateDirectory $env:TEST_NV_DIR -KeyCount ([int]$env:TEST_NV_COUNT) `
   -AudienceReviewReference 'synthetic audience review' -TrialReviewReference 'synthetic internal-only review'
} catch { Write-Output 'provisioning_refused'; exit 1 }
"""
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
        env=dict(
            os.environ,
            TEST_NV_PREFIX=prefix,
            TEST_NV_SCRIPT=str(SCRIPT),
            TEST_NV_DIR=str(path),
            TEST_NV_COUNT=str(count),
            TEST_NV_CONFIRM=confirmation,
        ),
        capture_output=True,
        text=True,
        timeout=30,
    )


@pytest.mark.parametrize("count", [1, 8])
def test_one_or_eight_hidden_private_keys_without_live_activation(
    tmp_path, monkeypatch, count
):
    path = tmp_path / "private"
    result = provision(path, count)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "synthetic-only" not in result.stdout + result.stderr
    data = json.loads((path / "nvidia-trial.json").read_text(encoding="utf-8"))
    assert len(data["api_keys"]) == count and len(set(data["api_keys"])) == count
    assert data["free_only"] is True and data["usage"] == "internal_evaluation"
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("ILM_BETA_ENABLED", "true")
    from services.study_help_provider import load_provider
    from services.nvidia_study_help import NvidiaTrialEvidenceSelector

    assert isinstance(
        load_provider(path / "nvidia-trial.json"), NvidiaTrialEvidenceSelector
    )
    check = subprocess.run(
        [
            "powershell.exe",
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            "$sid=[Security.Principal.WindowsIdentity]::GetCurrent().User.Value; "
            'foreach($p in @($env:TEST_NV_DIR,(Join-Path $env:TEST_NV_DIR "nvidia-trial.json"))) {'
            "$a=Get-Acl -LiteralPath $p; foreach($ace in $a.Access) {"
            "if($ace.IdentityReference.Translate([Security.Principal.SecurityIdentifier]).Value -ne $sid) {exit 2} } }; "
            "if(-not (Get-Acl -LiteralPath $env:TEST_NV_DIR).AreAccessRulesProtected) {exit 3}",
        ],
        env=dict(os.environ, TEST_NV_DIR=str(path)),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert check.returncode == 0, check.stdout + check.stderr


@pytest.mark.parametrize(
    "change", [{"prefix": "AQ."}, {"confirmation": "Production"}, {"count": 9}]
)
def test_foreign_key_production_or_ninth_key_not_saved(tmp_path, change):
    path = tmp_path / "private"
    result = provision(path, **change)
    assert result.returncode != 0
    assert not (path / "nvidia-trial.json").exists()
    assert "synthetic-only" not in result.stdout + result.stderr
