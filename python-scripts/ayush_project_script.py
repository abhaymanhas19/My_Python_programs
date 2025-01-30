import httpx
from bs4 import BeautifulSoup
import csv

SITES_URLS=[
    ("raywhite.com","https://raywhiteapi.ep.dynamics.net/v1/suburbs?apiKey=6625c417-067a-4a8e-8c1d-85c812d0fb25"),
    ("ljhooker.com.au",""),
    ("harcourts.com.au"),
    ("barryplant.com.au"),
    ("jelliscraig.com.au"),
    ("bigginandscott.com.au"),
    ("obrienrealestate.com.au"),
    ("mcgrath.com.au"),
    ("belleproperty.com"),
    ("vicprop.com.au"),
    ("hockingstuart.com.au"),
    ("nelsonalexander.com.au"),
    ("fletchers.ner.au"),
    ("marshallwhite.com.au"),
    ("kayburton.com.au"),
    ("rtedgar.com"),
    ("noeljones.com.au") 
]

def scrape_agency():
    with  httpx.Client() as client:
        for agency_url  in SITES_URLS:
            response =  client.get(agency_url[1])
            soup = BeautifulSoup(response.text, 'html.parser')
            print(soup)
        
    agents_data = []
    
    # Hypothetical loop
    # for office in offices_for_vic:
    #     office_link = office.find('a')['href']
    #     office_page = requests.get(office_link)
    #     office_soup = BeautifulSoup(office_page.text, 'html.parser')
        
    #     # Grab each agent listing in that office
    #     agent_cards = office_soup.find_all('div', class_='agent-card')
    #     for agent_card in agent_cards:
    #         name = agent_card.find('h3', class_='agent-name').get_text()
    #         phone = agent_card.find('span', class_='agent-phone').get_text()
    #         email = agent_card.find('a', class_='agent-email').get('href').replace("mailto:", "")
    #         # Possibly refine phone/email extraction as needed
    #         
    #         agents_data.append([agency_name, name, email, phone, 'Victoria']
scrape_agency()
