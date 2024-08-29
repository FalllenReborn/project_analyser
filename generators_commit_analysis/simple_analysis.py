class CommitAnalyzer:
    def __init__(self, commits_data):
        self.commits_data = commits_data

    def analyze_commits(self):
        total_commits = 0
        total_committers = set()
        total_authors = set()
        repo_analysis = []

        for repo_name, commits in self.commits_data.items():
            repo_commit_count = len(commits)
            repo_committers = set()
            repo_authors = set()

            for commit in commits:
                committer = commit.get('commit', {}).get('committer', {}).get('email')
                author = commit.get('commit', {}).get('author', {}).get('email')

                if committer:
                    repo_committers.add(committer)
                    total_committers.add(committer)
                if author:
                    repo_authors.add(author)
                    total_authors.add(author)

            repo_analysis.append({
                'repository': repo_name,
                'commit_count': repo_commit_count,
                'committer_count': len(repo_committers),
                'author_count': len(repo_authors),
            })

            total_commits += repo_commit_count

        return repo_analysis, total_commits, len(total_committers), len(total_authors)

    @staticmethod
    def print_and_save_results(repo_analysis, total_commits, total_committers,
                               total_authors, output_file="commit_analysis.txt", file_path=""):
        with open(file_path + output_file, "w") as f:
            f.write("Commit Analysis Report:\n\n")

            for repo in repo_analysis:
                repo_info = (
                    f"Repository: {repo['repository']}\n"
                    f" - Total commits: {repo['commit_count']}\n"
                    f" - Unique committers: {repo['committer_count']}\n"
                    f" - Unique authors: {repo['author_count']}\n\n"
                )
                print(repo_info)
                f.write(repo_info)

            total_info = (
                f"Overall Summary:\n"
                f" - Total commits across all repositories: {total_commits}\n"
                f" - Total unique committers across all repositories: {total_committers}\n"
                f" - Total unique authors across all repositories: {total_authors}\n"
            )
            print(total_info)
            f.write(total_info)
