import os
import json
import sys
from settings import settings
from generators_commit_analysis.commit_retriever import CommitRetriever
from generators_commit_analysis.simple_analysis import CommitAnalyzer
from generators_commit_analysis.advanced_search import AdvancedCommitSearcher
from generators_commit_analysis.create_xlsm import ExcelCreator


# --- Helper Functions ---
def check_commits_file():
    if not os.path.exists(settings["files"]["file_path"] + settings["files"]["commits_file"]):
        raise FileNotFoundError(
            f"{settings['files']['commits_file']} does not exist. Run commit_retriever.py first to retrieve commits."
        )


# --- Main Execution ---
def main():
    # Step 1: Retrieve commits
    if settings["retrieve_commits"]["run"]:
        # Create an instance of CommitRetriever
        retriever = CommitRetriever(settings["retrieve_commits"]["org_name"], settings["base_settings"]["token"])

        # Retrieve and save commits
        retriever.retrieve_commits(settings["files"]["commits_file"], settings["files"]["file_path"])

    # Step 2: Run simple analysis
    if settings["simple_analysis"]["run"] or settings["advanced_search"]["run"]:
        try:
            check_commits_file()
        except FileNotFoundError as e:
            print(e)
            sys.exit(1)

        # Load commits data from JSON file
        with open(settings["files"]["file_path"] + settings["files"]["commits_file"], "r") as f:
            commits_data = json.load(f)

    if settings["simple_analysis"]["run"]:
        print("Running simple analysis...")
        # Create an instance of CommitAnalyzer
        analyzer = CommitAnalyzer(commits_data)

        # Perform analysis and print/save the results
        repo_analysis, total_commits, total_committers, total_authors = analyzer.analyze_commits()
        analyzer.print_and_save_results(
            repo_analysis=repo_analysis,
            total_commits=total_commits,
            total_committers=total_committers,
            total_authors=total_authors,
            output_file=settings["files"]["commits_analysis_file"],
            file_path=settings["files"]["file_path"]
        )
        print("Simple analysis completed!")

    # Step 3: Run advanced search
    if settings["advanced_search"]["run"]:
        print("Running advanced search...")
        # Create an instance of AdvancedCommitSearcher
        searcher = AdvancedCommitSearcher(
            keywords=settings["advanced_search"]["keywords"],
            exclude_repos=settings["advanced_search"]["exclude_repos"],
            include_committer=settings["advanced_search"]["include_committer"],
            include_author=settings["advanced_search"]["include_author"],
            match_whole_word=settings["advanced_search"]["match_whole_word"],
            match_case=settings["advanced_search"]["match_case"],
            contained_words=settings["advanced_search"]["contained_words"],
            same_words=settings["advanced_search"]["same_words"]
        )

        # Perform search and save results
        searcher.search_and_save_results(
            commits_data=commits_data,
            output_file=settings["files"]["keyword_search_file"],
            file_path=settings["files"]["file_path"],
            sort_by_total_instances=settings["advanced_search"]["sort_by_total_instances"],
            sort_by_unique_findings=settings["advanced_search"]["sort_by_unique_findings"]
        )
        print("Advanced search completed!")

    # Step 4: Run create xlsm
    if settings["create_xlsm"]["run"]:
        print("Creating Excel analysis...")
        excel_creator = ExcelCreator(
            commits_file=settings["files"]["commits_file"],
            analysis_file=settings["files"]["commits_analysis_file"],
            keyword_search_file=settings["files"]["keyword_search_file"],
            excel_file=settings["files"]["excel_file"],
            file_path=settings["files"]["file_path"]
        )
        excel_creator.create_workbook()
        print("Excel analysis completed!")


if __name__ == "__main__":
    main()
