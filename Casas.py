import requests
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import Workbook
from datetime import datetime

#Saca as informacoes do site
# soup
# base_link link do site
# hi, e,
# p elemento html com o preco
# a elemento html com o adress
# d elemento html com o descricao
# h elemento html com a descricao do espaco
# l elemento html com o link para o anuncio
def scrapping(soup, base_link, hi, e, p ,a ,d, ho, l):
    higher = soup.find_all(class_= hi)
    data=[]
    for h in higher   :
        elem= h.find(class_= e)
        if elem is not None:
            price = elem.find(class_= p)
            if price is not None:
                price = price.text.strip()
            else:
                price = "-"
            adress = elem.find(class_= a)
            description = elem.find(class_= d)
            house = elem.find(class_= ho)
            if house is not None:
                house = house.text.strip()
            else:
                house = "-"
            link = h.find(class_= l)

            if "Zimmer" not in adress.text.strip():
                adress = adress.text.strip()
            else:
                s= link.get('href').split('/')
                adress= s[3]
            departure_time = datetime.now()
            # Get directions using public transit
            duration = directions(adress)
            data.append({
                'Link': base_link + link.get('href') ,
                'Price': price,
                'Address': adress,
                'Typology': house,
                'Description': description.text.strip(), 
                'Walk to Sarasin': duration[0],
                'Transport to Sarasin': duration[1],
                'Walk to Roche': duration[2],
                'Transport to Roche': duration[3],
                'Walk to ETH': duration[4],
                'Transport to ETH': duration[5]
            })
    
    return data

def directions(address):
    print(address)
    duration = [0, 0, 0, 0 ,0, 0]
    departure_time = datetime.now()
    # Replace YOUR_API_KEY with your actual API key
    API_KEY = ''
    client = googlemaps.Client(API_KEY)
    # Get the latitude and longitude for the origin address
    geocode_result = client.geocode(address)
    origin_latlng = geocode_result[0]['geometry']['location']
    

    directions_sarasin_t = client.directions(origin_latlng, "Elisabethenstrasse 62, 4002 Basel, Suíça",
                                            mode="transit",
                                            departure_time=departure_time)
    directions_roche_t = client.directions(origin_latlng, "Grenzacherstrasse 124, 4058 Basel, Suíça",
                                        mode="transit",
                                        departure_time=departure_time)
    directions_eth_t = client.directions(origin_latlng, "4058, Spitalstrasse 33, 4056 Basel, Suíça",
                                        mode="transit",
                                        departure_time=departure_time)
    
    directions_sarasin_w = client.directions(origin_latlng, "Elisabethenstrasse 62, 4002 Basel, Suíça",
                                        mode="walking",
                                        departure_time=departure_time)
    directions_roche_w = client.directions(origin_latlng, "Grenzacherstrasse 124, 4058 Basel, Suíça",
                                        mode="walking",
                                        departure_time=departure_time)
    directions_eth_w = client.directions(origin_latlng, "4058, Spitalstrasse 33, 4056 Basel, Suíça",
                                        mode="walking",
                                        departure_time=departure_time)
    
    duration[0] = directions_sarasin_w[0]['legs'][0]['duration']['text']
    duration[1] = directions_sarasin_t[0]['legs'][0]['duration']['text']
    duration[2] = directions_roche_w[0]['legs'][0]['duration']['text']
    duration[3] = directions_roche_t[0]['legs'][0]['duration']['text']
    duration[4] = directions_eth_w[0]['legs'][0]['duration']['text']
    duration[5] = directions_eth_t[0]['legs'][0]['duration']['text']

    return duration


if __name__ == "__main__":
    workbook = Workbook()
    worksheet = workbook.active
    base_url = 'https://www.homegate.ch/rent/real-estate/city-basel/matching-list?ac=1&ah=1550&ep='
    headers = [ 'Link','Price', 'Address', 'Typology', 'Description',  'Walk to Sarasin', 'Transport to Sarasin', 'Walk to Roche', 'Transport to Roche', 'Walk to ETH', 'Transport to ETH']
    worksheet.append(headers)
    import googlemaps
    data = []

    #### Para cada site de casas é preciso um bloco destes e descobrir quais os elementos html que têm aas informaçoes que interecam
    if(1):
        urls = []
        #Numero de paginas que aparecem no site
        for i in range(1, 17):
            urls.append(base_url + str(i))

        for url in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            data.append( scrapping(soup, 'https://www.homegate.ch', 'ResultList_ListItem_3AwDq' , 'HgListingCard_info_1Pekk' , 'HgListingCard_price_20FqK' , 'HgListingCard_address_2sEgN' , 'HgListingDescription_description_2cJrA' , 'HgListingRoomsLivingSpace_roomsLivingSpace_3In1d HgListingCard_spotlight_26doz' , 'HgCardElevated_link_-LVSD' ))


    ####################################
    if(1):
        base_url = 'https://www.immoscout24.ch/de/immobilien/mieten/ort-basel?nrf=1&pt=16h&pn='
        urls = []
        for i in range(15):
            urls.append(base_url + str(i))

        for url in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            data.append( scrapping(soup, 'https://www.immoscout24.ch', 'Wrapper__WrapperStyled-gUcoSG kxWxEh' , 'Box-cYFBPY Flex-feqWzG MetaBody-iCkzuU JVKAR dCDRxm dUKbXG' , 'Box-cYFBPY hKJGPR Heading-daBLVV dOtgYu' , 'AddressLine__TextStyled-eaUAMD iBNjyG' , 'Text__TextStyled-fiIwWW Hxaps' , 'Box-cYFBPY hKJGPR Heading-daBLVV dOtgYu' , 'Wrapper__A-kVOWTT lfjjIW' ))

    #Quando o site nao deixa fazer web scraping, "rouba-se" a pagina html ("guardar como" no browser) e faz-se a mesma coisa que nas outras
    ####################################
    if(1):
        with open('ImmoMapper.html', encoding = 'utf-8') as f:
            html_string = f.read()
        soup = BeautifulSoup(html_string, 'html.parser')

        data.append(scrapping(soup, 'https://www.immomapper.ch', 'col-6 col-sm-12 col-md-12 col-lg-6 col-xl-6' , 'card-body pb-2 px-2 pt-0 mt-n1' , 'card-title mb-1 text-truncate' , 'card-text text-truncate small' , None , 'card-text text-truncate small' , 'stretched-link text-reset text-decoration-none' ))


    for d in data:
        for item in d:
            row = [item['Link'], item['Price'], item['Address'], item['Typology'],  item['Description'], item['Walk to Sarasin'], item['Transport to Sarasin'], item['Walk to Roche'], item['Transport to Roche'], item['Walk to ETH'], item['Transport to ETH']]
            worksheet.append(row)
    # Save the workbook to a file
    workbook.save('CasasV3.xlsx')

