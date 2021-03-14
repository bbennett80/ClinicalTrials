import feedparser as fp
import requests

def last_updated():
    print('Gatering updated NCT trial numbers from clinicaltrials.gov...\n')
    
    url = 'https://clinicaltrials.gov/ct2/results/rss.xml?lup_d=2&sel_rss=mod2&recrs=a&type=Intr&cond=Cancer&cntry=US&count=10000'
    d = fp.parse(url)
    
    updated_nctids = [item.id for item in d.entries]

    return updated_nctids

def first_posted():
    print('Gatering first posted NCT trial numbers from clinicaltrials.gov...\n')

    url = 'https://clinicaltrials.gov/ct2/results/rss.xml?rcv_d=2&sel_rss=mod2&recrs=a&type=Intr&cond=Cancer&cntry=US&count=10000'
    d = fp.parse(url)

    new_nctids = [item.id for item in d.entries]

    return new_nctids

def write_nctids():
    with open('update/first_posted.csv', 'w+', newline='') as f:
        for ID in first_posted():
            f.write(f'{ID},\n')

def write_updated_nctids():
    with open('update/last_updated.csv', 'w+') as f:
        for ID in last_updated():
            f.write(f'{ID},\n')


if __name__=='__main__':
    write_nctids()
    write_updated_nctids()
