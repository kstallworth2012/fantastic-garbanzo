#This is a little application using the the MASSIVE STOCK 
#api ... I think it was called polygon io at some point 
#stock trading data extractor 
import os
from dotenv import load_dotenv
import requests
import schedule
import time
from datetime import datetime
import csv 


#Load the environment variables from the .env file 
load_dotenv()

massive_key = os.environ.get("MASSIVE_API_KEY")
LIMIT =  500

url = f'https://api.massive.com/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={massive_key}'
next_uniform_resource_locator= 'https://api.massive.com/v3/reference/tickers?cursor=YWN0aXZlPXRydWUmYXA9JTVCJTIyQ05YQyUyMiUyQyUyMjIwMjYtMTAtMjElMjIlNUQmYXM9JTVCJTIyQ05YQzAwMDE4MDM1OTklMjIlNUQmbGltaXQ9NTAwJm1hcmtldD1zdG9ja3Mmb3JkZXI9YXNjJnNvcnQ9dGlja2Vy' + f'&apikey={massive_key}'
next_uniform_resource_locator_two = 'https://api.massive.com/v3/reference/tickers?cursor=YWN0aXZlPXRydWUmYXA9JTVCJTIyR01FLldTJTIyJTJDJTIyMjAyNi0xMC0yMSUyMiU1RCZhcz0lNUIlMjJHTUUuV1MwMDAxMzI2MzgwJTIyJTVEJmxpbWl0PTUwMCZtYXJrZXQ9c3RvY2tzJm9yZGVyPWFzYyZzb3J0PXRpY2tlcg' + f'&apikey={massive_key}'
next_uniform_resource_locator_three = 'https://api.massive.com/v3/reference/tickers?cursor=YWN0aXZlPXRydWUmYXA9JTVCJTIyTUlUSyUyMiUyQyUyMjIwMjYtMTAtMjElMjIlNUQmYXM9JTVCJTIyTUlUSzAwMDA4MDc4NjMlMjIlNUQmbGltaXQ9NTAwJm1hcmtldD1zdG9ja3Mmb3JkZXI9YXNjJnNvcnQ9dGlja2Vy' + f'&apikey={massive_key}'


def my_write_to_csv(json_schema,output_filename,data_list):
    """This function will take a json_schema or dictionary and csv file name as a string as an argument and write a csv file with the 
        csv file name given 
        AND 
        we will have to include the list of items requested from the api ... that we converted to a list 
    """
    fieldnames = list(json_schema.keys())

    with open(output_filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for data in data_list:
            row = {key: data.get(key,'') for key in fieldnames}
            writer.writerow(row)
    print(f'\nWrote {len(data_list)} rows to {output_filename}\n')

def get_more_data(url,addl_request_number):
    """We are on a api limit so we are writing this function to request 
    another set of data based on the next url in the first request
    we will then return a list 
    """
    result = requests.get(url)

    tickers2 = []

    data = result.json()

    for ticker in data['results']:
        tickers2.append(ticker)

    while 'next_url' in data and addl_request_number >= 0:
        print("\n\n=============REQUESTING NEXT PAGE OF RESULTS=========================================\n\n")
        result = requests.get(data['next_url'] + f'&apikey={massive_key}')
        data = result.json() 
        print(data)
        for ticker in data['results']:
            tickers2.append(ticker)
            # print(f'\n============================\n{ticker}')
        addl_request_number -= 1

    return tickers2


def main():
    print("\n===========LOAD STOCK DATA=================================\n")
    # result = requests.get(url)

    # tickers = []

    # data = result.json() 
    
    
    # print("\n\n===================================\n\n")
    # print(data.keys())


    example_ticker = {
        'ticker': 'BKH', 
        'name': 'Black Hills Corporation', 
        'market': 'stocks', 
        'locale': 'us', 
        'primary_exchange': 'XNYS', 
        'type': 'CS', 'active': True, 
        'currency_name': 'usd', 
        'cik': '0001130464', 
        'composite_figi': 'BBG000BD9ZM7', 
        'share_class_figi': 'BBG001S5P6X8', 
        'last_updated_utc': '2026-10-22T06:08:59.724325978Z'
        }
    


    # print(f'The number of tickers we have: data["count"]')

    # for ticker in data['results']:
    #     tickers.append(ticker)
    #     # print(f'\n============================\n{ticker}')



    # number_of_requests = 3
    # while 'next_url' in data and number_of_requests >= 0:
    #     print("\n\n=============REQUESTING NEXT PAGE OF RESULTS=========================================\n\n")
    #     result = requests.get(data['next_url'] + f'&apikey={massive_key}')
    #     data = result.json() 
    #     print(data)
    #     for ticker in data['results']:
    #         tickers.append(ticker)
    #         # print(f'\n============================\n{ticker}')
    #     number_of_requests -= 1

    # print(f'\n\nData Count: {len(tickers)}\n\n')
    # my_write_to_csv(example_ticker,"massive_tickers.csv",tickers)
    # more_tickers = get_more_data(next_uniform_resource_locator_two,3)
    more_tickers2 = get_more_data(next_uniform_resource_locator_three,3)

    my_write_to_csv(example_ticker,"massive_tickers4.csv",more_tickers2)


if __name__ == "__main__":
    main()
    