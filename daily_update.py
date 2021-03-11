import feedparser as fp
import requests

def rss_feed():
    print('Gatering updated NCT trial numbers from clinicaltrials.gov...\n')
    
    url = 'https://clinicaltrials.gov/ct2/results/rss.xml?rcv_d=&lup_d=2&sel_rss=mod2&recrs=a&type=Intr&cond=Cancer&cntry=US&count=10000'
    d = fp.parse(url)
    
    nctids = []

    for item in d.entries:
        nctid = item.id
        nctids.append(nctid)
    return nctids
        
def update_url():
    studies = rss_feed()
    print(f'Found {len(studies)} studies to update.\n')

    for ID in studies:
        base_url = 'https://clinicaltrials.gov/api/query/study_fields?'
        expr = f'expr={ID}&' # change expression to search for disease, device, etc.
        field = 'fields=StudyType%2C+NCTId%2COfficialTitle%2C+StartDate%2C+PrimaryCompletionDate%2C+LastUpdatePostDate%2C+Condition%2C+Gender%2C+MaximumAge%2C+EligibilityCriteria%2C+CentralContactName%2C+CentralContactPhone%2C+CentralContactEMail%2C+LocationFacility%2C+LocationCity%2C+LocationState%2C+LocationZip%2C+LeadSponsorName&'
        fmt_json = 'min_rnk=1&max_rnk=1&fmt=json'
        fmt_csv = 'min_rnk=1&max_rnk=1&fmt=csv'
        
        #choose to return json or csv. TODO: add command line/install prompt. JSON works with MatchaMiner, FYI
        id_json = f'{base_url}{expr}{field}{fmt_json}\n'
        #id_csv = f'{base_url}{expr}{field}{fmt_csv}\n'
        print(id_json)
    return id_json

def main():
    update_url()

if __name__ == '__main__':
    main()
