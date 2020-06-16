import os
import requests
import bs4
import pandas as pd
import datetime
from pathlib import Path
import dateutil.parser as dparser

def get_bpi_data():
    #parse from BPI forex website
    bpi_website = requests.get(
                               "https://www.bpiexpressonline.com/"
                               "p/2/2091/indicative-exchange-rates")
    bpi_website_html = bs4.BeautifulSoup(bpi_website.text, 'html.parser')
    bpi_rates_table = bpi_website_html.find(id='b301-infographic-content')
    bpi_table_rows = bpi_rates_table.select('tr')
    bpi_aud = bpi_table_rows[5] #fx rate
    bpi_time = bpi_rates_table.find('p')   
    #clean timestamp
    bpi_time = dparser.parse(str(bpi_time.getText()).replace('\xa0', ' '),
                             fuzzy = True, ignoretz = True) 
    #clean rates data
    bpi_aud = str(bpi_aud.getText()) #convert to text
    bpi_aud = bpi_aud.replace("\n", ",") #replace \n with comma
    bpi_aud = bpi_aud.replace("\xa0", "") #remove \xa0
    bpi_aud = bpi_aud.split(",")
    #return value
    bpi_data = list()
    bpi_data.append(bpi_time)
    bpi_data.append(bpi_aud[3])
    bpi_data.append(float(bpi_aud[6]))
    bpi_data.append(float(bpi_aud[7]))
    return bpi_data

def get_sb_data():
    #parse from Security Bank website
    sb_website = requests.get(
                              "https://www.securitybank.com/"
                              "personal/investments/market-information/"
                              "foreign-exchange-rate-forex/")
    sb_website_html = bs4.BeautifulSoup(sb_website.text, 'html.parser')
    sb_rates_table = sb_website_html.find_all('div', {'class': 'et_pb_text_inner'})
    sb_time = dparser.parse(sb_rates_table[2].getText(),
                            fuzzy = True, ignoretz = True)
    sb_table_rows = sb_rates_table[1].select('tr')
    sb_aud = sb_table_rows[6].getText() #fx rate

    #clean rates data
    sb_aud = str(sb_aud.replace('\n', ',')).split(',')
    #return value
    sb_data = list()
    sb_data.append(sb_time)
    sb_data.append(sb_aud[1])
    sb_data.append(sb_aud[3])
    sb_data.append(sb_aud[5])
    return sb_data

if __name__ == '__main__':
    #Title
    print("AUD/PHP Arbitrage for Security Bank and BPI.")
    
    #Default file
    file_path = Path('D:/Projects/AUD forex/rates_table.csv')

    #get fx rates
    rates_from_bpi = get_bpi_data()
    rates_from_sb = get_sb_data()
    #output
    output_data = list()
    output_data.append(str(datetime.datetime.now()))
    output_data.append(rates_from_bpi[0])
    output_data.append(rates_from_bpi[2])
    output_data.append(rates_from_bpi[3])
    output_data.append(rates_from_sb[0])
    output_data.append(rates_from_sb[2])
    output_data.append(rates_from_sb[3])

    #Read file_path as pandas DataFrame
    rates_file = pd.read_csv(file_path)
    rates_file.loc[-1] = output_data
    print(rates_file)
    save_file = rates_file.to_csv(file_path, index = False)
    