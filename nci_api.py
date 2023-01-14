import requests
from KEYS import API_KEY

NCT_ID = " "
# NCT number/ID as string

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

def get_trial_by_nctid(NCT_ID: str):
    """Uses the trial NCT number to return JSON for study."""
    
    API_ENDPOINT = f"https://clinicaltrialsapi.cancer.gov/api/v2/trials/{NCT_ID}"
    HEADERS = {"Content-Type": "application/json", "x-api-key": API_KEY}

    res = requests.get(API_ENDPOINT, 
                       headers=HEADERS,
                       verify=True
                      )

    if res.status_code != 200:
        raise ValueError("Failed to retrieve trial information. Check trial number.")
    else:
        return res.json()
        

def criteria(trial):
    """Parse trial data in to inclusion/exclusion criteria"""
    
    official_title = trial['official_title']
    brief_summary = trial['brief_summary']
    detail_description = trial['detail_description']
    
    structured_eligibility = trial['eligibility']['structured']
    gender = structured_eligibility['gender']
    min_age = int(structured_eligibility['min_age_in_years'])
    max_age = int(structured_eligibility['max_age_in_years'])

    details = [official_title, brief_summary, detail_description, gender, min_age, max_age]

    inclusion_criteria = []
    exclusion_criteria = []
    

    unstructured_eligibility = trial['eligibility']['unstructured']
    
    for item in unstructured_eligibility:
        if item['inclusion_indicator']: inclusion_criteria.append(item['description'])
        else: exclusion_criteria.append(item['description'])
    
    return details, inclusion_criteria, exclusion_criteria


def print_in_notebook_or_terminal(details, inclusion_criteria, exclusion_criteria):
    print(f'NCT#: {NCT_ID}\n\n'
          f'Official Title: {details[0]}\n\n' 
          f'Summary: {details[1]}\n\n' 
          f'Description: \n{details[2]}\n\n')
    
    print(f'Gender: {details[3]}\n\n'
          f'Mininum Age: {details[4]}\n\n'
          f'Maximum Age: {details[5]}\n\n')
    
    print('***Inclusion criteria:***')
    for i in inclusion_criteria:
          print(f'[ ] {i}\n')

    print('***Exclusion criteria:***')
    for i in exclusion_criteria:
          print(f'[ ] {i}\n')
            
    return
