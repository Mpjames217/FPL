import pytest
import aiohttp
from aioresponses import aioresponses
from unittest.mock import AsyncMock, patch
import time
from src.utils.api import *

@pytest.mark.skip
class TestGetData():
    # Mock/ Patch requests.get
    # assert messages printed to console
    # assert program quit? Mock exit()?
    # assert python dict returned
    def test_returns_error_string(self):
        pass
    @patch("src.utils.api.requests.get")
    def test_returns_dict(self):
        pass

class TestGetCurrentGw():
    #returns string
    #return is correct
    response = get_data("https://fantasy.premierleague.com/api/bootstrap-static")

    def test_returns_string(self):
        result = get_current_gw(self.response)
        assert isinstance(result, str)

    def test_returns_correct_value(self):
        self.response['events'][0]['is_current'] = True
        result = get_current_gw(self.response)
        assert result == '1'

        self.response['events'][0]['is_current'] = False
        self.response['events'][1]['is_current'] = True
        result = get_current_gw(self.response)
        assert result == '2'


@pytest.mark.asyncio
class TestGetFdrByClub():
    # returns dict
    # keys are the next 3 GWs
    # contains list
    # lists must only contain numbers 1 - 5
    # has correct values - mock/patch get data 
    # one item per list when no dgw***
    # two items per list when dgw***
    # no items per list when bgw***
    # total runtime under 0.5 sec

    response = get_data('https://fantasy.premierleague.com/api/bootstrap-static')
    all_players = response['elements']
    current_gw = get_current_gw(response)
    #have called the funciton here to avoid ansycio complications
    start_time = time.time()
    result = asyncio.run(get_FDR_by_club(all_players, current_gw))
    execution_time = time.time() - start_time
        
    def test_returns_dict(self):
        assert type(self.result) == dict

    def test_dict_keys_are_club_ids(self):
        expected_keys = [i for i in range(1,21)]
        assert list(self.result.keys()) == expected_keys

    def test_dict_values_are_dicts(self):
        assert len(self.result) == 20

        for item in self.result.values():
            assert isinstance(item, dict)

    def test_inner_dict_keys_are_next_3_gws(self):
        current_gw = int(self.current_gw)
        expected_keys = [i for i in range(current_gw, current_gw + 3)]

        for item in self.result.values():
            assert list(item.keys()) == expected_keys

    def test_inner_dict_values_are_lists(self):
        for item in self.result.values():
            for inner_item in item.values():
                assert isinstance(inner_item, list)

    def test_list_values_are_valid(self):
        acceptable_values = [1,2,3,4,5]

        for item in self.result.values():
            for inner_item in item.values():
                for value in inner_item:
                    assert value in acceptable_values

    @pytest.mark.asyncio
    async def test_get_element_summaries(self):

        mock_element_summary_response = {"fixtures": [
                                                {"event": 1, "difficulty": 1},
                                                {"event": 2, "difficulty": 2},
                                                {"event": 3, "difficulty": 3}
                                            ]
                                        }
        player_id = 1
        url = f'https://fantasy.premierleague.com/api/element-summary/{player_id}'

        with aioresponses() as mock_response:
            mock_response.get(url, payload=mock_element_summary_response)

            async with aiohttp.ClientSession() as session:
                result = await get_fixtures_by_player(player_id, session, 1)

            assert result == {1: [1], 2: [2], 3: [3]}

    @pytest.mark.asyncio
    async def test_has_correct_values(self):

        with patch("src.utils.api.get_fixtures_by_player", new_callable=AsyncMock) as mock_get_fixtures_by_player:
            # Mock return values for each player's summaries
            mock_get_fixtures_by_player.return_value = {1: [1], 2: [2], 3: [3]}

            result = await get_FDR_by_club(self.all_players, 1)

        for i in range(1, 21):
            assert result[i] == {1: [1], 2: [2], 3: [3]}

    def test_sends_requests_asynchronously(self):
        assert self.execution_time < 1





