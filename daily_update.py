import feedparser as fp
import requests
import pandas as pd
import json

def main():
    download_trials()


def rss_feed():
    print('Gatering updated NCT trial numbers from clinicaltrials.gov...\n')
    
    url = 'https://clinicaltrials.gov/ct2/results/rss.xml?rcv_d=&lup_d=2&sel_rss=mod2&recrs=a&type=Intr&cond=Cancer&cntry=US&count=10000'
    d = fp.parse(url)
    
    nctids = [item.id for item in d.entries]
    print(f'Found {len(nctids)} studies to update.\n')
    
    rss_items = []
    
    for ID in nctids:
        base_url = 'https://clinicaltrials.gov/api/query/study_fields?'
        expr = f'expr={ID}&'
        field = 'fields=StudyType%2C+NCTId%2COfficialTitle%2C+StartDate%2C+PrimaryCompletionDate%2C+LastUpdatePostDate%2C+Condition%2C+Gender%2C+MaximumAge%2C+EligibilityCriteria%2C+CentralContactName%2C+CentralContactPhone%2C+CentralContactEMail%2C+LocationFacility%2C+LocationCity%2C+LocationState%2C+LocationZip%2C+LeadSponsorName&'
        fmt_json = 'min_rnk=1&max_rnk=1&fmt=json'
        #fmt_csv = 'min_rnk=1&max_rnk=1&fmt=csv'
        url = f'{base_url}{expr}{field}{fmt_json}'
        study = ID, url
        rss_items.append(study)
        
    return rss_items


def download_trials():
    rss_items = rss_feed()
    print('\nDownloading: ')
    
    for ID, URL in rss_items:
        r = requests.get(URL).json()
        raw_json = r['StudyFieldsResponse']['StudyFields'][0]
        print(f'{ID}')
        with open(f'{ID}.json', 'w+') as f:
            json.dump(raw_json, f, indent=2)

if __name__ == '__main__':
    main()
