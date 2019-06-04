import requests
import datetime
import csv
#from bs4 import BeautifulSoup
import simplejson as json
import pprint
import DHT

def getcimisdata(hour):
        #appKey = 'a28ddf14-568e-45b8-8050-6925a8ff77e1'  # cimis appKey
        #appKey = '3cae5dfd-ef01-49e4-b6f4-0441a144c5e5'
        #appKey = '952d594c-ff2e-4011-b1d9-8d62e6300ec8'
        #appKey = 'fe36cc18-4506-4cca-8ba9-c903131fde2f'
        appKey = 'fe36cc18-4506-4cca-8ba9-c903131fde2f'
        # list of CIMIS station ID's from which to query data
        sites = [75]  # uncomment to query single site
        sites = [str(i) for i in sites]  # convert list of ints to strings
        ItemInterval = 'hourly'
        # start date fomat in YYYY-MM-DD
        start = '2019-06-03'
        # end date fomat in YYYY-MM-DD
        # e.g. pull all data from start until today
        end = datetime.datetime.now().strftime("%Y-%m-%d")

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

        #test = requests.head(url)
        #if test.status_code == 302:
        #    print("error 302")
        #else:
        #    print("200")

        print(url)
        r = requests.get(url).json()
        #print(type(r))
        #pprint.pprint(r)

        data = r['Data']
        #print(type(data))
        #pprint.pprint(data)

        providers = data['Providers']
        #now a list and access using providers[int]
        #print(type(providers))
        #pprint.pprint(providers)
        
        access_list = providers[0]
        #print(type(access_list))
        #pprint.pprint(access_list)

        records_list = access_list['Records']
        #print(type(records_list))
        #pprint.pprint(records_list)

        hour_entries = {}

        for i,val in enumerate(records_list):
            hour_entries[i] = val

        #print(type(hour_entries))
        pprint.pprint(hour_entries)
        
        #targ_tmp = hour_entries[0]['HlyAirTmp']['Value']
        #targ_eto = hour_entries[0]['HlyEto']['Value']
        #targ_hum = hour_entries[0]['HlyRelHum']['Value']
        #print(targ_tmp)
        #print(targ_eto)
        #print(targ_hum)
        DHT.cimisTemp = hour_entries[hour]['HlyAirTmp']['Value']
        DHT.cimisET = hour_entries[hour]['HlyEto']['Value']
        DHT.cimisHumidity = hour_entries[hour]['HlyRelHum']['Value']

if __name__ == "__main__":
        #xls_path = 'CIMIS_query_irvine_hourly.xlsx'
        #site_names, cimis_data = main()
        #write_output_file(xls_path, cimis_data, site_names)
        main()
