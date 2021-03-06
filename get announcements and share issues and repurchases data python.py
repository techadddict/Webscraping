##loop through announcements and get information from announcment page for all urls with share issues only

#import libraries / modules
import re
import urllib
import csv
from bs4 import BeautifulSoup
import itertools
import requests
import webbrowser



#define fuctions to extract data

def getNumberAfterWords(word_options,text):

    try:
        result =  re.findall(word_options,text)
        result_2 =' '. join(result)

        return result_2
    except TypeError as e:

            pass
def getNumberBeforeWords(word_options,text):
    try:
            result =  re.findall(word_options,text)
            result_2 ='  '. join(result)
            return result_2
    except TypeError as e:
            result_2=''
            print(e)

            pass
def getRegex(word_options,text):
    try:
            result =  re.findall(word_options,text)
            result_2 ='  '. join(result)
            return result_2
    except TypeError as e:
            result_2=''
            print(e)

            pass

#get base url/link
announcements_links=[]
base_url="here"


pages = list(map(str,range(1,60)))
#get all links with the actual announcements
for n in pages:
    url = base_url + n
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    for link in soup("a", "annmt", href=True):
        web_link=link['href']
        announcements_links.append(web_link)


#get only urls for Issue of Equity
urls_final_issues=[]
for i in announcements_links:
    if('issue-of-equity' in i ):
       urls_final_issues.append(i)


data_final=[]
for u in urls_final_issues:
    url_d=base_url+str(u)
    req = urllib.request.Request(url_d, headers={'User-Agent' : "Magic Browser"})
    con_d = urllib.request.urlopen( req )
    soup_2 = BeautifulSoup(con_d, 'html.parser')

    #if data is stored in a paragraph
    #get dates
    date= soup_2.find('h4', {'class':"headLine"}).text
    #get company names
    company= soup_2.find('h3').text
    #get paragraph with details
    details_normalparagraph = soup_2.find('div', {'class':"KonaBody"}).find_all('p')

    article_text2 = soup_2.find('tr').text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').strip()

    #format paragraph with details so that it fits in a csv cell
    article_text=''
    for element in details_normalparagraph:
       article_text +=  ''.join(element.find_all(text = True))
       article_text=article_text.replace("\t", "").replace("\r", "").replace("\n", "")
    #this section ensures that announcements with data stored in table is picked up, one has to read the text to get the statistics through

    #get sentence with shares issued/alloted
    alloted_shares_sent=[sentence + '.' for sentence in article_text.split('.') if 'allotment and issue' in sentence or 'were allotted' in sentence or 'an allotment' in sentence or 'issued and allotted' in sentence or 'allotted and issued' in sentence or 'allotted' in sentence or 'Allotted' in sentence or 'allotted,' in sentence or 'Allotted,' in sentence or 'allotments of' in sentence or 'allotment of' in sentence or 'allotment and' in sentence or 'allotment on' in sentence or 'Allotment of' in sentence or 'allotment of,' in sentence or 'Allotment of,' in sentence or 'price' in sentence or 'announces' in sentence or 'announce' in sentence or 'allotted and issued,' in sentence or 'allotted and issued' in sentence  or 'further' in sentence]# get sentence with prices
    price_sent=[sentence + '.' for sentence in article_text.split(',') if 'price' in sentence or 'Scheme' in sentence or 'Net Asset' in sentence or 'ranged' in sentence or 'NAV' in sentence  or 'net asset value' in sentence or  'range' in sentence or 'issued at' in sentence or 'announces'in sentence ]    # get sentence with total voting rights
    voting_rights_sent=  [sentence + '.' for sentence in article_text.split('.') if 'voting rights' in sentence or 'Voting rights' in sentence]

     #filter out sentence with total share capital or total issued shares
    total_issued_shares_sent=[sentence + '.' for sentence in article_text.split('.') if 'capital' in sentence or 'in issue' in sentence or 'circulation' in sentence or 'Following' in sentence]
    #get prices
    treasury_shares_sent=[sentence + '.' for sentence in article_text.split('.') if 'treasury' in sentence or 'Treasury' in sentence or 'treasury.' in sentence or 'Treasury.' in sentence or 'Treasury.F' in sentence or  'treasury.F' in sentence or 'Treasury.T' in sentence  or 'treasury.T' in sentence or 'treasury,' in sentence or 'Treasury,' in sentence ]


    #turn lists into text again so that we can use regex functions
    prices=' '.join(price_sent)
    shares_alloted=' '.join(alloted_shares_sent)
    voting_rights=' '.join(voting_rights_sent)
    total_issued_shares=' '.join(total_issued_shares_sent)
    treasury_shares=' '.join(treasury_shares_sent)
    voting_rights=''.join(voting_rights_sent)

    #list of words to look for when using regex
    price_words=  r'(\d+.?\d\d*)(?:p per | p per| per| pence|p to|p|p,|p to |p and| pence to| pence and|per|p each)'
    shares_alloted_words =r'\s*[0-9,.]* (?:[A-Z ]*Ordinary|Venture|venture|[A-Z ]*ordinary|[A-Z ]*share|[A-Z ]*Share|new|New|new Ordinary|New Ordinary|new ordinary|New ordinary|Generalist|Healthcare|venture|Venture)\s*'
    treasury_shares_words =r'\s*[0-9,.]* (?:[A-Z ]*Ordinary|[A-Z ]*ordinary|[A-Z ]*shares|[A-Z ]*Shares)\s*'
    shares_issued=r'\s*[0-9,.]* (?:[A-Z ]*Ordinary|[A-Z ]*ordinary|[A-Z ]*shares|[A-Z ]*Shares)\s*'
    votingRights_words=r'[0-9,]+'

        #write data to CSV file
    csvfile = path_to_where_file_should_be_saved
    with open(csvfile, "a") as shareissuesData:
         wr = csv.writer(shareissuesData, dialect='excel')
         wr.writerow([date,company,getNumberBeforeWords(shares_alloted_words,shares_alloted),getNumberBeforeWords(price_words,prices),getNumberBeforeWords(shares_issued,total_issued_shares),getNumberBeforeWords(treasury_shares_words,treasury_shares),getRegex(votingRights_words,voting_rights),url_d, article_text,article_text2])
