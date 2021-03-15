# welcome to my first python project
#the goal is to scrapp the stats of Larry Nance Jr (go pokes!) off sports ref

#imports
import requests
from bs4 import BeautifulSoup
import pandas as pd

def stat_player(url):
    #url='https://www.sports-reference.com/cbb/players/larry-nance-2.html'

    # getting response
    response=requests.get(url)

    #transforming it to soup that we can parse
    soup=BeautifulSoup(response.text,'lxml')

    # looking for td in html wich is part where we have our stats
    # Looking for a in html, subpart of th where we have the season
    # Looking for td, class left in html where school and conference are
    tds=soup.findAll('td',class_='right')
    as_=soup.findAll('th',class_='left')
    school_conf=soup.findAll('td',class_='left')

    #getting name
    h1s=soup.findAll('h1')
    name=h1s[0].text.strip("\n")

    #looking for stats in the tds, and the season in as_
    #stats is a dictionary. Doing one loop for seasons in as_ + putting name, second school and conf in school_conf
    # then third for stats in tds

    stats={}
    for a in as_:
        if a['data-stat'] in stats.keys():
            stats['name'].append(name)
            stats[a['data-stat']].append(a.text)
        else:
            stats['name']=[name]
            stats[a['data-stat']]=[a.text]
    for school in school_conf:
        if school['data-stat'] in stats.keys():
            stats[school['data-stat']].append(school.text)
        else:
            stats[school['data-stat']]=[school.text]
            
    for td in tds:
        if td['data-stat'] in stats.keys():
            stats[td['data-stat']].append(td.text)
        else:
            stats[td['data-stat']]=[td.text]

    #converting dict to df
    df=pd.DataFrame.from_dict(stats)

    #converting object to floats
    for col in df:
        df[col]=pd.to_numeric(df[col], errors='ignore')

    print(f"data was scrapped and csv for {df['name'][0]} was created")
    df.to_csv(f"sport_reference_players{df['name'][0]}.csv")
    return df