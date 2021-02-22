# expr query: Cancer AND SEARCH[Location](AREA[LocationCountry]United States AND AREA[LocationStatus]Recruiting) AND AREA[MinimumAge]18 Years AND AREA[StudyType]Interventional

import requests
import json

# construct nctid url 
base_url = 'https://clinicaltrials.gov/api/query/field_values?'
expr = 'expr=Cancer+' # change expression to search for disease, device, etc.
location = 'AND+SEARCH%5BLocation%5D%28AREA%5BLocationCountry%5DUnited+States+' #default set to United States.
status = 'AND+AREA%5BLocationStatus%5DRecruiting%29+'# default to recruiting studies
study_type = 'AND+AREA%5BStudyType%5DInterventional+'# default to interventional studies
age = 'AND+AREA%5BMinimumAge%5D18+Years&' #default adult studies
field = 'field=NCTId&'
fmt = 'fmt=json'# format set to json, available: xml, csv

nctid_api_call = f'{base_url}{expr}{location}{status}{study_type}{age}{field}{fmt}'

def nctids():
    # """gathers NCT ID for all studies in url construct"""
    nctids = requests.get(nctid_api_call).json()
    return nctids

nctid = nctids()

def n_studies(nctid):
    # """returns number of studies which match url construct criteria"""
    n_studies = data['FieldValuesResponse']['NUniqueValuesFound']
    return n_studies

n_studies = n_studies(nctid)

print(f'Found {n_studies} studies \n')


def download_studies(data):
    for ID in data['FieldValuesResponse']['FieldValues']:
        ID = ID['FieldValue']
        full_study = f'https://clinicaltrials.gov/api/query/full_studies?expr={ID}&min_rnk=1&max_rnk=&fmt=json'
        study = requests.get(full_study).json()                                                
        with open(f'{ID}.json', 'w+') as f:
            json.dump(study, f, sort_keys=True, indent=2)



if __name__=='__main__':
    download_studies(data)
