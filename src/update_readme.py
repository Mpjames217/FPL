from github import Github
from dotenv import load_dotenv
import os
import regex as re
import src.utils.api as api

load_dotenv(override=True)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = os.environ.get("REPO")
TEAM_ID = os.environ.get("team_id")

def update_readme():
    # Authenticate with GitHub
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    # Fetch the README file
    try:
        readme = repo.get_contents("README.md")
        print("README.md fetched successfully.")
    except Exception as e:
        print(f"Error fetching README.md: {e}")
        return

    # Get the current content of the README
    current_content = readme.decoded_content.decode("utf-8")

    # Generate new content
    response = api.get_data('https://fantasy.premierleague.com/api/bootstrap-static')
    current_gw = api.get_current_gw(response)
    pattern = r"/event/[\d]{1,2}"
    updated_GW = f"/event/{current_gw}"

    new_content = re.sub(pattern, updated_GW, current_content)

    # Update the README file
    try:
        repo.update_file(
            path=readme.path,
            message="Automated update of README.md to have up-to-date link to FPL team",
            content=new_content,
            sha=readme.sha,
        )
        print("README.md updated successfully.")
    except Exception as e:
        print(f"Error updating README.md: {e}")

if __name__ == "__main__":
    update_readme()
