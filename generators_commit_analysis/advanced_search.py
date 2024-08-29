import json
import re
from collections import defaultdict


class AdvancedCommitSearcher:
    def __init__(self, keywords, exclude_repos=(), include_committer=True, include_author=True,
                 match_whole_word=False, match_case=False, contained_words=False, same_words=True):
        self.keywords = keywords
        self.exclude_repos = exclude_repos
        self.include_committer = include_committer
        self.include_author = include_author
        self.match_whole_word = match_whole_word
        self.match_case = match_case
        self.contained_words = contained_words
        self.same_words = same_words

    def keyword_search_in_commit(self, commit_message):
        keyword_counts = defaultdict(int)
        total_instances = 0
        found_keywords = set()

        search_message = commit_message if self.match_case else commit_message.lower()

        def is_whole_word_match(word, message):
            return bool(re.search(rf'\b{re.escape(word)}\b', message))

        for keyword in self.keywords:
            keyword_to_search = keyword if self.match_case else keyword.lower()

            if self.match_whole_word:
                if is_whole_word_match(keyword_to_search, search_message):
                    found_keywords.add(keyword_to_search)
                    keyword_counts[keyword] += 1
            else:
                if keyword_to_search in search_message:
                    found_keywords.add(keyword_to_search)
                    keyword_counts[keyword] += search_message.count(keyword_to_search)

        if self.same_words:
            for keyword in found_keywords:
                keyword_counts[keyword] = 1
                total_instances += 1
        else:
            total_instances = sum(keyword_counts.values())

        if not self.contained_words:
            found_keywords_sorted = sorted(found_keywords, key=len, reverse=True)
            to_remove = set()
            for i in range(len(found_keywords_sorted)):
                for j in range(i + 1, len(found_keywords_sorted)):
                    if found_keywords_sorted[j] in found_keywords_sorted[i]:
                        to_remove.add(found_keywords_sorted[j])

            for word in to_remove:
                if word in keyword_counts:
                    total_instances -= keyword_counts[word]
                    del keyword_counts[word]

        return total_instances, keyword_counts

    def process_commits(self, commits_data):
        results = {}

        for repo, commits in commits_data.items():
            if repo in self.exclude_repos:
                continue

            for commit in commits:
                commit_message = commit.get("commit", {}).get("message", "")
                commit_date = commit.get("commit", {}).get("committer", {}).get("date", "unknown")
                total_instances, keyword_counts = self.keyword_search_in_commit(commit_message)

                if total_instances > 0:
                    commit_hash = commit.get("sha", "unknown")
                    results[commit_hash] = {
                        "repo": repo,
                        "commit": {
                            "message": commit_message,
                            "unique_finds": len(keyword_counts),
                            "instances": keyword_counts,
                            "total_instances": total_instances,
                            "commit_date": commit_date
                        }
                    }

                    if self.include_committer:
                        committer_info = commit.get("commit", {}).get("committer", {})
                        committer_name = committer_info.get("name", "unknown") if committer_info else "unknown"
                        results[commit_hash]["commit"]["committer"] = committer_name

                    if self.include_author:
                        author_info = commit.get("author", {})
                        author_name = author_info.get("name", "unknown") if author_info else "unknown"
                        results[commit_hash]["commit"]["author"] = author_name

        return results

    @staticmethod
    def sort_results(results, sort_by_total_instances=True, sort_by_unique_findings=False):
        if sort_by_total_instances:
            return dict(sorted(results.items(), key=lambda item: item[1]["commit"]["total_instances"], reverse=True))
        elif sort_by_unique_findings:
            return dict(sorted(results.items(), key=lambda item: item[1]["commit"]["unique_finds"], reverse=True))
        return results

    def search_and_save_results(self, commits_data, output_file="keyword_search_results.json", file_path="",
                                sort_by_total_instances=True, sort_by_unique_findings=False):
        results = self.process_commits(commits_data)
        sorted_results = self.sort_results(results, sort_by_total_instances, sort_by_unique_findings)

        with open(file_path + output_file, "w") as result_file:
            json.dump(sorted_results, result_file, indent=4)
