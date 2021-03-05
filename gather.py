import requests
import json
from tqdm import trange


# construct url 
base_url = 'https://clinicaltrials.gov/api/query/study_fields?'
expr = 'expr=Cancer+'
location = 'AND+SEARCH%5BLocation%5D%28AREA%5BLocationCountry%5DUnited+States+'
status = 'AND+AREA%5BLocationStatus%5DRecruiting%29+'
study_type = 'AND+AREA%5BStudyType%5DInterventional+'
age = 'AND+AREA%5BMinimumAge%5D18+Years&'
fields = 'fields=NCTId%2CCondition&'
rank = 'min_rnk=1&max_rnk=&'
fmt = 'fmt=json'

api_call = f'{base_url}{expr}{location}{status}{study_type}{age}{fields}{rank}{fmt}'

def n_studies(url):
    # find number of studies matching api_call
    r = requests.get(api_call)
    text = r.text
    data = json.loads(text)
    n_studies = data['StudyFieldsResponse']['NStudiesFound']
    return n_studies   

def nct_nums():
    # gather NCTID's for all trials: cancer, US, interventional, recruiting
    n_studies = n_studies(api_call)
    print(f'Found {n_studies} studies \n')
    
    if n_studies < 1000:
        r = requests.get(api_call)                                                  
        text = r.text                                                               
        data = json.loads(text)
        for ID in data['StudyFieldsResponse']['StudyFields']:
            ID = ID['NCTId']
                for NCTId in ID:
                    with open(f'nctid.txt', 'a+') as outfile:
                        outfile.write(f'{NCTId},\n')

    else:
        print('Downloading NCT numbers from clinicaltrials.gov.\n This might take a while, coffee break...')
        for i in trange(1, n_studies, 19):
            api_call = f'{base_url}{expr}{location}{status}{study_type}{age}{fields}min_rnk={i}&max_rnk=&{fmt}'
            r = requests.get(api_call)                                                  
            text = r.text                                                               
            data = json.loads(text)
            for ID in data['StudyFieldsResponse']['StudyFields']:
                ID = ID['NCTId']
                for NCTId in ID:
                    with open(f'nctid.txt', 'a+') as outfile:
                        outfile.write(f'{NCTId},\n')
 
if __name__=='__main__':
    nct_nums()
