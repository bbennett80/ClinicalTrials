def query_params(disease: str) -> str:

    api_endpoint = 'https://clinicaltrials.gov/api/query/study_fields'

    query_params = {
        "expr": f"{disease} SEARCH[Location](AREA[LocationCountry]United States AND AREA[LocationStatus]Recruiting) AND AREA[StudyType]Interventional AND AREA[MinimumAge]18 Years",
        "fields": "NCTId, OfficialTitle, StartDate, Condition, Gender, MaximumAge, EligibilityCriteria, LocationCountry, LocationFacility, LocationCity, LocationState, LocationZip",
        "min_rnk": 1,
        "max_rnk": 999,
        "fmt": "json"
    }

    r = requests.get(api_endpoint, params=query_params, verify=True)
    data = r.json()
    
    return data, r.request.url, data['StudyFieldsResponse']['NStudiesFound']

data, url_string, n_studies_found = query_params("breast adenocarcinoma")
