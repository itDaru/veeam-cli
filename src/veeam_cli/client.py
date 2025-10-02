
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class VeeamApiClient:
    def __init__(self, api_version="v1"):
        self.host = os.getenv("VEEAM_HOST")
        self.port = os.getenv("VEEAM_PORT", 9419)
        self.username = os.getenv("VEEAM_USER")
        self.password = os.getenv("VEEAM_PASSWORD")
        self.api_version = api_version
        self.base_url = f"https://{self.host}:{self.port}/api"
        self.access_token = None
        self.refresh_token = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with the Veeam Backup & Replication API."""
        token_url = f"{self.base_url}/oauth2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
        }
        response = requests.post(token_url, headers=headers, data=data, verify=False)
        response.raise_for_status()
        token_data = response.json()
        self.access_token = token_data["access_token"]
        self.refresh_token = token_data["refresh_token"]

    def _refresh_token(self):
        """Refresh the access token."""
        token_url = f"{self.base_url}/oauth2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }
        response = requests.post(token_url, headers=headers, data=data, verify=False)
        if response.status_code == 401:
            # Refresh token is invalid, re-authenticate
            self._authenticate()
        else:
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data["access_token"]
            self.refresh_token = token_data["refresh_token"]

    def _request(self, method, endpoint, **kwargs):
        """Make a request to the Veeam API."""
        url = f"{self.base_url}/{self.api_version}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Add default verify=False to kwargs if not present
        kwargs.setdefault('verify', False)

        response = requests.request(method, url, headers=headers, **kwargs)

        if response.status_code == 401:
            self._refresh_token()
            headers["Authorization"] = f"Bearer {self.access_token}"
            response = requests.request(method, url, headers=headers, **kwargs)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if 400 <= e.response.status_code < 500:
                print(f"Client error: {e.response.status_code} {e.response.reason} for URL {e.response.url}")
            elif 500 <= e.response.status_code < 600:
                print(f"Server error: {e.response.status_code} {e.response.reason} for URL {e.response.url}")
            raise

        return response

    def get_backup_jobs(self, limit=20, offset=0):
        """Get a list of backup jobs."""
        return self._request("GET", "jobs", params={"limit": limit, "offset": offset}).json()

    def get_repositories(self, limit=20, offset=0):
        """Get a list of backup repositories."""
        return self._request("GET", "backupRepositories", params={"limit": limit, "offset": offset}).json()

    def get_job_sessions(self, job_id, limit=20, offset=0):
        """Get a list of sessions for a specific job."""
        return self._request("GET", f"jobs/{job_id}/sessions", params={"limit": limit, "offset": offset}).json()

    def get_job_restore_points(self, job_id, limit=20, offset=0):
        """Get a list of restore points for a specific job."""
        return self._request(
            "GET", f"jobs/{job_id}/restorePoints", params={"limit": limit, "offset": offset}
        ).json()

    def get_tape_libraries(self, limit=20, offset=0):
        """Get a list of tape libraries."""
        return self._request("GET", "tape/libraries", params={"limit": limit, "offset": offset}).json()

    def get_tape_drives(self, limit=20, offset=0):
        """Get a list of tape drives."""
        return self._request("GET", "tape/drives", params={"limit": limit, "offset": offset}).json()
