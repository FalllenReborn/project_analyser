import os

settings = {
    "base_settings": {
        "token": os.getenv("GITHUB_TOKEN"),
        "gpt_key": os.getenv("OPENAI_API_KEY"),
    },

    "files": {
        "file_path": "generated_files/",
        "commits_file": "organization_commits.json",
        "commits_analysis_file": "commit_analysis.txt",
        "keyword_search_file": "keyword_search_results.json",
        "excel_file": "project_analysis.xlsm"
    },

    "retrieve_commits": {
        "run": False,   # Should commit_retriever.py run
        "org_name": "novaexchange",   # retrieve all repositories from targeted organisation
    },

    "simple_analysis": {
        "run": True
    },

    "advanced_search": {
        "run": True,
        "keywords": (
            "currency", "crypto", "currencies", "blackcoin", "ReddCoin", "Phoenix", "DigiByte", "Decred", "GlobalBoost",
            "OnixCoin", "MotaCoin", "Nexus", "Unobtanium", "RYI", "Unityventures", "HempCoin", "cryptocurrency"
        ),
        "exclude_repos": (),   # Write repositories to exclude from search
        "include_committer": True,
        "include_author": True,
        "match_whole_word": False,  # Set to True to match whole words only
        "match_case": False,        # Set to True to make letter case matter
        "contained_words": True,   # Skip counting shorter words contained within longer words
        "same_words": True,         # Skip counting the same word multiple times
        # Sorting options (set only one to True at a time)
        "sort_by_total_instances": True,   # todo convert into single variable with priority rather than chose one
        "sort_by_unique_findings": False   # todo convert into single variable with priority rather than chose one
    },

    "create_xlsm": {
        "run": True
    }
}
