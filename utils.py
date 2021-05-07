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
    fmt - defaults to json. However, csv and xml can also be passed.
    
    """ 
    base_url = 'https://clinicaltrials.gov/api/query/study_fields?'
    
    if not expr:
        expr = f'expr='
    else:
        expr = f"expr={expr.replace(' ', '+')}+AND+"
        
    if not status:
        status = ''
    else:
        status = f"+AND+AREA%5BLocationStatus%5D{status.replace(' ', '+')}"
    
    if study_type == 'Observational' or study_type == 'Interventional':
        study_type = f"%29+AND+AREA%5BStudyType%5D{study_type}+"
    else:
        print("""        This paramater only accepts Observational or Interventional.
        The url will not build if other parameters are entered.
        """)
    
    country = f"SEARCH%5BLocation%5D%28AREA%5BLocationCountry%5D{country.replace(' ', '+')}"

    age = 'AND+AREA%5BMinimumAge%5D18+Years&'
    fields =  "%2C+".join(field_names)
    
    api_url = f'{base_url}{expr}{country}{status}{study_type}{age}fields={fields}&min_rnk={min_rnk}&max_rnk={max_rnk}&fmt={fmt}'

    return api_url
