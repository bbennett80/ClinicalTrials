import csv
import feedparser as fp
import requests

def last_updated():
    print('Gatering updated NCT trial numbers from clinicaltrials.gov...\n')
    
    url = 'https://clinicaltrials.gov/ct2/results/rss.xml?lup_d=2&sel_rss=mod2&recrs=a&type=Intr&cond=Cancer&cntry=US&count=10000'
    d = fp.parse(url)
    
    updated_nctids = []

    for item in d.entries:
        nctid = item.id
        updated_nctids.append(nctid)
    return updated_nctids

def first_posted():
    print('Gatering first posted NCT trial numbers from clinicaltrials.gov...\n')

    url = 'https://clinicaltrials.gov/ct2/results/rss.xml?rcv_d=2&sel_rss=mod2&recrs=a&type=Intr&cond=Cancer&cntry=US&count=10000'
    d = fp.parse(url)

    new_nctids = []

    for item in d.entries:
        nctid = item.id
        new_nctids.append(nctid)
    return new_nctids

def write_nctids():
    nctids_first_posted = first_posted()
    with open('/update/first_posted.csv', 'w+', newline='') as f:
        first = csv.writer(f, delimiter=',')
        first.writerow(nctids_first_posted)

def write_updated_nctids():
    last_update = last_updated()
    with open('/update/last_updated.csv', 'w+', newline='') as f:
        last = csv.writer(f, delimiter=',')
        last.writerow(last_update)

if __name__=='__main__':
    write_nctids()
    write_updated_nctids()
