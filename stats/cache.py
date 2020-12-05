from selenium import webdriver
from bs4 import BeautifulSoup
import json

CACHE_DICT = {}
CACHE_FILENAME = "tankstats_cache.json"
HOME_URL = "https://tanks.gg"
TECH_TREE_URL = "https://tanks.gg/techtree/sweden"

def get_page(url):
    '''
    get html response using selenuium

    params: 
        url: str
    return:
        response
    '''

    browser = webdriver.Chrome()
    browser.get(url)
    response = browser.page_source
    browser.close()
    
    return response

def get_nation_href(url):
    '''
    get html reference for nations

    params: 
        url: str
    return:
        nation_list: list
    '''
    response = get_page_with_cache(url)
    page = BeautifulSoup(response, features="html.parser")
    
    tech_tree = page.find_all('div', class_ = 'techtree')[0]
    tech_tree_header = tech_tree.find('header')
    nation_list = []
    for a in tech_tree_header.find_all('a'):
        nation_href = a.get('href')
        nation_list.append(nation_href) 
    return nation_list

def get_tank_href(url):
    '''
    get html reference for tanks

    params: 
        url: str
    return:
        tank_list: list
    '''
    response = get_page_with_cache(url)
    page = BeautifulSoup(response, features="html.parser")

    tech_tree = page.find_all('div', class_ = 'tree')[0]

    tank_list = []
    for a in tech_tree.find_all('a'):
        nation_href = a.get('href')
        tank_list.append(nation_href) 
    return tank_list

def get_tank_stats(url):
    '''
    get stats of a tank

    params: 
        url: str
    return:
        stats: dictionary
    '''
    stats = {}
    response = get_page_with_cache(url)
    page = BeautifulSoup(response, features="html.parser")

    stats_cards = page.find_all('div', class_ = 'sections')[0]
    for stat in stats_cards.find_all('div', class_ = 'stat-line'):
        stats[stat.find('label').text] = stat.find('span').text

    title = page.find_all('div', class_ = 'clearfix header')[0]
    tags = title.find('small').text.split()
    stats['Tier'] = tags[1]
    stats['Country'] = tags[2]
    if len(tags) == 5:
        stats['Type'] = tags[3] + ' ' + tags[4]
    else:
        stats['Type'] = tags[3]
    return stats


def construct_unique_key(baseurl, params):
    ''' constructs a key that is guaranteed to uniquely and 
    repeatably identify an API request by its baseurl and params
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    string
        the unique key as a string
    '''
    if not params:
        return baseurl
    param_strings = []
    connector = '_'
    for k in params.keys():
        param_strings.append(f'{k}_{params[k]}')
    param_strings.sort()
    unique_key = baseurl + connector + connector.join(param_strings)
    return unique_key

def get_page_with_cache(baseurl, params = {}):
    '''Check the cache for a saved result for this baseurl+params:values
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.
  
    Parameters
    ----------s
    baseurl: string
        The URL for the API endpoint
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    '''
    unique_url = construct_unique_key(baseurl, params)
    
    if unique_url in CACHE_DICT:
        print('Using cache')
        return CACHE_DICT[unique_url]
    else: 
        print('Fetching')
        page = get_page(unique_url)
        CACHE_DICT[unique_url] = page
        save_cache(CACHE_DICT)
        return CACHE_DICT[unique_url]

def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 



if __name__ == "__main__":
    CACHE_DICT = open_cache()

    nation_list = get_nation_href(TECH_TREE_URL)
    tank_list = []
    tank_stats_dic = {}
    tank_tags_dic = {}
    for nation in nation_list:
        url = HOME_URL + nation
        tank_list += get_tank_href(url)
    for index, tank in enumerate(tank_list):
        url = HOME_URL + tank
        stats = get_tank_stats(url)
        tank_stats_dic[tank[6:]] = stats
        print("Progress "+ str(index) + '/' + str(len(tank_list)-1))
    
    f = open("tank_list.txt","w")
    f.write(str(tank_list))
    f.close()

    dumped_json_cache = json.dumps(tank_stats_dic)
    f = open("tankstats_stats.json","w")
    f.write(dumped_json_cache)
    f.close()


    