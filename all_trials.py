import json
import requests
import os

def main():
    folder_setup()
    download_trials()
    

def folder_setup():
    current_directory = os.getcwd()

    studies_directory = os.path.join(current_directory, r'Full_Studies')
    
    if not os.path.exists(studies_directory):
       os.makedirs(studies_directory)


def build_url(expr: str='Cancer',
              country: str='United States',
              status: str='Recruiting',
              study_type: str='Interventional',
              field_names: list=['NCTId','OfficialTitle','StartDate',
                                 'PrimaryCompletionDate','LastUpdatePostDate',
                                 'Condition','Gender','MaximumAge','EligibilityCriteria',
                                 'CentralContactName','CentralContactPhone','CentralContactEMail',
                                 'LocationFacility','LocationCity','LocationState',
                                 'LocationZip','LeadSponsorName'],
              min_rnk: int=1,
              max_rnk: int=1000,
              fmt: str='json'
             ) -> str:
    
    """returns api url for the study fields api on clinicaltrials.gov (https://clinicaltrials.gov/api/gui/demo/simple_study_fields).
    expr -  defaults to Cancer trials. However, any expression one might consider for clinicaltrials.gov.
    country -  defaults to The United States. However, any country can be entered.
    status - defaults to Recruiting. However, the following status can also be passed:
        Not yet recruiting: Participants are not yet being recruited
        Recruiting: Participants are currently being recruited, whether or not any participants have yet been enrolled
        Enrolling by invitation: Participants are being (or will be) selected from a predetermined population
        Active, not recruiting: Study is continuing, meaning participants are receiving an intervention or being examined, but new participants are not currently being recruited or enrolled
        Completed: The study has concluded normally; participants are no longer receiving an intervention or being examined (that is, last participant’s last visit has occurred)
        Suspended: Study halted prematurely but potentially will resume
        Terminated: Study halted prematurely and will not resume; participants are no longer being examined or receiving intervention
        Withdrawn: Study halted prematurely, prior to enrollment of first participant
    study_type -  defaults to Interventional trials. However, Observational can also be passed.
    field_names - a list of data elements and their corresponding API fields as described in the crosswalk documentation. (https://clinicaltrials.gov/api/gui/ref/crosswalks)
    min_rnk = defaults to 1. Can be any interger.
    max_rnk - defaults to 1000 records. Can range from 1 - 1000.
    fmt - defaults to json. However, csv and xml can also be passed.
    
    """
    
    base_url = 'https://clinicaltrials.gov/api/query/study_fields?'
    
    if not expr:
        expr = ''
    else:
        expr = f"{expr.replace(' ', '+')}+AND+"
        
    if not status:
        status = ''
    else:
        status = f"{status.replace(' ', '+')}"
    
    if study_type == 'Observational' or study_type == 'Interventional':
        study_type = study_type
    else:
        print("""        This paramater only accepts Observational or Interventional.
        The url will not build if other parameters are entered.
        """)
    
    country = country.replace(' ', '+')

    age = 'AND+AREA%5BMinimumAge%5D18+Years&'
    fields =  "%2C+".join(field_names)
    
    api_url = f'{base_url}expr={expr}SEARCH%5BLocation%5D%28AREA%5BLocationCountry%5D{country}+AND+AREA%5BLocationStatus%5D{status}%29+AND+AREA%5BStudyType%5D{study_type}+{age}fields={fields}&min_rnk={min_rnk}&max_rnk={max_rnk}&fmt={fmt}'

    return api_url


def full_study_by_nct(trial_number: str):    
    full_study_url = f'https://clinicaltrials.gov/api/query/full_studies?expr={trial_number}&min_rnk=1&max_rnk=&fmt=json'
    
    print(f'Downloading: {trial_number}')
#     print(f'https://clinicaltrials.gov/ct2/show/{trial_number} \n')

    r = requests.get(full_study_url)
    
    if r.status_code != 200:
        print(f'Bad url: {trial_number}')
        
        with open('Full_Studies/http_error.txt', 'a+') as http_error:
            http_error.write(f'Bad url: {trial_number},\n')
            
    elif r.json()['FullStudiesResponse']['NStudiesReturned'] > 1:
        print(f'\n Multiple NCT numbers for https://clinicaltrials.gov/ct2/show/{trial_number} \n')
        
        with open('Full_Studies/trial_error.txt', 'a+') as trial_error:
            trial_error.write(f'Trial number error: https://clinicaltrials.gov/ct2/show/{trial_number},\n')
            
    elif r.json()['FullStudiesResponse']['NStudiesReturned'] == 0:
        print(f'\n No NCT number for https://clinicaltrials.gov/ct2/show/{trial_number} \n')
        
        with open('Full_Studies/trial_error.txt', 'a+') as trial_error:
            trial_error.write(f'Trial number error: https://clinicaltrials.gov/ct2/show/{trial_number},\n')
        
    else:
        full_study = r.json()
        with open(f'Full_Studies/{trial_number}.json', 'w+') as f:
            json.dump(full_study, f, indent=2)
        

def download_trials():
    url = build_url(expr='Cancer', field_names=['NCTId'])

    r = requests.get(url)
    
    if r.status_code != 200:
        print(f'Bad url: {r}')
        with open('Full_Studies/http_error.txt', 'a+') as http_error:
            http_error.write(f'Bad url: {r},\n')
        
    else:
        ID = r.json()
        for item in ID['StudyFieldsResponse']['StudyFields']:
            nctid = ''.join(item['NCTId'])
            full_study_by_nct(nctid)
    
    print('\n-----Trial downloads complete-----\n')

if __name__=='__main__':
    main()
