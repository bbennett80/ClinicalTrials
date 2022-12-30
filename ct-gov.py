def query_params(disease: str, 
                 country: str="United States", 
                 trial_status: str="Recruiting", 
                 study_type: str="Interventional"):

    api_endpoint = 'https://clinicaltrials.gov/api/query/study_fields'

    query_params = {
        "expr": f"{disease} SEARCH[Location](AREA[LocationCountry]{country} AND AREA[LocationStatus]{trial_status}) AND AREA[StudyType]{study_type} AND AREA[MinimumAge]18 Years",
        "fields": "NCTId, OfficialTitle, StartDate, Condition, Gender, MaximumAge, EligibilityCriteria, LocationCountry, LocationFacility, LocationCity, LocationState, LocationZip",
        "min_rnk": 1,
        "max_rnk": 999,
        "fmt": "json"
    }

    r = requests.get(api_endpoint, params=query_params, verify=True)
    
    data = r.json()
    trials = data['StudyFieldsResponse']['StudyFields'][0]
    url = r.request.url
    n_studies_found = data['StudyFieldsResponse']['NStudiesFound']
    
    return data, trials, url, n_studies_found
