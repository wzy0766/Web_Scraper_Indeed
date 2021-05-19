import requests, collections, html
from bs4 import BeautifulSoup
import pandas as pd

def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'}
    url = f'https://www.indeed.com/jobs?q=software+developer&l=United+States&start={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    divs = soup.find_all('div', class_ = 'jobsearch-SerpJobCard')
    for item in divs:
        title = item.find('a').text.strip()
        company = item.find('span', class_ = 'company').text.strip()
        try:
            salary = item.find('span', class_ = 'salaryText').text.strip()
        except:
            salary = ''
        summary = item.find('div', {'class' : 'summary'}).text.strip().replace('\n', '')
        # frequency check
        desired_skills = ['Python', 'C++', 'Java', 'Node JS', 'HTML', 'CSS', 'React', 'PHP', 'SQL']
        skills = [skill for skill in summary.split()]
        skill_list = []
        for s in skills:
            if s in desired_skills:
                skill_list.append(s)
        # print(skill_list)
        frenquency = {}
        for skill in skill_list:
            if skill in frenquency:
                frenquency[skill] += 1
            else:
                frenquency[skill] = 1
        # print(frenquency)
        job = {
            'title': title,
            'company': company,
            'salary': salary,
            'summary': summary
        }
        joblist.append(job)
    return

joblist = []
for i in range(0, 10, 10):
    print(f'Getting Page,{i}')
    c = extract(i)
    transform(c)
    print(frenquency)

# print(len(joblist))
df = pd.DataFrame(joblist)
print(df.head())
df.to_csv('jobs.csv')