# https://gist.github.com/codingforentrepreneurs/ffb3fb23a2710361a9489e7e0ee73cb8

from typing import Dict, List, Optional

import requests
from django.conf import settings

NEON_API_KEY = getattr(settings, "NEON_API_KEY", None)
NEON_PROJECT_ID = getattr(settings, "NEON_PROJECT_ID", None)
NEON_API_BASE_URL = "https://console.neon.tech/api/v2"


class NeonBranchClient:
    def __init__(self, api_key: str = NEON_API_KEY, project_id: str = NEON_PROJECT_ID):
        self.api_key = api_key
        self.project_id = project_id
        self.base_url = NEON_API_BASE_URL
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def list_branches(self, names_only: bool = False) -> Dict:
        """List all branches in the project"""
        url = f"{self.base_url}/projects/{self.project_id}/branches"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        branches = response.json()["branches"]
        if names_only:
            return [branch["name"] for branch in branches]
        return branches

    def protect_branch(self, branch_id: str) -> Dict:
        """Protect a branch"""
        url = f"{self.base_url}/projects/{self.project_id}/branches/{branch_id}"
        payload = {"branch": {"protected": True}}
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            **self.headers,
        }
        try:
            response = requests.patch(url, headers=headers, json=payload)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            return {"error": str(http_err)}
        except Exception as err:
            return {"error": str(err)}
        return response.json()

    def set_as_primary(self, branch_id: str) -> Dict:
        """Set a branch as the primary branch"""
        url = f"{self.base_url}/projects/{self.project_id}/primary_branch"
        payload = {"branch_id": branch_id}
        response = requests.put(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def get_primary_branch(
        self, fields: List[str] = ["id", "name", "protected"]
    ) -> Dict:
        """Get the primary branch"""
        branches = self.list_branches()
        for branch in branches:
            if branch["primary"]:
                if len(fields) == 0:
                    return branch
                elif len(fields) == 1:
                    if fields[0] == "*":
                        return branch
                return {field: branch[field] for field in fields}
        return {}

    def create_branch(
        self,
        parent_id: Optional[str] = None,
        name: Optional[str] = None,
        with_compute: bool = True,
    ) -> Dict:
        """Create a new branch"""
        url = f"{self.base_url}/projects/{self.project_id}/branches"

        payload = {}
        if parent_id:
            payload["branch"] = {"parent_id": parent_id}
        if name:
            payload["branch"] = payload.get("branch", {})
            payload["branch"]["name"] = name
        if with_compute:
            payload["endpoints"] = [{"type": "read_write"}]

        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def get_branch_by_name(self, starts_with: str) -> Dict:
        """Get a branch by name"""
        branches = self.list_branches()
        for branch in branches:
            if branch["name"].startswith(starts_with):
                return branch
        return {}

    def delete_branch(self, branch_id: str) -> Dict:
        """Delete a specific branch"""
        url = f"{self.base_url}/projects/{self.project_id}/branches/{branch_id}"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_branch(self, branch_id: str) -> Dict:
        """Get details of a specific branch"""
        url = f"{self.base_url}/projects/{self.project_id}/branches/{branch_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()