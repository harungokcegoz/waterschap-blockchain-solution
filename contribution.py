import subprocess
import re
import matplotlib.pyplot as plt

# Function to get the list of authors with names and email addresses
def get_contributors_with_emails():
    cmd = "git log --format='%an' | sort | uniq"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = result.stdout.strip()
    contributors = output.split('\n')
    return contributors

# Function to get contributions for a specific author
def get_contributions_for_author(author):
    cmd = f"git log --author='{author}' --shortstat --no-merges 'develop' -- . ':(exclude)client/package-lock.json'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = result.stdout

    insertions = 0
    deletions = 0
    contributions = []

    pattern = re.compile(r'(\d+) insertions?\(\+\), (\d+) deletions?\(-\)')

    for line in output.split('\n'):
        match = pattern.search(line)
        if match:
            insertions = int(match.group(1))
            deletions = int(match.group(2))
       
            total_changes = insertions + deletions
            contributions.append(total_changes)

    print(f"Contributions for {author}: {contributions}")
    return contributions

# Main function to visualize contributions
def visualize_contributions():
    contributors = get_contributors_with_emails()
    total_contributions = []
    contributor_names = []

    for contributor in contributors:
        contributions = get_contributions_for_author(contributor)
        if sum(contributions) > 0:
            total_contributions.append(sum(contributions))
            contributor_names.append(contributor)
        else:
            continue

    total_sum = sum(total_contributions)

    if total_sum == 0:
        print("No contributions found.")
        return

    percentages = [(contribution / total_sum) * 100 for contribution in total_contributions]
    
    plt.figure(figsize=(8, 8))
    plt.pie(percentages, labels=contributor_names, autopct='%1.1f%%', startangle=140)
    plt.title('Contributions by Contributor')
    plt.axis('equal')
    plt.show()

if __name__ == "__main__":
    visualize_contributions()
