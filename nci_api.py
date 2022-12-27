import requests
import json
from pprint import pprint
from KEYS import API_KEY

def disease_query(disease_keyword: str):
    """A query to be passed to the request function. 
    'disease_keywords' are passed to a list of strings.
    'query_params' are passed as a json request."""
    
    query_params = {
        "trial_status": "OPEN",
        "diseases.name": disease_keyword,
        "include": [
            "nct_id",
            "sites.trial_status",
            "diseases.name",
            "diseases.is_lead_disease",
            "study_protocol_type",
            "current_trial_status",
            "sites.recruitment_status",
            "current_trial_status_date",
            "brief_summary",
            "anatomic_sites",
            "eligibility",
            "arms",
            "biomarkers",
            "phase",
            "minimum_target_accrual_number",
            "prior_therapy",
            "associated_studies",
            "sites",
            "diseases",
          ],
        "sites.org_country":"United States",
        "order": "asc",
        "sort": "nct_id"
        }
    
    return query_params

def get_trial(nct_number: str):
    """Uses GET method to API based on 'NCT#'"""
    
    api_endpoint = f"https://clinicaltrialsapi.cancer.gov/api/v2/trials/{nct_number}"
    
    res = requests.get(
            api_endpoint, 
            headers = {"Content-Type": "application/json", "x-api-key": API_KEY},
            verify=True
        )    
    
    #TODO add error handling
    if res.ok:
        return res.json(), res.url
    else:
        return res.raise_for_status(), res.url

nct_number = "NCT04214262"
trial, query_url = get_trial(nct_number)

trial['eligibility']

brief_summary = trial["brief_summary"]
print(brief_summary)
print("-----")


structured_eligibility = trial['eligibility']['structured']
gender = structured_eligibility['gender']
min_age = structured_eligibility['min_age_in_years']
max_age = structured_eligibility['max_age_in_years']
print(f'\nGender: {gender}\n'
      f'\nMininum Age: {min_age}\n'
      f'\nMaximum Age: {max_age}\n')


inclusion_criteria = []
exclusion_criteria = []

unstructured_eligibility = trial['eligibility']['unstructured']
print(unstructured_eligibility)

for item in unstructured_eligibility:
    if item['inclusion_indicator'] is True:
        inclusion_criteria.append(item['description'])
    elif item['inclusion_indicator'] is False:
        exclusion_criteria.append(item['description'])
        
