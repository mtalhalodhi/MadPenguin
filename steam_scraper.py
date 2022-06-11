import requests
from bs4 import BeautifulSoup

def get_release_date_for_game_from_steam(game_name):
    """
    Returns the release date for a game from Steam.
    """
    url = "https://store.steampowered.com/search/?sort_by=_ASC&term=" + game_name
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    game_info = soup.find('div', id='search_result_container')
    if len(game_info) == 0:
        return "No results found for " + game_name
    else:
        return game_info.find_all('div', class_='col search_released responsive_secondrow')[0].text
    