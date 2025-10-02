
import pytest
from click.testing import CliRunner
from src.veeam_cli.cli import cli

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("VEEAM_HOST", "testhost")
    monkeypatch.setenv("VEEAM_USER", "testuser")
    monkeypatch.setenv("VEEAM_PASSWORD", "testpassword")

def test_jobs_list_empty(requests_mock, mock_env):
    """Test jobs list command with no jobs."""
    requests_mock.post(
        "https://testhost:9419/api/oauth2/token",
        json={"access_token": "test_access_token", "refresh_token": "test_refresh_token"},
    )
    requests_mock.get(
        "https://testhost:9419/api/v1/jobs",
        json={"data": []},
    )
    runner = CliRunner()
    result = runner.invoke(cli, ["jobs", "list"])
    assert result.exit_code == 0
    assert "Name" in result.output
    assert "Type" in result.output
    assert "Last Result" in result.output

def test_jobs_list_with_jobs(requests_mock, mock_env):
    """Test jobs list command with jobs."""
    requests_mock.post(
        "https://testhost:9419/api/oauth2/token",
        json={"access_token": "test_access_token", "refresh_token": "test_refresh_token"},
    )
    requests_mock.get(
        "https://testhost:9419/api/v1/jobs",
        json={
            "data": [
                {
                    "id": "job1",
                    "name": "Test Job 1",
                    "type": "Backup",
                    "lastResult": "Success",
                },
                {
                    "id": "job2",
                    "name": "Test Job 2",
                    "type": "Replica",
                    "lastResult": "Failed",
                },
            ]
        },
    )
    runner = CliRunner()
    result = runner.invoke(cli, ["jobs", "list"])
    assert result.exit_code == 0
    assert "Test Job 1" in result.output
    assert "Test Job 2" in result.output
