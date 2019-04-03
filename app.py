import requests
from bs4 import BeautifulSoup


BRISBANE = 'https://www.brisbanepollen.com.au/'
MELBOURNE = 'https://www.melbournepollen.com.au/'
CANBERRA = 'https://www.canberrapollen.com.au/'
SYDNEY = 'https://www.sydneypollen.com.au/'


def get_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content.decode('utf-8'), 'html.parser')
    return soup


def get_pollen_level_today(soup):
    result = soup.find(id='plevel')
    if result:
        return result.string

    result = soup.find(class_='pollen-level')
    if result:
        return result.string



def get_pollen_level_yesterday(soup):
    result =  soup.find(id='plevel2')
    if result:
        return result.string


def get_date(soup):
    """Format: weekday | month | date | year"""
    result =  soup.find(id='pdate')
    if result:
        return result.string


def get_pollen_header(soup):
    """Today's pollen header"""
    result = soup.find(class_='pollen-header')
    if result:
        return result.text


def get_pollen_grass_count(soup):
    """Grass pollen grains per m^3 of air."""
    result =  soup.find(id='pgrass')
    if result:
        return result.string


def get_data_provider(soup):
    result = soup.find(id='data-provid')
    if result:
        return result.string


def get_pollen_forecast_header(soup):
    result = soup.find(class_='pollen-forecast-header')
    if result:
        return result.text


def _get_pollen_forecast_day(soup, day):
    result = soup.find(id=f'dy{day}')
    if result:
        return result.string


def _get_pollen_forecast_date(soup, day):
    result = soup.find(id=f'dt{day}')
    if result:
        return result.string


def _get_pollen_forecast_value(soup, day):
    result = soup.find(id=f'fc{day}')
    if result:
        return result.string


def get_pollen_forecast_data(soup):
    """Get the pollen forecast for the week. (Six days)"""
    data = []
    for i in range(1, 7):
        day = _get_pollen_forecast_day(soup, i)
        date = _get_pollen_forecast_date(soup, i)
        value = _get_pollen_forecast_value(soup, i)
        data.append({
            'day': day,
            'date': date,
            'value': value
        })
    return data


def get_error_msg(soup):
    result = soup.find(id='pmsg')
    if result:
        return result.text


if __name__ == '__main__':
    soup = get_soup(MELBOURNE)
    today = get_pollen_level_today(soup)
    yesterday = get_pollen_level_yesterday(soup)
    header = get_pollen_header(soup)
    count = get_pollen_grass_count(soup)
    provider = get_data_provider(soup)
    forecast_header = get_pollen_forecast_header(soup)
    data = get_pollen_forecast_data(soup)
    error = get_error_msg(soup)
    print(today)
    print(yesterday)
    print(header)
    print(count)
    print(provider)
    print(forecast_header)
    for d in data:
        print(d)
    print(error)