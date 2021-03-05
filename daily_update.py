import feedparser as fp
import requests


def rss_feed():
    print('Gatering updated NCT trial numbers from clinicaltrials.gov...')
    nctids = []
    
    url = 'https://clinicaltrials.gov/ct2/results/rss.xml?rcv_d=&lup_d=2&sel_rss=mod2&recrs=a&type=Intr&cond=Cancer&cntry=US&count=10000'
    d = fp.parse(url)
    
    for item in d.entries:
        nctid = item.id
        nctids.append(nctid)
    return nctids

def update():
    studies = rss_feed()

    for ID in studies:
        full_study = f'https://clinicaltrials.gov/api/query/full_studies?expr={ID}&min_rnk=1&max_rnk=&fmt=json'
        print(full_study)
        
if __name__ == '__main__':
    update()
