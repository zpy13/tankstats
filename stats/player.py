from bs4 import BeautifulSoup
import json, requests

# server_list = ["EU","US","SEA","RU"]

def get_player_stats(server, player_id):
    url = f"http://www.wotinfo.net/en/efficiency?server={server}&playername={player_id}"

    response = requests.get(url)
    page = BeautifulSoup(response.text, "html.parser")
    try:
        stats = page.find_all('div', class_ = "col-sm-6")[0]
    except:
        return None
    output = []
    for a in stats.find_all('p'):
            output.append(a.text.strip())
    for i in range(len(output)):
        output_list = output[i].replace('\n','').split()
        output[i] = ""
        for st in output_list:
            output[i] = output[i] + " " + st
        output[i] = output[i][1:]
    return output
