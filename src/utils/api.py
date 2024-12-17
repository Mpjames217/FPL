import requests

def get_all_player_data():
    try:
        result = requests.get('https://fantasy.premierleague.com/api/bootstrap-static').json()
        return result['elements']
    
    except:
        print('Error encounted accessing API. Execution will terminate')
        exit()
    

