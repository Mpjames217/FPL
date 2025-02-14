import requests, os, dotenv
from pprint import pprint

dotenv.load_dotenv()

pl_profile = os.environ.get('FPL_COOKIE')
datadtome = os.environ.get('FPL_COOKIE2')
team_id = os.environ.get('team_id')
email = os.environ.get('FPL_EMAIL')
password = os.environ.get('FPL_PASSWORD')


def FPL_login(session):
    payload = {
        "login": email,
        "password": password,
        "app": "plfpl-web",
        "redirect_uri": "https://fantasy.premierleague.com/a/login"
    }

    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; PRO 5 Build/LMY47D)",
        "Cookie": f"datadome={datadtome};pl_profile={pl_profile}"
    }

    login_url = "https://users.premierleague.com/accounts/login/"
    response = session.post(login_url, data=payload,headers=headers)

    print(response)
    return session

def get_FPL_team(session):

    url = f"https://fantasy.premierleague.com/api/my-team/{os.environ.get('team_id')}/"

    response = session.get(url)

    print(response)

    team = response.json()

    pprint(team)

    return team


def change_captain(new_captain_id, new_vice_captain_id, team):
    '''Update the team lineup with the new captain and vice-captain'''

    for player in team['picks']:
        if player["element"] == new_captain_id:
            player["is_captain"] = True
        else:
            player["is_captain"] = False

        if player["element"] == new_vice_captain_id:
            player["is_vice_captain"] = True
        else:
            player["is_vice_captain"] = False

s = requests.Session()
s = FPL_login(s)
team = get_FPL_team(s)

new_captain_id = 401
new_vice_captain_id = 328

# change_captain(new_captain_id, new_captain_id, team)

# url = f"https://fantasy.premierleague.com/api/my-team/{os.environ.get('team_id')}/"
# response = s.post(url, json=team)
# print(response)