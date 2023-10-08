import os
import re
from time import sleep
import requests
from bs4 import BeautifulSoup
from lxml import etree 


URL = "https://fitgirl-repacks.site/all-my-repacks-a-z/?lcp_page0="
dataGame=""

def getTotalPage():
    while True:
        try:
            response=requests.get(URL+"1",timeout=10)
            if response.status_code!=200:
                print("Stuck in getTotalPage, Error:"+str(response.status_code))
                sleep(20)
                continue
            soup=BeautifulSoup(response.text,"html.parser")
            a=soup.findAll("a",title=re.compile("$"))
            #print(a)
            return int(a[-2].text)

        except Exception as e:
            print(e)


def scrapeMainPage(page):
    done=False
    while not done:
        try:
            response=requests.get(URL+page,timeout=10)
            if response.status_code!=200:
                print("Stuck in main page "+page)
                sleep(20)
                continue
            soup=BeautifulSoup(response.text,"html.parser")
            allA=soup.findAll("a") #good are in [11:61] except in the final page
            currentA=11
            goodA=[]
            while True:
                if "Previous Page" in allA[currentA].text or "2"==allA[currentA].text:
                    break
                goodA.append(allA[currentA])
                currentA+=1
            #print(goodA)
            games=[]
            for tag in goodA:
                scrapeGamePage(tag["href"])
                if dataGame==None:
                    print("Tag: "+str(tag["href"]))
                    print(dataGame)
                    raise Exception("Value returned not expected, value: "+str(dataGame))
                games.append(dataGame)
            
            g=open("games_data.txt","a",encoding="utf-8")
            g.writelines(games)
            g.close()
            f=open("backup_mainpage.txt","w",encoding="utf-8")
            f.write(str(int(page)+1))
            f.close()
            done=True

        except Exception as e:
            print(e)
            print(page)
            print("Exception, try again in 100 sec")
            sleep(100)


def scrapeGamePage(href):
    done=False

    if "cod-black-ops-3-repack-status" in href:
        #avoid the link https://fitgirl-repacks.site/cod-black-ops-3-repack-status/
        return
    if "winter-is-coming" in href:
        #blank page
        return

    if "diablo-2-resurrected-pc" in href:
        #they redirect to another URL
        href="https://fitgirl-repacks.site/diablo-ii-resurrected-pc/"

    skipCompanies=False
    if "mother-russia-bleeds" in href:
        #There is "Companies" field but no value
        skipCompanies=True

    skipGenres=False
    if "sleeping-dogs" in href:
        #There is "Genres" field but no value
        skipGenres=True


    while not done:
        sleep(0)
        try:
            response=requests.get(href,timeout=10)
            if response.status_code!=200:
                print("Stuck in "+href+" Error:"+str(response.status_code))
                sleep(20)
                continue
            g=open("pages/"+href.split("/")[-2]+".html","w",encoding="utf-8")
            g.write(response.text)
            g.close()

            soup=BeautifulSoup(response.text,"html.parser")
            dom = etree.HTML(str(soup))

            #Selector created to manage: Red text inside "Repack Features"; Background image on game page; Less info on game page; Without 1337x link; Different type of magnet URL

            title=dom.xpath("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/article[1]/header[1]/h1[1]")[0].text.replace(","," ")
            print(title)
            dateUpload=dom.xpath("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/article[1]/header[1]/div[2]/span[1]/a[1]/time[1]")[0].text.replace(",","")
            print(dateUpload)
            try:
                commentsNumber=dom.xpath("//*[contains(text(),'Comments')]")[0].text.replace(" Comments","")
            except:
                commentsNumber="NULL"
            print(commentsNumber)

            strongNumber=1
            if not skipGenres:
                genresPresence=dom.xpath("//*[contains(text(),'Genres')]")
                if len(genresPresence)>0:
                    genresPresence=True
                else:
                    genresPresence=False
                
                print(genresPresence)
                if genresPresence:
                    try:
                        genres=dom.xpath("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/article[1]/div[1]/p[1]/strong["+str(strongNumber)+"]")[0]
                    except:
                        genres=dom.xpath("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/article[1]/div[1]/div[1]/p[1]/strong["+str(strongNumber)+"]")[0]
                    if genres.text!=None:
                        genres=genres.text.replace(",",";").replace(" ","")
                        genres="["+genres+"]"
                    else:
                        genres="NULL"
                    strongNumber+=1
                else:
                    genres="NULL"
            else:
                genres="NULL"
            print(genres)

            if not skipCompanies:
                try:
                    companies=dom.xpath("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/article[1]/div[1]/p[1]/strong["+str(strongNumber)+"]")[0]
                except:
                    companies=dom.xpath("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/article[1]/div[1]/div[1]/p[1]/strong["+str(strongNumber)+"]")[0]
                if companies.text!=None:
                    companies=companies.text.replace(",",";").replace(" ","")
                    companies="["+companies+"]"
                else:
                    companies="NULL"
                strongNumber+=1
            else:
                companies="NULL"
            print(companies)

            try:
                languages=dom.xpath("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/article[1]/div[1]/p[1]/strong["+str(strongNumber)+"]")[0]
            except:
                languages=dom.xpath("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/article[1]/div[1]/div[1]/p[1]/strong["+str(strongNumber)+"]")[0]
            languages=languages.text
            strongNumber+=1
            print(languages)

            try:
                skipRedElement=dom.xpath("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/article[1]/div[1]/p[1]/strong["+str(strongNumber)+"]")[0].text
            except:
                skipRedElement=dom.xpath("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/article[1]/div[1]/div[1]/p[1]/strong["+str(strongNumber)+"]")[0].text
            if skipRedElement==None or "indows" in skipRedElement or "controller" in skipRedElement or "game" in skipRedElement:
                strongNumber+=1
                print("Red element on "+href)
            
            try:
                originalSize=dom.xpath("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/article[1]/div[1]/p[1]/strong["+str(strongNumber)+"]")[0].text
                if "Windows" in originalSize:
                    strongNumber+=1
                    originalSize=dom.xpath("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/article[1]/div[1]/p[1]/strong["+str(strongNumber)+"]")[0].text
            except:
                originalSize=dom.xpath("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/article[1]/div[1]/div[1]/p[1]/strong["+str(strongNumber)+"]")[0].text
            originalSize=originalSize.replace(",",".")
            strongNumber+=1
            print(originalSize)
            try:
                repackSize=dom.xpath("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/article[1]/div[1]/p[1]/strong["+str(strongNumber)+"]")[0].text
            except:
                repackSize=dom.xpath("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/article[1]/div[1]/div[1]/p[1]/strong["+str(strongNumber)+"]")[0].text
            if repackSize==None:
                repackSize="NULL"
            else:
                repackSize=repackSize.replace(",",".")
            print(repackSize)

            try:
                link1337x=dom.xpath("//a[contains(text(),'1337x')]/@href")[0].text
            except:
                link1337x="NULL"
            print(link1337x)
            try:
                magnet=dom.xpath("//a[contains(text(),'Magnet') or contains(text(),'magnet')]/@href")[0].text
            except:
                magnet="NULL"
            print(magnet)
            try:
                statsTorrentUrl=dom.xpath("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/article[1]/div[1]/ul[1]/li[1]/img[1]/@src")[0].text
            except:
                statsTorrentUrl="NULL"
            print(statsTorrentUrl)
            

            repackFeaturesArray=dom.xpath("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/article[1]/div[1]/ul[2]/li") #normal position
            if len(repackFeaturesArray)==0 or repackFeaturesArray[0].text==None:
                repackFeaturesArray=dom.xpath("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/article[1]/div[1]/div[1]/ul[2]/li") #with background photo
            if len(repackFeaturesArray)==0 or repackFeaturesArray[0].text==None:
                repackFeaturesArray=dom.xpath("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/article[1]/div[1]/ul[3]/li") #solution for assassins-creed-odyssey (there is another list before, ul[3])
            if len(repackFeaturesArray)>0:
                repackFeatures="["
                for element in repackFeaturesArray:
                    if element.text==None: #Skipping text with <b> tag
                        continue
                    phrase=element.text.replace(","," ").replace("\n","")
                    print(phrase)
                    repackFeatures+=phrase+";"
                repackFeatures=repackFeatures[:-1]+"]"
            else:
                repackFeatures="NULL"
            
            data=title+","+href+","+dateUpload+","+commentsNumber+","+genres+","+companies+","+languages+","+originalSize+","+repackSize+","+link1337x+","+magnet+","+statsTorrentUrl+","+repackFeatures+"\n"
            global dataGame
            dataGame=data
            done=True
            
        except Exception as e:
            print(e)
            print("Exception, try again in 100 sec: "+href)
            sleep(100)










try:
    f=open("backup_mainpage.txt","r",encoding="utf-8")
    i=int(f.readline())
    f.close()
except:
    f=open("backup_mainpage.txt","w",encoding="utf-8")
    f.write("1")
    f.close()
    i=1

if not os.path.exists("games_data.txt"):
    g=open("games_data.txt","a",encoding="utf-8")
    g.write("title,link,date upload,number of comment,genres,companies,languages,original size,repack size,link1337x,magnet,statsTorrentUrl,repack features\n")
    g.close()


totalPage=getTotalPage()
print("Start from page "+str(i)+" up to the page "+str(totalPage))

while i<=totalPage:
    scrapeMainPage(str(i))
    i+=1





