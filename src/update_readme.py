from github import Github
from dotenv import load_dotenv
from datetime import datetime
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

    # Get the current content of the README - .decode needed?
    current_content = readme.decoded_content.decode("utf-8")

    # Generate new content
    game_info = api.get_data('https://fantasy.premierleague.com/api/bootstrap-static')
    current_gw = api.get_current_gw(game_info)
    updated_GW = f"/event/{current_gw}"

    if current_gw == '0':
        print('Game not started yet. Process terminating.')
        quit() 

    hyperlink_pattern = r"/event/[\d]{1,2}"
    new_content = re.sub(hyperlink_pattern, updated_GW, current_content)

    #team specific API call 
    team_info_address = 'https://fantasy.premierleague.com/api/entry/' + TEAM_ID + '/event/' + current_gw + '/picks'
    team_info = api.get_data(team_info_address)

    total_points = team_info['entry_history']['total_points']
    global_ranking = team_info['entry_history']['overall_rank']
    global_percentile = round(global_ranking / game_info['total_players'] * 100)
    updated_metrics = f"|2025/2026|{total_points}|{global_ranking}|{global_percentile}%|"

    metrics_pattern = r"\|2025/2026\|[\d]{1,4}\|[\d]{1,8}\|[\d]{1,3}%\|"
    new_content = re.sub(metrics_pattern, updated_metrics, new_content)
    
    timestamp_pattern = r"[\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updated_timestamp = timestamp

    new_content = re.sub(timestamp_pattern, updated_timestamp, new_content)
    # Update the README file
    try:
        repo.update_file(
            path=readme.path,
            message="Automated update of README.md to have up-to-date stats and link to FPL team",
            content=new_content,
            sha=readme.sha,
        )
        print("README.md updated successfully.")
    except Exception as e:
        print(f"Error updating README.md: {e}")

if __name__ == "__main__":
    update_readme()
