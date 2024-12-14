import utils, pprint, json

result = utils.get_all_player_data()['elements']

trimmed = []

trimmed.append(result[18])
trimmed.append(result[99])
trimmed.append(result[260])
trimmed.append(result[320])
trimmed.append(result[400])

with open('elements.json', 'w') as f:
    json.dump(trimmed, f)

