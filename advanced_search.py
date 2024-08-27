import json
import re
from collections import defaultdict

# Hardcoded keywords to search for
KEYWORDS = ("currency", "add", "currencies", "blackcoin", "security")

# Optional settings
INCLUDE_COMMITTER = True
INCLUDE_AUTHOR = True

# Sorting options (set only one to True at a time)
SORT_BY_TOTAL_INSTANCES = True
SORT_BY_UNIQUE_FINDINGS = False

# New settings for advanced search
MATCH_WHOLE_WORD = False  # Set to True to match whole words only
MATCH_CASE = False       # Set to True to make letter case matter


def keyword_search_in_commit(commit_message):
    """Finds and counts the keywords in a commit message."""
    keyword_counts = defaultdict(int)
    total_instances = 0

    # Adjust keywords for case sensitivity
    keywords = KEYWORDS if MATCH_CASE else tuple(k.lower() for k in KEYWORDS)

    # Tokenize the commit message based on word boundaries
    words = re.findall(r'\b\w+\b', commit_message) if MATCH_WHOLE_WORD else commit_message.split()

    for word in words:
        word_to_match = word if MATCH_CASE else word.lower()

        if word_to_match in keywords:
            keyword_counts[word_to_match] += 1
            total_instances += 1

    unique_findings = len(keyword_counts)

    return unique_findings, total_instances, keyword_counts


def process_commits(commits_data):
    results = []

    for repo_name, commits in commits_data.items():
        for commit in commits:
            commit_message = commit.get('commit', {}).get('message', "")

            # Perform keyword search on the commit message
            unique_findings, total_instances, keyword_counts = keyword_search_in_commit(commit_message)

            # Only include commits where at least one keyword is found
            if unique_findings > 0:
                commit_info = {
                    "repo": repo_name,
                    "commit": {
                        "message": commit_message,
                        "unique_finds": unique_findings,
                        "instances": {
                            **keyword_counts,
                            "total": total_instances
                        }
                    }
                }

                if INCLUDE_COMMITTER:
                    commit_info["commit"]["committer"] = commit.get('commit', {}).get('committer', {}).get('email')

                if INCLUDE_AUTHOR:
                    commit_info["commit"]["author"] = commit.get('commit', {}).get('author', {}).get('email')

                results.append(commit_info)

    # Sort results based on chosen sorting option
    if SORT_BY_TOTAL_INSTANCES:
        results.sort(key=lambda x: x["commit"]["instances"]["total"], reverse=True)
    elif SORT_BY_UNIQUE_FINDINGS:
        results.sort(key=lambda x: x["commit"]["unique_finds"], reverse=True)

    return results


def save_to_json(data, filename="filtered_commits.json"):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)


def main():
    # Load the commits data from the JSON file
    with open("organization_commits.json", "r") as f:
        commits_data = json.load(f)

    # Process the commits to filter and count keywords
    filtered_commits = process_commits(commits_data)

    # Save the filtered commits to a new JSON file
    save_to_json(filtered_commits)

    print(f"Filtered commits saved to filtered_commits.json with {len(filtered_commits)} matching commits.")


if __name__ == "__main__":
    main()
