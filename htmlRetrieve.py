#!/usr/bin/python3
import urllib.request
from bs4 import BeautifulSoup
import ast
from requests.exceptions import ConnectionError

def checkEncoding(data):
    #print(type(data))
    if type(data) is not list:
        return convert(data)
    else:
        data = str(data)
    return data


'''
def is_ascii(text):
    if isinstance(text, str):
        try:
            text=text.encode('ascii')
        except UnicodeEncodeError:
            return text
    else:
        try:
            text=text.decode('ascii')
        except UnicodeDecodeError:
            return text
    return text
'''
def convert(data):
    if type(data) is not list:
        if isinstance(data,str):
            return data
        else:
            return data.decode()
    else:
        return str(data)
     
'''
def nameTransformation(filmName):
    name=''
    for char in filmName:
        if char is '(':
            break
        else:
            name=name+char

    size=len(name)-1
    name=name[:size]
    return name

def getInfoFromIMDBpage(name):
    name = nameTransformation(name)
    url="http://www.omdbapi.com/?s="+name+"&apikey=8a848f56"
    response = urllib.request.urlopen(url).read().decode('utf-8')
    movieDict = ast.literal_eval(response)
    movieId = movieDict['Search'][0]['imdbID']
    url='http://www.omdbapi.com/?i='+movieId+'&apikey=8a848f56'
    response = urllib.request.urlopen(url).read().decode('utf-8')
    return response
'''

def getInfoFromIMDBpage(link):
    info = {}
    page = urllib.request.urlopen(link)
    soup = BeautifulSoup(page, 'html.parser')

    for line in soup.find_all("div", {"class": "plot_summary"}):
        counter = 0
        for div in line.find_all("div"):
            if counter == 0: #blurb
                info['Plot'] = div.text.lstrip().rstrip()       
            elif counter == 1: #director
                info['Director'] = div.find("span", {"class": "itemprop"}).text
            elif counter == 2: #writer
                info['Writer'] = div.find("span", {"class": "itemprop"}).text
            elif counter == 3: #stars
                stars=[]
                for span in div.find_all("span", {"class": "itemprop"}):
                    stars.append(span.text)
                info['Stars'] = checkEncoding(stars)
                
            counter = counter+1
    
    g = []
    for line in soup.find_all("div", {"class": "subtext"}):
        for genre in line.find_all("span", {"class": "itemprop"}):
            g.append(genre.text)
        info['Genre'] = checkEncoding(g)

        info['Age_Rating'] = line.find("meta", {"itemprop": "contentRating"}).get('content').lstrip().rstrip()

        #info['ageRating'] = line.find("meta", {"itemprop": "contentRating"}).text
        info['Length'] = line.find("time", {"itemprop": "duration"}).text.lstrip().rstrip()

        
    return info

def generalHtml(link):
    d = getInfoFromIMDBpage(link)
    #print(1)
    html = "<div style=overflow:auto;height:100%;'><h1>General Information</h1>" 

    t = "even"

    for key in d:
        #print(key)
        info = checkEncoding(d[key])
        #print(info)
        html = html+"<section class='"+t+"'><p>"+key+": "+info+"</p></section>"
        if t == "even":
            t = "odd"
        else:
            t = "even"
    #print(2)
    html = html+"</div>"

    return html
    

def getParentalGuideInfo(link):
    link = link+"parentalguide?ref_=tt_ql_stry_5"
    page = urllib.request.urlopen(link)
    soup = BeautifulSoup(page, 'html.parser')
    catagories = ['advisory-nudity','advisory-violence','advisory-frightening','advisory-profanity','advisory-alcohol']
    outer=[]
    for subject in catagories:
        inner=[]
        sub = soup.find('section', attrs={'id' : subject})
        for line in sub.find_all("li", {"class": "ipl-zebra-list__item"}):
            sub = line.text.lstrip().rstrip()
            sub = sub[:len(sub)-17]
            sub=sub.replace('"', '\\"')
            sub=sub.replace('\n', '')
            inner.append(sub)
        outer.append(inner)

    return outer

def htmlParental(link):
    info = getParentalGuideInfo(link)
    catagories = ['Nudity','Violence','Frightening','Profanity','Alcohol']
    html = ""
    counter = 0
    t='even'

    for subject in info:
        if len(subject)>0:
            html=html+"<section class='"+t+"'><h1>"+catagories[counter]+"</h1><ul>"
        
            if t=='even':
                t='odd'
            else:
                t='even'
                
            for fact in subject:
                html=html+'<li>'+fact+'</li>'
            html=html+'</ul></section>'

        counter = counter+1

    return html

def getImages(baseLink):
    #link = link+"mediaindex?ref_=tt_ql_pv_1"
    #page = urllib.request.urlopen(link)
    #soup = BeautifulSoup(page, 'html.parser')
    
    listOfImageSrc = []
    counter = 1
    b=False
    while b == False:
        #print('page '+str(counter))
        link = baseLink+"mediaindex?refine=still_frame&page="+str(counter)
        #print(link)
        page = urllib.request.urlopen(link)
        if not b:
            soup = BeautifulSoup(page, 'html.parser')
            num=0
            for line in soup.find_all("a", {"itemprop": "thumbnailUrl"}):
                num=num+1
                imageSrc = line.find('img').get('src')
                listOfImageSrc.append(imageSrc)
        if num<10:
            b=True

        counter=counter+1

    #print (listOfImageSrc)
    return listOfImageSrc

def htmlImages(link):
    info = getImages(link)
    html = ""

    for imageSrc in info:
        html = html + "<img src='"+imageSrc+"'>"

    return html
    




















