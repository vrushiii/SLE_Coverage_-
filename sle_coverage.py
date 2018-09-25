import requests
import urllib3
import math
import os, sys, json
from collections import OrderedDict
from datetime import datetime, timedelta

urllib3.disable_warnings()


# Org id: Production
# ORG_ID = '<add your org id here>'

# API url
API_URL = 'https://api.mist.com/api/v1'

# Prod API Token
# API_TOKEN = '<add your API token here>'

output = {}


class Project(object):
    def __init__(self, token=''):
        self.session = requests.Session()
        self.header = {'Content-Type': 'application/json', 'Authorization': 'Token ' + token}

    # -----method to get all sites id in that ORG-----#
    def get_Sites(self):
        site_id_list = []

        output = {}

        session = self.session
        header = self.header
        url = '{}/orgs/{}/sites'.format(API_URL, ORG_ID)
        response = session.get(url, headers=header)

        if response.status_code != 200:
            print('Failed to GET')
            print('\tResponse: {} ({})'.format(response.text, response.status_code))

        data = json.loads(response.text)


        print('\n')

        #getting site id and site name

        for item in data:
            site_id_list.append(item['id'])
            output[item['id']]= [item['name']]

            print('@@@@@ collecting site ids for site:',item['name'])

        #print('site_id_list:', site_id_list)

        total_sites=len(site_id_list)
        print("\n")

        print("we have total ",total_sites, 'sites')

        print("\n")

        for item in site_id_list:

            print("Calculating coverage % for site id:",item)

            url_2 = '{}/sites/{}/sle/site/{}/metric/coverage/summary?end={}&start={}'.format(API_URL, item, item,
                                                                                    datetime.now,
                                                                                    datetime.now() + timedelta(
                                                                                        days=-(7)))
            response_2 = session.get(url_2, headers=header)

            if response_2.status_code != 200:
                print('Failed to GET')
                print('\tResponse: {} ({})'.format(response_2.text, response_2.status_code))
            data_2 = json.loads(response_2.text)

            sample_values = data_2.get('sle', {}).get("samples")
            degrade_values= sample_values.get("degraded")
            degrade_values_cleaned=filter(None,degrade_values)

            total_values = sample_values.get("total")
            total_values_cleaned = filter(None, total_values)
            dv=sum(degrade_values_cleaned)
            dt=sum(total_values_cleaned)
            #print(dt,dv)

            #calculating % coverage


            if dt != 0:
                coverage_percent=(1 - (dv)/(dt)) * 100
                output[item].append(math.ceil(coverage_percent))
            else:
                output[item].append(0)

        #print (output)

        #zipping site name and coverage

        output_data={}
        output_data = {x[0]:x[1] for x in output.values()}

        # for v in output.values():
        #     for x in v:
        #         output_data[v[0]

        print("\n")

        print("Data for last 7 days: ")

        print("\n")

        #print(output_data)


        sorted_output = [(v,k) for k,v in output_data.items()]

        sorted_output.sort()

        sorted_output.reverse()

        sorted_output = [(k,v) for v,k in sorted_output]


        #final output

        print(sorted_output)

        print("\n")

        for x in sorted_output:
            print (x[0],' ---->> ', x[1])





def main():


    global ORG_ID, API_URL, API_TOKEN,output

    print("\n")

    ORG_ID = str(input("Please enter ORG id: "))
    print("\n")

    API_TOKEN = str(input("Please enter API Token: "))
    print("\n")

    print("Calculating coverage % for last 7 days starting from today")

    print("\n")

    # create object for class 'Project'
    site_object = Project(API_TOKEN)

    # calling the function
    site_object.get_Sites()




main()