import glob
import json
import os
import pandas as pd
import requests
from tqdm import trange

trial_type = 'Interventional'

def build_url():
    # construct nctid url 
    base_url = 'https://clinicaltrials.gov/api/query/study_fields?'
    expr = 'expr=Cancer+' # change expression to search for disease, device, etc.
    location = 'AND+SEARCH%5BLocation%5D%28AREA%5BLocationCountry%5DUnited+States+' #default set to United States.
    status = 'AND+AREA%5BLocationStatus%5DRecruiting%29+'# default to recruiting studies
    study_type = f'AND+AREA%5BStudyType%5D{trial_type}+'# default to interventional studies
    age = 'AND+AREA%5BMinimumAge%5D18+Years&' #default adult studies
    field = 'fields=StudyType%2C+NCTId%2COfficialTitle%2C+StartDate%2C+PrimaryCompletionDate%2C+LastUpdatePostDate%2C+Condition%2C+Gender%2C+MaximumAge%2C+EligibilityCriteria%2C+CentralContactName%2C+CentralContactPhone%2C+CentralContactEMail%2C+LocationFacility%2C+LocationCity%2C+LocationState%2C+LocationZip%2C+LeadSponsorName&'
    fmt_json = 'min_rnk=1&max_rnk=&fmt=json'
    fmt_csv = 'min_rnk=1&max_rnk=1000&fmt=csv'

    api_json = f'{base_url}{expr}{location}{status}{study_type}{age}{field}{fmt_json}'
    api_csv = f'{base_url}{expr}{location}{status}{study_type}{age}{field}{fmt_csv}'
    return api_json, api_csv

api_json = build_url()[0]
api_csv = build_url()[1]

def studies(json_url, csv_url):
    r = requests.get(api_json)
    data = json.loads(r.text)
    n_studies = data['StudyFieldsResponse']['NStudiesFound']
    print(f'There were {n_studies} studies found.')

    if n_studies < 1000:
        df = pd.read_csv(api_csv, skiprows=9)
        return df.to_csv(f'{trial_type}_clinical_trials.csv', index=False)
    else:        
        for trial in trange(1, 100, 19):
            urls = f'https://clinicaltrials.gov/api/query/study_fields?expr=cancer+AND+SEARCH%5BLocation%5D%28AREA%5BLocationCountry%5DUnited+States+AND+AREA%5BLocationStatus%5DRecruiting%29+AND+AREA%5BMinimumAge%5D18+Years+AND+AREA%5BStudyType%5DObservational&fields=StudyType%2C+NCTId%2COfficialTitle%2C+StartDate%2C+PrimaryCompletionDate%2C+LastUpdatePostDate%2C+Condition%2C+Gender%2C+MaximumAge%2C+EligibilityCriteria%2C+CentralContactName%2C+CentralContactPhone%2C+CentralContactEMail%2C+LocationFacility%2C+LocationCity%2C+LocationState%2C+LocationZip%2C+LeadSponsorName&min_rnk={trial}&max_rnk=&fmt=csv'
            df = pd.read_csv(urls, skiprows=9)
            df = df.drop(columns=['Rank', 'StudyType'])
            dfs = df.to_csv(f'{trial_type}_clinical_trials_{trial}.csv', index=False)
    
    all_files = glob.glob(f'{trial_type}_clinical_trials_*.csv')
    df = pd.concat((pd.read_csv(f) for f in all_files))
    df = df.sort_values(by='NCTId', ascending=True)
    return df.to_csv(f'{trial_type}_clinical_trials.csv', index=False)

def clean_up():

    all_files = glob.glob(f'./{trial_type}_clinical_trials_*.csv', recursive=True)
    if not all_files:
        print('Files cleaned up. Trials downloaded.')
    else:
        for file_batch in all_files:
            print(f'Cleaning up files: {file_batch}')
        try:
            for files in all_files:
                os.remove(files)
        except OSError as e:
            print(f'Error: {file_path} : {e.strerror}')
            
def map_zipcode():
    df_ct = pd.read_csv('Interventional_clinical_trials.csv', dtype='object')
    df_zipcodes = pd.read_csv('zipcodes.csv', dtype='object')

    df_ct.LocationZip = df_ct.LocationZip.str.split('|')
    df_ct = df_ct.explode('LocationZip')
    df_ct['LocationZip'] = df_ct['LocationZip'].str[:5]

    df = pd.merge(df_ct, df_zipcodes, how='left', on='LocationZip')
    return df.to_csv('clinical_trials_db.csv', index=False)

def main():
    studies(api_json, api_csv)
    clean_up()
    map_zipcode()
    
if __name__=='__main__':
    main()         
