import requests
import json

def get_site_trial(nctid):

    api_key = 'XXXXXXXXXXXXXXXXXXXX'
    headers = {'x-api-key': api_key}

    v2_base_trials = 'https://clinicaltrialsapi.cancer.gov/api/v2/trials/'
    url = f'{v2_base_trials}{nctid}'
    url

    r = requests.get(url, headers=headers)
    trial = r.json()
    return trial

trial = get_site_trial(nctid)

nct_id = trial['nct_id']
protocol_id = trial['protocol_id']
ctep_id = trial['ctep_id']
official_title = trial['official_title']
brief_summary = trial['brief_summary']
detail_description = trial['detail_description']
print(f'NCT#: {nct_id}\n'
      f'\nProtocolID: {protocol_id}\n'
      f'\nCTEP#: {ctep_id}\n '
      f'\nOfficial Title: {official_title}\n' 
      f'\nSummary: {brief_summary}\n' 
      f'\nDescription: {detail_description}')

structured_eligibility = data['eligibility']['structured']
gender = structured_eligibility['gender']
min_age = structured_eligibility['min_age_in_years']
max_age = structured_eligibility['max_age_in_years']
print(gender, min_age, max_age)


inclusion_criteria = []
exclusion_criteria = []

unstructured_eligibility = trial['eligibility']['unstructured']
for item in unstructured_eligibility:
    if item['inclusion_indicator'] is True:
        inclusion_criteria.append(item['description'])
    elif item['inclusion_indicator'] is False:
        exclusion_criteria.append(item['description'])

if not exclusion_criteria:
    print('Poorly formatted criteria. Consider manual curation.')



def build_url(disease: str,
              keywords: str,
              country: str='United States',
              status: str='Active',
              study_type: str='Treatment',
              
             ) -> str:
    
    base_url = "https://clinicaltrialsapi.cancer.gov/api/v2/trials?"
    
    disease = f"diseases.name._fulltext={disease}&"
    country = f"sites.org_country={country.replace(' ', '%20')}&"
    status = f"current_trial_status={status}&"
    study_type = f"primary_purpose={study_type}&"
    keywords = f"keyword={keywords.replace(' ', '%20')}"
    
    url = f'{base_url}{disease}{country}{status}{study_type}{keywords}'
    return url

build_url(disease='Breast Cancer', keywords='HER-2 Negative')

url = build_url(disease='Breast Cancer', keywords='Triple Negative Breast Cancer')


API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'
HEADERS = {'x-api-key': API_KEY}

r = requests.get(url, headers=HEADERS)
trial = r.json()
n_trials = trial['total']
print(f'{n_trials} trials found.')

trial['data']
