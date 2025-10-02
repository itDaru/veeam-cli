
import pytest
import requests
from src.veeam_cli.client import VeeamApiClient

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("VEEAM_HOST", "testhost")
    monkeypatch.setenv("VEEAM_USER", "testuser")
    monkeypatch.setenv("VEEAM_PASSWORD", "testpassword")

def test_authenticate_success(requests_mock, mock_env):
    """Test successful authentication."""
    requests_mock.post(
        "https://testhost:9419/api/oauth2/token",
        json={"access_token": "test_access_token", "refresh_token": "test_refresh_token"},
    )
    client = VeeamApiClient()
    assert client.access_token == "test_access_token"
    assert client.refresh_token == "test_refresh_token"

def test_authenticate_failure(requests_mock, mock_env):
    """Test authentication failure."""
    requests_mock.post(
        "https://testhost:9419/api/oauth2/token",
        status_code=401,
    )
    with pytest.raises(requests.exceptions.HTTPError):
        VeeamApiClient()

def test_refresh_token(requests_mock, mock_env):
    """Test token refresh."""
    requests_mock.post(
        "https://testhost:9419/api/oauth2/token",
        [
            {
                "json": {
                    "access_token": "initial_access_token",
                    "refresh_token": "initial_refresh_token",
                }
            },
            {
                "json": {
                    "access_token": "new_access_token",
                    "refresh_token": "new_refresh_token",
                }
            },
        ],
    )
    client = VeeamApiClient()
    assert client.access_token == "initial_access_token"

    # Trigger a refresh
    requests_mock.get("https://testhost:9419/api/v1/jobs", [
        {"status_code": 401},
        {"json": {}},
    ])
    client.get_backup_jobs()

    assert client.access_token == "new_access_token"

def test_get_backup_jobs(requests_mock, mock_env):
    """Test get_backup_jobs method."""
    requests_mock.post(
        "https://testhost:9419/api/oauth2/token",
        json={"access_token": "test_access_token", "refresh_token": "test_refresh_token"},
    )
    requests_mock.get(
        "https://testhost:9419/api/v1/jobs",
        json={"data": [{"id": "job1", "name": "Test Job"}]},
    )
    client = VeeamApiClient()
    jobs = client.get_backup_jobs()
    assert jobs["data"][0]["name"] == "Test Job"
