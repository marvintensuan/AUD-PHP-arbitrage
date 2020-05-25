import os, requests, bs4, pyinputplus as pyip #, pandas as pd
from pathlib import Path

def get_bpi_data():
    #parse from BPI forex website
    bpi_website = requests.get("https://www.bpiexpressonline.com/p/2/2091/indicative-exchange-rates")
    bpi_website_html = bs4.BeautifulSoup(bpi_website.text, 'html.parser')
    bpi_rates_table = bpi_website_html.find(id='b301-infographic-content')
    bpi_table_rows = bpi_rates_table.select('tr')
    bpi_aud = bpi_table_rows[5] #fx rate
    bpi_time = bpi_rates_table.find('p')   
    #clean timestamp
    bpi_time = str(bpi_time.getText()).replace('\xa0', ' ')
    bpi_time = bpi_time.replace('As of', '')
    bpi_time = bpi_time.replace('  ', '')   
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

if __name__ == '__main__':
    #Title
    print ("AUD/PHP Arbitrage for Security Bank and BPI.")
    
    #Default file
    file_path = Path('D:/Projects/AUD forex/rates_table.csv')
    
    #Change to custom file
    print(" ".join(["Current file path is", str(file_path)]))
    i = pyip.inputYesNo(prompt='Do you want to change file?\n')
    if i in ['y', 'yes']:
        print(file_path)
        file_path = Path(input('Enter new file path.\n'))
        print(" ".join(["New file path will be", str(file_path)]))
    
    #get fx rates
    rates_from_bpi = get_bpi_data()
    
    
    #Read file_path as pandas DataFrame

    #rates_file = pd.read_csv(file_path)
    #rates_file.loc[-1] = []
    #print (rates_file)
    #save_file = rates_file.to_csv(file_path, index = False)
    