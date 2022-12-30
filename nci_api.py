import requests
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

def get_trial_information(nct_number: str):
    """Uses GET method to API based on 'NCT#'"""
    
    api_endpoint = f"https://clinicaltrialsapi.cancer.gov/api/v2/trials/{nct_number}"
    
    res = requests.get(
            api_endpoint, 
            headers = {"Content-Type": "application/json", "x-api-key": API_KEY},
            verify=True
        )    
    
    if res.status_code != 200:
        raise ValueError("Failed to retrieve trial information. Check trial number.")
    else:
        return res.json(), res.url


def parse_eligibility_criteria(trial_data):
    """Parse trial data in to inclusion/exclusion criteria"""
    inclusion_criteria = []
    exclusion_criteria = []
    
    structured_criteria = trial_data['structured']
    inclusion_criteria.append(int(structured_criteria['min_age_number']))
    inclusion_criteria.append(int(structured_criteria['max_age_number']))
    inclusion_criteria.append(structured_criteria['gender'])
    
    
    unstructured_criteria = trial_data['unstructured']
    
    for criteria in unstructured_criteria:
        if criteria['inclusion_indicator']:
            inclusion_criteria.append(criteria['description'])
        else:
            exclusion_criteria.append(criteria['description'])

    return inclusion_criteria, exclusion_criteria


if __name__ == "__main__":
    nct_number = "NCT04214262"
    trial, query_url = get_trial_information(nct_number)
    inclusion_criteria, exclusion_criteria = parse_eligibility_criteria(trial['eligibility'])
    print(inclusion_criteria)
    print(exclusion_criteria)
