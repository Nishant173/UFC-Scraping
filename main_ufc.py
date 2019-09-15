from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
import numpy as np



def get_soup_object(url):
    """
    Returns soup object of the source code from the given URL.
    """
    source_code = requests.get(url).text
    soup = BeautifulSoup(source_code, 'lxml')
    return soup



def pound_for_pound_rankings(soup):
    """
    Creates CSV file for Pound-to-pound rankings.
    """
    pfp_rankings = soup.find('div', class_='view-grouping')
    pfp_rankings = pfp_rankings.find('table', class_='views-table views-view-table cols-0')
    pfp_rankings = pfp_rankings.find_all('div', class_='view-content')

    list_rankings = list()
    list_fighters = list()

    for index, ranking_row in enumerate(pfp_rankings):
        list_rankings.append(index + 1)
        list_fighters.append(ranking_row.find('a').text)
    
    df_pfp_rankings = pd.DataFrame({
        "Ranking": list_rankings,
        "Fighter": list_fighters
    })
    date_string = str(datetime.today().date())
    df_pfp_rankings.to_csv("UFC - Pound for pound rankings - (Dated {}).csv".format(date_string), index=False)



def rankings_by_division(soup, division):
    """
    Creates CSV file for rankings by UFC division.
    """
    tbody = soup.find('tbody', class_='row-hover')
    fighters = tbody.findChildren('strong')
    fights_overall = tbody.findChildren('td', class_='column-5')
    fights_ufc = tbody.findChildren('td', class_='column-6')
    fights_previous = tbody.findChildren('td', class_='column-7')
    fights_next = tbody.findChildren('td', class_='column-8')

    # Set top 'n' fighters per division to extract info from.
    top = 20
    # Set counter to terminate loop after top 'n' fighters are extracted.
    counter = 0

    list_fighters = list()
    list_fights_overall = list()
    list_fights_ufc = list()
    list_fights_previous = list()
    list_fights_next = list()

    for fighter, fight_ufc, fight_overall, fight_previous, fight_next in zip(fighters, fights_ufc, fights_overall, fights_previous, fights_next):
        counter += 1
        
        list_fighters.append(fighter.text)
        list_fights_ufc.append(fight_ufc.text)
        list_fights_overall.append(fight_overall.text)
        list_fights_previous.append(fight_previous.text)
        list_fights_next.append(fight_next.text)
        
        if(counter > top):
            break


    df_by_division = pd.DataFrame({
        "Fighter": list_fighters,
        "Overall record": list_fights_overall,
        "UFC record": list_fights_ufc,
        "Last fight": list_fights_previous,
        "Next fight": list_fights_next
    })

    # Set ranking, re-order columns, add date, and save to CSV file.
    df_by_division['Ranking'] = np.arange(1, len(df_by_division) + 1)
    cols = ['Ranking', 'Fighter', 'Overall record', 'UFC record', 'Last fight', 'Next fight']
    df_by_division = df_by_division.loc[:, cols]
    date_string = str(datetime.today().date())
    division = division.capitalize()
    df_by_division.to_csv("UFC - {} division rankings - (Dated {}).csv".format(division, date_string), index=False)




if __name__ == '__main__':
    # Pount-for-pound rankings
    url = "https://www.ufc.com/rankings"
    soup = get_soup_object(url)
    pound_for_pound_rankings(soup)

    # Ranking by division
    divisions = ['flyweight', 'bantamweight', 'featherweight', 'lightweight',
                'welterweight', 'middleweight', 'light-heavyweight', 'heavyweight']
    
    for division in divisions:
        url = "http://rankingmma.com/ufc-rankings/{}/".format(division)
        soup = get_soup_object(url)
        rankings_by_division(soup, division)

