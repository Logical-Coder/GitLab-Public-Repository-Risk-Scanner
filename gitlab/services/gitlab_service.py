import requests


class GitLabService:

    BASE_URL = "https://gitlab.com/api/v4"

    def get_projects(
                self,
                target_type,
                target_name
            ):

        if target_type == "user":
            return self.get_user_projects(
                target_name
            )

        elif target_type == "group":
            return self.get_group_projects(
                target_name
            )

        elif target_type == "repository":

            project = self.get_project_by_path(
                target_name
            )

            return [
                {
                    "id": project["id"],
                    "name": project["name"],
                    "web_url": project["web_url"]
                }
            ]

        raise ValueError(
            f"Unsupported target type: {target_type}"
        )

    def get_user_projects(self, username):

        url = (
            f"{self.BASE_URL}/users"
            f"?username={username}"
        )

        response = requests.get(url, timeout=30)
        

        print("User API Status:", response.status_code)
        print("User API Response:", response.text[:500])

        response.raise_for_status()

        users = response.json()

        if not users:
            return []

        user_id = users[0]["id"]

        projects_url = (
            f"{self.BASE_URL}/users/"
            f"{user_id}/projects"
        )

        response = requests.get(
            projects_url,
            timeout=30
        )

        print(
            "Projects API Status:",
            response.status_code
        )

        response.raise_for_status()

        projects = response.json()

        return [
            {
                "id": project["id"],
                "name": project["name"],
                "web_url": project["web_url"]
            }
            for project in projects
        ]

    def get_group_projects(self, group_name):

        url = (
            f"{self.BASE_URL}/groups"
            f"?search={group_name}"
        )

        response = requests.get(url, timeout=30)

        print(
            "Group API Status:",
            response.status_code
        )

        response.raise_for_status()

        groups = response.json()

        if not groups:
            return []

        group_id = groups[0]["id"]

        projects_url = (
            f"{self.BASE_URL}/groups/"
            f"{group_id}/projects"
        )

        response = requests.get(
            projects_url,
            timeout=30
        )

        response.raise_for_status()

        projects = response.json()

        return [
            {
                "id": project["id"],
                "name": project["name"],
                "web_url": project["web_url"]
            }
            for project in projects
        ]

    def get_repository_tree(self, project_id):

        url = (
            f"{self.BASE_URL}/projects/"
            f"{project_id}/repository/tree"
        )

        print("Repository Tree URL:", url)

        response = requests.get(
            url,
            params={
                "recursive": True,
                "per_page": 100
            },
            timeout=30
        )

        print("Status:", response.status_code)
        print("Response:", response.text[:500])

        response.raise_for_status()

        return response.json()
    def get_file_content(
        self,
        project_id,
        file_path,
        branch="main"
    ):

        encoded_path = requests.utils.quote(
            file_path,
            safe=""
        )

        url = (
            f"{self.BASE_URL}/projects/"
            f"{project_id}/repository/files/"
            f"{encoded_path}/raw"
        )

        response = requests.get(
            url,
            params={"ref": branch},
            timeout=30
        )

        if response.status_code != 200:
            return ""

        return response.text
    def get_project_by_path(self, project_path):

        encoded_path = requests.utils.quote(
            project_path,
            safe=""
        )

        url = (
            f"{self.BASE_URL}/projects/"
            f"{encoded_path}"
        )

        response = requests.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        return response.json()