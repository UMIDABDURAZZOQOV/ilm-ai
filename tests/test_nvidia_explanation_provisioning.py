"""Windows ACL and fake-token provisioning, never a real credential or API."""

import json
import os
from pathlib import Path
import subprocess

import pytest

pytestmark = pytest.mark.skipif(os.name != 'nt', reason='Windows ACL helper')
SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/configure_nvidia_explanations.ps1'


def provision(path, usage='internal_evaluation', confirmation='Internal NVIDIA Text Evaluation', prefix='nvapi-'):
    wrapper = r'''
$ErrorActionPreference='Stop'
function Read-Host {
  param([string]$Prompt,[switch]$AsSecureString)
  if ($AsSecureString) { return ConvertTo-SecureString ($env:NV_TEST_PREFIX+('synthetic-only-'*3)) -AsPlainText -Force }
  return $env:NV_TEST_CONFIRM
}
try {
 & $env:NV_TEST_SCRIPT -PrivateDirectory $env:NV_TEST_DIR -Usage $env:NV_TEST_USAGE `
   -UsageReviewReference 'synthetic usage review' -AudienceReviewReference 'synthetic audience review' `
   -DataProcessingReviewReference 'synthetic privacy review' -FreePlanReviewReference 'synthetic free-plan review'
} catch { Write-Output 'provisioning_refused'; exit 1 }
'''
    return subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass','-Command',wrapper],
                          env=dict(os.environ,NV_TEST_SCRIPT=str(SCRIPT),NV_TEST_DIR=str(path),
                                   NV_TEST_USAGE=usage,NV_TEST_CONFIRM=confirmation,NV_TEST_PREFIX=prefix),
                          capture_output=True,text=True,timeout=30)


@pytest.mark.parametrize('usage,confirmation,field', [
    ('internal_evaluation','Internal NVIDIA Text Evaluation','trial_review_reference'),
    ('authorized_hosted_application','Authorized Hosted NVIDIA Text','hosted_use_review_reference'),
])
def test_private_new_directory_one_key_exact_reviewed_config(tmp_path,usage,confirmation,field):
    folder=tmp_path/'new-private'
    result=provision(folder,usage,confirmation)
    assert result.returncode==0,result.stdout
    data=json.loads((folder/'nvidia-explanations.json').read_text(encoding='utf-8'))
    assert data['usage']==usage and data['provider']=='nvidia_explanation'
    assert data['audience']=='adults_only' and data['free_only'] is True and field in data
    assert 'api_keys' not in data and data['api_key'] not in result.stdout+result.stderr
    check=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
        '$a=Get-Acl -LiteralPath $env:NV_TEST_DIR; if (-not $a.AreAccessRulesProtected) {exit 1}; '
        '$s=[Security.Principal.WindowsIdentity]::GetCurrent().User.Value; '
        'if (@($a.Access | Where-Object {$_.IdentityReference.Translate([Security.Principal.SecurityIdentifier]).Value -ne $s}).Count) {exit 2}'],
        env=dict(os.environ,NV_TEST_DIR=str(folder)),capture_output=True,text=True,timeout=30)
    assert check.returncode==0


@pytest.mark.parametrize('prefix,confirmation', [('AQ.','Internal NVIDIA Text Evaluation'),('nvapi-','wrong confirmation')])
def test_invalid_key_or_unconfirmed_usage_never_writes_private_file(tmp_path,prefix,confirmation):
    folder=tmp_path/'refused'
    result=provision(folder,prefix=prefix,confirmation=confirmation)
    assert result.returncode!=0 and not (folder/'nvidia-explanations.json').exists()
    assert 'synthetic-only' not in result.stdout+result.stderr


def test_existing_directory_is_unchanged(tmp_path):
    marker=tmp_path/'keep.txt'
    marker.write_text('untouched',encoding='utf-8')
    assert provision(tmp_path).returncode!=0
    assert marker.read_text(encoding='utf-8')=='untouched'
    assert not (tmp_path/'nvidia-explanations.json').exists()
