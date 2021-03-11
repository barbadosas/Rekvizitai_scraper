import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://rekvizitai.vz.lt/imone/maxima_lt_uab/atsiliepimai/' #change url for required company
file_name = 'Maxima_results.csv' #change for different name

def get_pages():

    pages_list = []
    get_url = requests.get(url)
    soup = BeautifulSoup(get_url.content, "html.parser")
    for data in soup.findAll('div', {"class": "pager"}):
        for x in data.findAll('a'):
            pages_list.append(x.text)
    return pages_list[-2]

urls = []
def get_urls(pages):
    for i in range(1, pages):
        urls.append(url + str(i))

def get_name_comment(soup, link):
    name_list = []
    comment_list = []
    date_list = []
    ip_list = []
    link_list = []
    

    for div in soup.find_all("div", {'class':'quote'}): 
        div.decompose() # remove quote divs
     
    for data in soup.findAll('div', {"class": "comment"}):
        for comments in data.findAll('div', {"class": "text"}):
            comments_striped = comments.text.strip()
            comment_list.append(comments_striped)
            link_list.append(link) #count how many links and add them to find comments if needed later
    for data in soup.findAll('div', {"class": "floatLeft"}):
        for name in data.findAll('strong'):
            name_list.append(name.string)

    for data in soup.findAll('a', {"class": "date"}):
        for data_split in data:
            if data_split.startswith('20'):
                date_list.append(data_split)
            if data_split.startswith('IP'):
                splited = data_split.split()
                ip_list.append(splited[1])            
    
    df = pd.DataFrame(list(zip(date_list, ip_list, name_list, comment_list, link_list )))
    df.columns = ["Date", "Ip", "Name", "Comment", "Link"]

    if not os.path.isfile(file_name): # If file exist - headers are not saved, file is appended
        df.to_csv(file_name, mode='a', header=True, index=False, encoding="utf-8-sig")
    else:    # if file exists - headers are not inlucded and file is appended                              
        df.to_csv(file_name, mode='a', header=False, index=False, encoding="utf-8-sig")

def collect_data():
    pages = get_pages()
    get_urls(int(pages))
    for link in urls:
        get_soup = requests.get(link)
        soup = BeautifulSoup(get_soup.content, "html.parser")
        get_name_comment(soup, link)

collect_data()