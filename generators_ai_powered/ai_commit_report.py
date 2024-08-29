from openai import OpenAI
import json

# Set your OpenAI API key
# openai.api_key = 'your_openai_api_key_here'

# File path for the commit messages JSON
organization_commits_file = '../generated_files/organization_commits.json'

client = OpenAI()


def load_commit_messages(file_path):
    """Load commit messages from the organization_commits.json file."""
    with open(file_path, 'r') as file:
        commits_data = json.load(file)

    # Extract all commit messages
    messages = []
    for repo, commits in commits_data.items():
        for commit in commits:
            commit_message = commit.get("commit", {}).get("message", "")
            if commit_message:
                messages.append((repo, commit_message))

    return messages


def generate_report(messages):
    """Generate a report using GPT based on the commit messages."""
    generated_report = ""

    # Combine all commit messages into a single input for GPT
    for repo, message in messages:
        generated_report += f"Repository: {repo}\nCommit Message: {message}\n\n"

    # Make API call to GPT to generate a report
    response = client.chat.completions.create(
        model="GPT-3.5 Turbo",
        messages=[
            {"role": "system", "content": "You are an AI that generates project reports based on commit messages."},
            {"role": "user",
             "content": f"Here are the commit messages:\n\n{generated_report}\n\nPlease generate a detailed report for this project and each repository."}
        ]
    )

    # Extract the generated report
    generated_report = response['choices'][0]['message']['content']

    return generated_report


def save_report(generated_report, file_path):
    """Save the generated report to a text file."""
    with open(file_path, 'w') as file:
        file.write(generated_report)


if __name__ == "__main__":
    # Load commit messages from the JSON file
    commit_messages = load_commit_messages(organization_commits_file)

    # Generate a report using GPT
    report = generate_report(commit_messages)

    # Save the generated report to a file
    report_file_path = '../generated_files/ai_commit_report.txt'
    save_report(report, report_file_path)

    print(f"Report saved to {report_file_path}")
