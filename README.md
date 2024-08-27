# GitHub Projects Analysis tools
1. Create GITHUB_TOKEN in developer settings with access to read repositories (access to private repositories requires full permissions on "repo" and read on "admin:org")
2. Add GITHUB_TOKEN to environmental variables (win+R -> _sysdm.cpl_ -> Advanced tab -> environmental variables) in eiter system or user variables by creating new variable with name "GITHUB_TOKEN" and paste GitHub token as value
3. Change organisation name in commit_retriever.py 