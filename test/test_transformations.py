import pytest, json
from src.utils.transform import *

class TestTransformAllPlayerData():
    # returns dict
    # dict has correct keys
    # values are lists of dicts
    # values have correct keys
    # values are correct

    with open('test/test_data/elements.json') as f:
        data = json.load(f)

    def test_returns_dict(self):
        result = transform_all_player_data(self.data)
        assert isinstance(result, dict)

    def test_dict_has_correct_keys(self):
        result = transform_all_player_data(self.data)
        expected_keys = ['GK', 'DEF', 'MID', 'FWD']
        for key in result.keys():
            assert key in expected_keys

    def test_values_are_lists_of_dicts(self):
        result = transform_all_player_data(self.data)
        for item in result.values():
            assert isinstance(item, list)
            for nested_item in item:
                assert isinstance(nested_item, dict)
        
    def test_each_item_has_correct_keys(self):
        result = transform_all_player_data(self.data)
        expected_keys = ['name', 'club', 'cost', 'points']
        for item in result.values():
            for nested_item in item:
                for key in nested_item.keys():
                    assert key in expected_keys

    def test_values_are_correct(self):
        result = transform_all_player_data(self.data)
        assert result == { 'DEF': [
                                {
                                    'club': 10,
                                    'cost': 3.9,
                                    'name': 'Burgess',
                                    'points': 9,
                                },
                            ],
                            'FWD': [
                                {
                                    'club': 8,
                                    'cost': 5.0,
                                    'name': 'Beto',
                                    'points': 16,
                                },
                            ],
                            'GK': [
                                {
                                    'club': 3,
                                    'cost': 4.0,
                                    'name': 'Dennis',
                                    'points': 0,
                                },
                            ],
                            'MID': [
                                {
                                    'club': 1,
                                    'cost': 6.8,
                                    'name': 'Trossard',
                                    'points': 46,
                                },
                                {
                                    'club': 12,
                                    'cost': 13.1,
                                    'name': 'M.Salah',
                                    'points': 124,
                                },
                            ],
                            }

class TestGetUniquePricePoints():
    #returns dict
    #dict keys are positions from all_player_data
    #values are lists of floats
    #values are correct
    with open('test/test_data/elements.json') as f:
        data = json.load(f)

    all_player_data = transform_all_player_data(data)

    def test_returns_dict(self):
        result = get_unique_price_points(self.all_player_data)
        assert isinstance(result, dict)

    def test_has_correct_keys(self):
        result = get_unique_price_points(self.all_player_data)
        expected_keys = ['GK', 'DEF', 'MID', 'FWD']
        for key in result.keys():
            assert key in expected_keys

    def test_has_correct_values(self):
        result = get_unique_price_points(self.all_player_data)
        assert result == {'DEF': [3.9], 'FWD': [5.0], 'GK': [4.0], 'MID': [13.1, 6.8]}


                                