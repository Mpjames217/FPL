import pytest
import aiohttp
from aioresponses import aioresponses
from unittest.mock import AsyncMock, patch
from time import time
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
    # returns tuple
    # contains two dicts
    # dicts have keys 1-20
    # has correct values - mock/patch get data
    # total runtime under 0.5 sec

    response = get_data('https://fantasy.premierleague.com/api/bootstrap-static')
    all_players = response['elements']
    
    @pytest.mark.asyncio
    async def test_returns_tuple(self):
        result = await get_FDR_by_club(self.all_players)
        assert type(result) == tuple

    @pytest.mark.asyncio
    async def test_tuple_contains_two_dicts(self):
        result = await get_FDR_by_club(self.all_players)
        assert len(result) == 2

        for item in result:
            assert isinstance(item, dict)

    @pytest.mark.asyncio
    async def test_dict_keys_one_to_twenty(self):
        result = await get_FDR_by_club(self.all_players)
        expected_keys = [i for i in range(1,21)]

        for item in result:
            assert list(item.keys()) == expected_keys

    @pytest.mark.asyncio
    async def test_get_element_summaries(self):

        mock_element_summary_response = {"fixtures": [
                                                {"difficulty": 1},
                                                {"difficulty": 2},
                                                {"difficulty": 3}
                                            ]
                                        }
        player_id = 1
        url = f'https://fantasy.premierleague.com/api/element-summary/{player_id}'

        with aioresponses() as mock_response:
            mock_response.get(url, payload=mock_element_summary_response)

            async with aiohttp.ClientSession() as session:
                FDR_next_match, FDR_average = await get_element_summaries(player_id, session)

            assert FDR_next_match == 1
            assert FDR_average == 2.0


    @pytest.mark.asyncio
    async def test_get_FDR_by_club(self):

        with patch("src.utils.api.get_element_summaries", new_callable=AsyncMock) as mock_get_element_summaries:
            # Mock return values for each player's summaries
            mock_get_element_summaries.side_effect = [(i, i * 2) for i in range(1, 21)]

            result = await get_FDR_by_club(self.all_players)

            FDR_next_match, FDR_average = result

            for i in range(1, 21):
                assert FDR_next_match[i] == i
                assert FDR_average[i] == i * 2

    @pytest.mark.asyncio
    async def test_sends_requests_asynchronously(self):
        start_time = time()
        await get_FDR_by_club(self.all_players)
        execution_time = time() - start_time

        assert execution_time < 1





