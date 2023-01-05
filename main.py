from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
import requests
import lxml
import csv

def scrape():
    VILLARICA_URL = requests.get('https://villaricapawnshop.ph/money-changer/').text
    SOUP = BeautifulSoup(VILLARICA_URL, 'lxml')
    TABLE = SOUP.find('table', class_='table table-striped')
    
    INFORMATION = TABLE.find_all('tr')
    
    needed_data = []

    for data in INFORMATION:
        data = data.text.replace('\n', '')
        needed_data.append(data)
    needed_data.pop(0)

    CURRENCIES = ['USD', 'EUR', 'JPY', 'AUD', 'CAD', 'GBP', 'HKD', 'SGD'] # Names of the currencies
    rates = [] # Float values for the currencies
    counter = 1
    for data in needed_data:
        if counter == 3:
            data = float(data[-6:])
            rates.append(data)
        elif counter ==7:
            data = float(data[-4:])
            rates.append(data)
        else:
            data = float(data[-5:])
            rates.append(data)
        counter += 1

    with open('data.csv', 'a') as file:
        csv_writer = csv.writer(file)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        csv_writer.writerow([f'Time:', current_time])
        index = 0
        for currency in CURRENCIES:
            csv_writer.writerow([f'{currency}', f'{rates[index]}'])
            index += 1
        csv_writer.writerow(' ')


if __name__ == "__main__":
    try:
        while True:
            scrape()
            sleep(21_600)
    except KeyboardInterrupt:
        exit()