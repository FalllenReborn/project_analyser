import requests
import json
import time


class CommitRetriever:
    def __init__(self, org_name, token, base_url="https://api.github.com", per_page=100, timeout=1):
        self.org_name = org_name
        self.token = token
        self.base_url = base_url
        self.per_page = per_page
        self.timeout = timeout

        self.repos_url = f"{self.base_url}/orgs/{self.org_name}/repos"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def get_all_repos(self):
        repos = []
        page = 1
        while True:
            response = requests.get(self.repos_url, headers=self.headers, params={"page": page, "per_page": self.per_page})
            if response.status_code != 200:
                print(f"Error fetching repos: {response.status_code}, {response.text}")
                break
            page_data = response.json()
            if not page_data:
                break
            repos.extend(page_data)
            page += 1
        return repos

    def get_commits_for_repo(self, repo_name):
        commits = []
        page = 1
        while True:
            commits_url = f"{self.base_url}/repos/{self.org_name}/{repo_name}/commits"
            response = requests.get(commits_url, headers=self.headers, params={"page": page, "per_page": self.per_page})
            if response.status_code != 200:
                print(f"Error fetching commits for {repo_name}: {response.status_code}, {response.text}")
                break
            page_data = response.json()
            if not page_data:
                break
            commits.extend(page_data)
            page += 1
            time.sleep(self.timeout)  # To avoid hitting rate limits
        return commits

    def retrieve_commits(self, output_file="organization_commits.json", file_path=""):
        all_data = {}
        repos = self.get_all_repos()

        print(f"Found {len(repos)} repositories.")

        for repo in repos:
            repo_name = repo["name"]
            print(f"Fetching commits for repository: {repo_name}")
            commits = self.get_commits_for_repo(repo_name)
            all_data[repo_name] = commits

        # Save all data to a JSON file
        with open(file_path + output_file, "w") as json_file:
            json.dump(all_data, json_file, indent=4)

        print(f"All commits have been saved to {output_file}")
