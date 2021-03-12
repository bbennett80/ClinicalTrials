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
    with open('first_posted.txt', 'w+') as f:
        for trial in nctids_first_posted:
            f.write(f'{trial},\n')

def write_updated_nctids():
    last_update = last_updated()
    with open('last_updated.txt', 'w+') as f:
        for trial in last_update:
            f.write(f'{trial},\n')

if __name__=='__main__':
    write_nctids()
    write_updated_nctids()










