import requests
import json

nct_list = []

def read_nctids():
    #reads in NCT IDs to list
    with open('nctid.txt', 'r') as f:
        for IDs in f.readlines():
            ID = IDs.strip().replace(',', '')
            nct_list.append(ID)


def download_studies():
    #downloads and saves NCT ID study
    for ID in nct_list:
        full_study_url = f'https://clinicaltrials.gov/api/query/full_studies?expr={ID}&min_rnk=1&max_rnk=&fmt=json'
        r = requests.get(full_study_url)
        text = r.text
        data = json.loads(text)
        print(f'Saving study {ID}')
        with open(f'{ID}.json', 'w+') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=2)


if __name__=='__main__':
    read_nctids()
    download_studies()
