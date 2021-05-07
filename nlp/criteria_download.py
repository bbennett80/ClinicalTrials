import json
import requests
import csv
from glob import glob
import pandas as pd
from pathlib import Path
from tqdm import trange

def main():
    folder_setup()
    download_trials()
    write_txt()

def folder_setup():
    """Makes directory 'Full_Studies' to which trial files are downloaded."""
    current_directory = Path.cwd()
    
    global studies_directory    
    studies_directory = current_directory / r'Full_Studies_test'

    not_available = studies_directory / r'log.txt'

    criteria_file = studies_directory / r'criteria.txt'

    if not Path.exists(studies_directory):
       Path.mkdir(studies_directory)

    if not Path.exists(not_available):
        pass
    else:
        Path.unlink(not_available)

    if not Path.exists(criteria_file):
        pass
    else:
        Path.unlink(criteria_file)


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
              max_rnk: int=999,
              fmt: str='csv'
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
    fmt - defaults to csv. However, json and xml can also be passed.
    
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


def generate_urls():
    """Gathers clinical trials from clinicaltrials.gov for search term
       defined in build_url() function and downloads to specified file format.
    """
    urls = []
    
    api_call = build_url(expr='Cancer', max_rnk=1, fmt='json')
    r = requests.get(api_call)
    data = r.json()
    n_studies = data['StudyFieldsResponse']['NStudiesFound']
    print(f'{n_studies} studies found.\n')
    print('\nGenerating request urls...')

    for i in range(1, n_studies, 1000):

        url = build_url(expr='Cancer', field_names=['EligibilityCriteria'],
                        min_rnk=f'{i}', max_rnk=f'{i+999}',
                        fmt='csv')
        
        urls.append(url)
    
    return urls



def download_trials():
    urls = generate_urls()
    
    print('\n-----Downloading trials-----\n')
    
    for url, i in zip(urls, trange(1, len(urls))):
        df = pd.read_csv(url, skiprows=9)
        df = df.drop(columns='Rank')
        df.to_csv(f'{studies_directory}/trial_set_{i}.csv', index=False)

    print('\n-----Downloads complete-----\n')

def write_txt():
    all_files = glob(f'{studies_directory}/*.csv')

    for file in all_files:
        data = []
        print(f'Working on file {file}')
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for criteria in reader:
                c = criteria['EligibilityCriteria']
                c = c.replace('Inclusion Criteria:||', '')
                c = c.split('|')
                for i in c:
                    data.append(f'\n{i}')
        with open(f'{studies_directory}/criteria.txt', 'a+', encoding='utf-8', errors='ignore') as f:
            for item in data:
                f.write(item)  

    print('\n-----Process complete-----')
            
if __name__=='__main__':
    main()
