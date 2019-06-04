import requests
import datetime
import csv
#from bs4 import BeautifulSoup
import simplejson as json
import pprint
#from cimis import run_cimis, retrieve_cimis_station_info, write_output_file

def main():
        appKey = 'a28ddf14-568e-45b8-8050-6925a8ff77e1'  # cimis appKey
        # list of CIMIS station ID's from which to query data
        sites = [75]  # uncomment to query single site
        sites = [str(i) for i in sites]  # convert list of ints to strings
        ItemInterval = 'hourly'
        # start date fomat in YYYY-MM-DD
        start = '2019-06-03'
        # end date fomat in YYYY-MM-DD
        # e.g. pull all data from start until today
        end = datetime.datetime.now().strftime("%Y-%m-%d")
        # pull daily data; other options are 'hourly' and 'default'
        # edit convert_data_items function to customize list of queried parameters
        #station_info = retrieve_cimis_station_info()
        #pulled_site_names = [station_info[x] for x in sites]
        # retrieve the data for each station and place into a list of dataframes
        #df = run_cimis(appKey, sites, start, end, ItemInterval)
        #return pulled_site_names, df

        station = sites[0]
        dataItems_list = ['hly-air-tmp',
                          'hly-eto',
                          'hly-asce-eto',
                          'hly-asce-etr',
                          'hly-precip',
                          'hly-rel-hum',
                          'hly-res-wind']
        dataItems = ','.join(dataItems_list)
        url = ('http://et.water.ca.gov/api/data?appKey=' + appKey + '&targets='
            + str(station) + '&startDate=' + start + '&endDate=' + end +
            '&dataItems=' + dataItems +'&unitOfMeasure=E')
        #r = requests.get(url)
        r = requests.head(url)
        if r.status_code == 302:
            print("error 302")
        #print(url)
        #raw = r.json()
        #print(type(raw))

        #data = raw['Data']
        #print(type(data))
        #pprint.pprint(data)

        #providers = data['Providers']
        #now a list and access using providers[int]
        #print(type(providers))
        #pprint.pprint(providers)
        
        #access_list = providers[0]
        #print(type(access_list))
        #pprint.pprint(access_list)

        #records_list = access_list['Records']
        #print(type(records_list))
        #pprint.pprint(records_list)

        #print(soup.prettify())

if __name__ == "__main__":
        #xls_path = 'CIMIS_query_irvine_hourly.xlsx'
        #site_names, cimis_data = main()
        #write_output_file(xls_path, cimis_data, site_names)
        main()
