import os
import requests
import json
import time

# Replace with your GitHub organization and personal access token
ORG_NAME = "novaexchange"
TOKEN = os.getenv("GITHUB_TOKEN")
print(f"TOKEN: {TOKEN}")

# GitHub API URLs
BASE_URL = "https://api.github.com"
REPOS_URL = f"{BASE_URL}/orgs/{ORG_NAME}/repos"

# Headers for authentication
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


def get_all_repos():
    repos = []
    page = 1
    while True:
        response = requests.get(REPOS_URL, headers=HEADERS, params={"page": page, "per_page": 100})
        if response.status_code != 200:
            print(f"Error fetching repos: {response.status_code}, {response.text}")
            break
        page_data = response.json()
        if not page_data:
            break
        repos.extend(page_data)
        page += 1
    return repos


def get_commits_for_repo(repo_name):
    commits = []
    page = 1
    while True:
        commits_url = f"{BASE_URL}/repos/{ORG_NAME}/{repo_name}/commits"
        response = requests.get(commits_url, headers=HEADERS, params={"page": page, "per_page": 100})
        if response.status_code != 200:
            print(f"Error fetching commits for {repo_name}: {response.status_code}, {response.text}")
            break
        page_data = response.json()
        if not page_data:
            break
        commits.extend(page_data)
        page += 1
        time.sleep(1)  # To avoid hitting rate limits
    return commits


def main():
    all_data = {}

    print("Fetching all repositories...")
    repos = get_all_repos()
    print(f"Found {len(repos)} repositories.")

    for repo in repos:
        repo_name = repo["name"]
        print(f"Fetching commits for repository: {repo_name}")
        commits = get_commits_for_repo(repo_name)
        all_data[repo_name] = commits

    # Save all data to a JSON file
    with open("organization_commits.json", "w") as json_file:
        json.dump(all_data, json_file, indent=4)

    print("All commits have been saved to organization_commits.json")


if __name__ == "__main__":
    main()
