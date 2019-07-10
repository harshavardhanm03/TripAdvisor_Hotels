# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 01:35:49 2019

@author: harsh
"""
import scrapy
import requests
import time
from bs4 import BeautifulSoup
import random
import sys
import pandas as pd
from fake_useragent import UserAgent
import json
import csv

url='https://www.tripadvisor.com'
base_url='/'+'Hotels-g60745-Boston_Massachusetts-Hotels.html'
timeDelay=random.randrange(0,20)
ua=UserAgent()


#"Date","CityID","HotelID","ReviewID","ReviewTitle","ReviewText","NonEng","RatingDate","StayTime",
#"AvgRatingStarsThisUser","Value","Location","SleepQuality","Rooms","Cleanliness","Service",
#"NumHelpful","UserID","UserSumPage","UserFullProfile","UserLocation","TotalReviewsUser",
#"HotelRevUser","RevInCitiesUser","HelpfulVotesUser",,"MemberSince","Contributions",#
#"PageUrl"

def main():
    ip=get_proxy()
    all_pages=pages(url,base_url,ip)
    Hotel_PageUrl=hotels(all_pages,ip)
    hotel_details=Details(Hotel_PageUrl)




#proxy rotator to prevent blocking
def get_proxy():
    working_proxy=[]
    try:
        working_proxy=[]
        keys=['xG2M5BHQpLafkdrb6eum4oSJZgXCyPKc','zeygcLPASh8KvG7TJxfB9ZE6bukU4FNV','sDtpJfvTLu9Szqmkw52QjZehVWCEGydM']
        for key in keys:
            for i in range(0,50):
                proxy_rotator_url="http://falcon.proxyrotator.com:51337/"
                params = dict(
                    apiKey=key
                )
                resp = requests.get(url=proxy_rotator_url, params=params)
                print(resp)
                data = json.loads(resp.text)
                print(data)
                working_proxy.append(data['ip'] + ":" + data['port'])            
    except:
        print("all ips fecthed")
    return working_proxy


#"CitiesVisited","NumExcellent","NumVeryGood","NumAverage","NumPoor","NumTerrible",
#"Gender","Age",UserTitle"
    
#Scraping all the pages from the main page
def pages(url,base_url,ip):
    pages_list=[url+base_url]
    proxy=random.choice(ip)
    print(proxy)
    proxies={
            'http': f'http://{proxy}',
            'https':f'http://{proxy}',
             }
    print(proxies)
    try:
        page=requests.get(pages_list[0],headers={'User-Agent':ua.random})
        time.sleep(timeDelay)
        while(page.status_code!=200):
            ip.remove(proxy)
            proxy=random.choice(ip)                
            page=requests.get(pages_list[0],headers={'User-Agent':ua.random})
            time.sleep(timeDelay)
        soup = BeautifulSoup(page.text, 'html.parser')
        page_numbers=soup.find(class_='pageNumbers')
        page_info=page_numbers.find_all('a')
        for i in range(0,len(page_info)):
            page_urls=url+page_info[i]['href']
            print("fecthing page",page_urls)
            pages_list.append(page_urls)
    except:
        print("all ips have been expired")
    return pages_list


#Scraping all the HotelName,HotelId,CityID,AreaID,       
def  hotels(all_pages,ip):
    try:
        Hotels_URLS=[]
        if(len(all_pages)<1):
            print("Not able to fetch any pages..Exiting program")
            print("Pages:{}".format(all_pages))
            sys.exit()
        else:
            #print("feteched all pages")
            count=0
            
        for i in range(0,len(all_pages)):
            proxy=random.choice(ip)
            proxies={
            'http': f'http://{proxy}',
            'https':f'http://{proxy}',
            }
            print(proxies)
            #print(all_pages[i])
            #time.sleep(timeDelay)
            page=requests.get(all_pages[i],headers={'User-Agent':ua.random})
            print(page.status_code)
            while(page.status_code!=200):
                print("enetered the while loop")
                ip.remove(proxy)
                proxy=random.choice(ip)                
                page=requests.get(all_pages[i],headers={'User-Agent':ua.random},proxies=proxies)
                #time.sleep(timeDelay)               
                #print("Fectching the details of {}".format(all_pages[i]))
            soup = BeautifulSoup(page.text, 'html.parser')
            hotel_containers=soup.find_all(class_='ui_column is-8 main_col allowEllipsis ')
            for j in range(0,len(hotel_containers)):
                count=count+1
                print(count)
                hotel_href=hotel_containers[j].find('a')['href']                
                Hotel_PageUrl=url+hotel_href
                Hotels_URLS.append(Hotel_PageUrl)
    except:
        print("all ips have been expired.Add some more proxies to scrape")
    return Hotels_URLS        
            







#"ReviewID","ReviewTitle","ReviewText","NonEng","RatingDate","StayTime",
#"AvgRatingStarsThisUser","Value","Location","SleepQuality","Rooms","Cleanliness","Service",

def reviews(reviews_url,ip):
    Reviews={}
    time.sleep(timeDelay)
    proxy=random.choice(ip)
    proxies={
            'http': f'http://{proxy}',
            'https':f'https://{proxy}',
            }
    try:
        #Page=requests.get(reviews_url,headers={'User-Agent':ua.random},proxies=proxies)
        Page=requests.get(reviews_url,headers={'User-Agent':ua.random})
    except:
        Page=requests.get(reviews_url,headers={'User-Agent':ua.random})        
    while(Page.status_code!=200):
        time.sleep(timeDelay)
        ip.remove(proxy)
        proxy=random.choice(ip)                
        Page=requests.get(reviews_url,headers={'User-Agent':ua.random})
        print("Page not found")
    Hotel_ID=reviews_url.split('-')[2][1:]
    Area_ID=reviews_url.split('-')[1][1:]            
    soup=BeautifulSoup(Page.text, 'html.parser')
    reviews=soup.find_all(class_="ui_column is-9")
    next_available=soup.find_all(class_="nav next taLnk ui_button primary")
    if(len(next_available)>0):
        condition_check=next_available[0].text
        count=0
        while(condition_check!=None and count<500):
            count=count+1
            time.sleep(timeDelay)
            proxy=random.choice(ip)
            proxies={
                     'http': f'http://{proxy}',
                     'https':f'https://{proxy}',
                     }
            try:
                Page=requests.get(reviews_url,headers={'User-Agent':ua.random})
            except:
                print("failed to connect to the proxy ,creating a new connection")
                proxy=random.choice(ip)
                proxies={
                     'http': f'http://{proxy}',
                     'https':f'https://{proxy}',
                     }
                Page=requests.get(reviews_url,headers={'User-Agent':ua.random})               
            while(Page.status_code!=200):
                print("Page not found")
                ip.remove(proxy)
                proxy=random.choice(ip)
                proxies={
                     'http': f'http://{proxy}',
                     'https':f'https://{proxy}',
                     }
                time.sleep(timeDelay)
                Page=requests.get(reviews_url,headers={'User-Agent':ua.random})
                #print("Fecthing the deatils of URL",reviews_url)
            soup=BeautifulSoup(Page.text, 'html.parser')
            next_available=soup.find_all(class_="nav next taLnk ui_button primary")
            reviews=soup.find_all(class_="ui_column is-9")
            users=soup.find_all(class_="ui_column is-2")
            for i in range(0,len(reviews)):
                review_id=reviews[i].find(class_="quote")
                try:
                    Review_ID=review_id.find('a')['id'].split('rn')[1]
                except:
                    Review_ID='NA'
                print(Review_ID)                
                review_title=reviews[i].find(class_="noQuotes")
                try:
                    Review_Title=review_title.text
                except:
                    Review_Title='NA'
                print(Review_Title)
                date_of_stay=reviews[i].find(class_="prw_rup prw_reviews_stay_date_hsx")
                try:
                    Date_Of_Stay=date_of_stay.text.split('Date of stay:')[1]
                except:
                    Date_Of_Stay='NA'
                trip_type=reviews[i].find(class_="recommend-titleInline noRatings")
                try:
                    Trip_Type=trip_type.text.split(':')[1]
                except:
                    Trip_Type='NA'
                review_text=reviews[i].find(class_="prw_rup prw_reviews_text_summary_hsx")
                try:
                    Review_Text=review_text.text
                except:
                    Review_Text='NA'
                try:
                    User_Rating=int(reviews[i].find('span')['class'][1].split('_')[1])
                except:
                    User_Rating='NA'    
                review_date=reviews[i].find(class_="ratingDate")
                if(review_date!=None):
                    Review_Date=review_date['title']
                else:
                    Review_Date='NA'
                SleepQuality='NA'
                Value='NA'
                Rooms='NA'
                LocationQuality='NA'
                Cleanliness='NA'
                Service='NA'
                attribute_ratings=reviews[i].find_all(class_="recommend-answer")
                if(attribute_ratings!=None):
                    for j in range(0,len(attribute_ratings)):
                        if(attribute_ratings[j].text=='Sleep Quality'):
                            SleepQuality=(attribute_ratings[j].find('div')['class'][1].split('_')[1])
                        elif(attribute_ratings[j].text=='Value'):
                            Value=(attribute_ratings[j].find('div')['class'][1].split('_')[1])
                        elif(attribute_ratings[j].text=='Rooms'):
                            Rooms=(attribute_ratings[j].find('div')['class'][1].split('_')[1])
                        elif(attribute_ratings[j].text=='Cleanliness'):
                            Cleanliness=(attribute_ratings[j].find('div')['class'][1].split('_')[1])
                        elif(attribute_ratings[j].text=='Location'):
                            LocationQuality=(attribute_ratings[j].find('div')['class'][1].split('_')[1])
                        elif(attribute_ratings[j].text=='Service'):
                            Service=(attribute_ratings[j].find('div')['class'][1].split('_')[1])
                user_id=users[i].find(class_="member_info")
                time.sleep(timeDelay)
                try:
                    User_ID=user_id.find('div')['id']
                except:
                    User_ID='NA'
                contributions_helpful=users[i].find(class_="memberBadgingNoText is-shown-at-tablet")
                badge_text=contributions_helpful.find_all(class_="badgetext")
                contributions=contributions_helpful.find(class_="ui_icon pencil-paper")
                helpful_votes=contributions_helpful.find(class_="ui_icon thumbs-up-fill")
                Contributions='NA'
                Helpful_Votes='NA'
                if(contributions!=None):
                    Contributions=badge_text[0].text
                if(helpful_votes!=None and len(badge_text)==2):
                    Helpful_Votes=badge_text[1].text
                elif(helpful_votes!=None and len(badge_text)==1):
                    Helpful_Votes=badge_text[0].text
                NonEng=0
                user_location=users[i].find(class_="userLoc")
                if(user_location!=None):
                    #print(user_location.text)
                    User_Location=user_location.text
                else:
                    User_Location='NA'
                user_profile=users[i].find('div',class_="info_text")
                if(user_profile!=None and user_location!=None):
                    User_Pofile="https://www.tripadvisor.com/Profile/"+user_profile.text.split(User_Location)[0]
                elif(user_profile!=None and user_location==None):
                    User_Pofile="https://www.tripadvisor.com/Profile/"+user_profile.text                    
                else:
                    User_Pofile='NA'
                Reviews.update({
                        Review_ID:{
                        "Hotel_ID":Hotel_ID,
                        "Area_ID":Area_ID,
                        "Review_Title":Review_Title,
                        "Review_Text":Review_Text,
                        "NonEnglish":NonEng,
                        "Review_Date":Review_Date,
                        "Date_Of_Stay":Date_Of_Stay,
                        "User_Rating":User_Rating,
                        "Trip_Type":Trip_Type,
                        "SleepQulaity":SleepQuality,
                        "Value":Value,
                        "Rooms":Rooms,
                        "LocationQuality":LocationQuality,
                        "Cleanliness":Cleanliness,
                        "Service":Service,
                        "User_ID":User_ID,
                        "User_Location":User_Location,
                        "User_Profile":User_Pofile,
                        "Contributions":Contributions,
                        "Helpful_Votes":Helpful_Votes
                        }
                        })
            print(reviews_url)
            if(len(next_available)>0):
                print("length of next",len(next_available))
                reviews_url=url+next_available[0]['href']
            else:
                condition_check=None
                next_available=[]
                print("No more reviews to scrape for that hotel")
                print(condition_check)
    elif(len(next_available)==0 and len(reviews)>0):
        print("elif loop")
        proxy=random.choice(ip)
        proxies={
                'http': f'http://{proxy}',
                'https':f'https://{proxy}',
                     }
        Page=requests.get(reviews_url,headers={'User-Agent':ua.random})
        print("scraping last page of url")
        while(Page.status_code!=200):
            time.sleep(timeDelay)
            ip.remove(proxy)
            proxy=random.choice(ip) 
            proxies={
                'http': f'http://{proxy}',
                'https':f'https://{proxy}',
                     }
            Page=requests.get(reviews_url,headers={'User-Agent':ua.random})
            print("status code  is not 200")
        #print("Fecthing the deatils of URL",reviews_url)
        soup=BeautifulSoup(Page.text, 'html.parser')
        reviews=soup.find_all(class_="ui_column is-9")
        users=soup.find_all(class_="ui_column is-2")
        for i in range(0,len(reviews)):
            review_id=reviews[i].find(class_="quote")
            try:
                Review_ID=review_id.find('a')['id'].split('rn')[1]
                print(Review_ID)
            except:
                Review_ID='NA'
                review_title=reviews[i].find(class_="noQuotes")
            try:
                Review_Title=review_title.text
            except:
                Review_Title='NA'
            print(Review_Title)
            date_of_stay=reviews[i].find(class_="prw_rup prw_reviews_stay_date_hsx")
            try:
                Date_Of_Stay=date_of_stay.text.split('Date of stay:')[1]
            except:
                Date_Of_Stay='NA'
            trip_type=reviews[i].find(class_="recommend-titleInline noRatings")
            try:
                Trip_Type=trip_type.text.split(':')[1]
            except:
                Trip_Type='NA'
            review_text=reviews[i].find(class_="prw_rup prw_reviews_text_summary_hsx")
            try:
                Review_Text=review_text.text
            except:
                Review_Text='NA'
            try:
                User_Rating=int(reviews[i].find('span')['class'][1].split('_')[1])
            except:
                User_Rating='NA'
            review_date=reviews[i].find(class_="ratingDate")
            if(review_date!=None):
                Review_Date=review_date['title']
            else:
                Review_Date='NA'
            SleepQuality='NA'
            Value='NA'
            Rooms='NA'
            LocationQuality='NA'
            Cleanliness='NA'
            Service='NA'
            attribute_ratings=reviews[i].find_all(class_="recommend-answer")
            if(attribute_ratings!=None):
                for j in range(0,len(attribute_ratings)):
                    if(attribute_ratings[j].text=='Sleep Quality'):
                        SleepQuality=(attribute_ratings[j].find('div')['class'][1].split('_')[1])
                    elif(attribute_ratings[j].text=='Value'):
                        Value=(attribute_ratings[j].find('div')['class'][1].split('_')[1])
                    elif(attribute_ratings[j].text=='Rooms'):
                        Rooms=(attribute_ratings[j].find('div')['class'][1].split('_')[1])
                    elif(attribute_ratings[j].text=='Cleanliness'):
                        Cleanliness=(attribute_ratings[j].find('div')['class'][1].split('_')[1])
                    elif(attribute_ratings[j].text=='Location'):
                        LocationQuality=(attribute_ratings[j].find('div')['class'][1].split('_')[1])
                    elif(attribute_ratings[j].text=='Service'):
                        Service=(attribute_ratings[j].find('div')['class'][1].split('_')[1])
            user_id=users[i].find(class_="member_info")
            time.sleep(timeDelay)
            try:
                User_ID=user_id.find('div')['id']
            except:
                User_ID='NA'
            contributions_helpful=users[i].find(class_="memberBadgingNoText is-shown-at-tablet")
            badge_text=contributions_helpful.find_all(class_="badgetext")
            contributions=contributions_helpful.find(class_="ui_icon pencil-paper")
            helpful_votes=contributions_helpful.find(class_="ui_icon thumbs-up-fill")
            Contributions='NA'
            Helpful_Votes='NA'
            if(contributions!=None):
                Contributions=badge_text[0].text
            if(helpful_votes!=None and len(badge_text)==2):
                Helpful_Votes=badge_text[1].text
            elif(helpful_votes!=None and len(badge_text)==1):
                Helpful_Votes=badge_text[0].text
            NonEng=0
            user_location=users[i].find(class_="userLoc")
            if(user_location!=None):
                User_Location=user_location.text
            else:
                User_Location='NA'
            user_profile=users[i].find('div',class_="info_text")
            if(user_profile!=None and user_location!=None):
                User_Pofile="https://www.tripadvisor.com/Profile/"+user_profile.text.split(User_Location)[0]
            elif(user_profile!=None and user_location==None):
                User_Pofile="https://www.tripadvisor.com/Profile/"+user_profile.text                    
            else:
                User_Pofile='NA'
            print(reviews_url)
            if(len(next_available)>0):
                reviews_url=url+next_available[0]['href']
            else:
                next_available=[]
                condition_check=None
                print("No more reviews to scrape for that hotel")
            
            Reviews.update({
                            Review_ID:{
                            "Hotel_ID":Hotel_ID,
                            "Area_ID":Area_ID,
                            "Review_Title":Review_Title,
                            "Review_Text":Review_Text,
                            "NonEnglish":NonEng,
                            "Review_Date":Review_Date,
                            "Date_Of_Stay":Date_Of_Stay,
                            "User_Rating":User_Rating,
                            "Trip_Type":Trip_Type,
                            "SleepQulaity":SleepQuality,
                            "Value":Value,
                            "Rooms":Rooms,
                            "LocationQuality":LocationQuality,
                            "Cleanliness":Cleanliness,
                            "Service":Service,
                            "User_ID":User_ID,
                            "User_Location":User_Location,
                            "User_Profile":User_Pofile,
                            "Contributions":Contributions,
                            "Helpful_Votes":Helpful_Votes
    
                            }
                            })
    else:
        print("No reviews for the current Hotel")
        Reviews=Reviews
    
    return Reviews


#0,#180-211
def Details(Hotel_PageUrl,ip):
    for i in range(0,len(Hotel_PageUrl)):
        print(Hotel_PageUrl[i])
        time.sleep(timeDelay)
        proxy=random.choice(ip)
        proxies={
            'http': f'http://{proxy}',
            'https':f'https://{proxy}',
            }
        try:
            hotel_page=requests.get(Hotel_PageUrl[i],headers={'User-Agent':ua.random})
        except :
            proxy=random.choice(ip)
            proxies={
            'http': f'http://{proxy}',
            'https':f'https://{proxy}',
            }
            hotel_page=requests.get(Hotel_PageUrl[i],headers={'User-Agent':ua.random})            
        while(hotel_page.status_code!=200):
            time.sleep(timeDelay)
            ip.remove(proxy)
            proxy=random.choice(ip)
            print("status code is not 200")
            hotel_page=requests.get(Hotel_PageUrl[i],headers={'User-Agent':ua.random})
        soup2= BeautifulSoup(hotel_page.text, 'html.parser')
        Hotel_ID=Hotel_PageUrl[i].split('-')[2][1:]
        Area_ID=Hotel_PageUrl[i].split('-')[1][1:]
        hotel_location=soup2.find(class_="detail")
        try:
            Location=hotel_location.text
        except:
            Location='NA'
        print(Location)
        reviews_href=soup2.find_all(class_="hotels-review-list-parts-ReviewTitle__reviewTitleText--3QrTy")
        time.sleep(timeDelay+20)
        if(len(reviews_href)>0):
            review_href=reviews_href[0]['href']
            if(review_href!=None):
                reviews_url=url+review_href
                k=reviews(reviews_url,ip)
                if(len(k)>0):
                    for i in k.values():
                        i.update({"Location":Location})
        else:
             Hotel_ID=Hotel_PageUrl[i].split('-')[1][1:]
             Area_ID=Hotel_PageUrl[i].split('-')[2][1:]
             k={ "NA":{
                 "Hotel_ID":Hotel_ID,
                 "Area_ID":Area_ID,
                 "Review_Title":"NA",
                 "Review_Text":"NA",
                 "NonEnglish":"NA",
                 "Review_Date":"NA",
                 "Date_Of_Stay":"NA",
                 "User_Rating":"NA",
                 "Trip_Type":"NA",
                 "SleepQulaity":"NA",
                 "Value":"NA",
                 "Rooms":"NA",
                 "LocationQuality":"NA",
                 "Cleanliness":"NA",
                 "Service":"NA",
                 "User_ID":"NA",
                 "Contributions":"NA",
                 "Helpful_Votes":"NA",
                 "User_Location":"NA",
                 "User_Profile":"NA",
                 "Location":Location
                        }                            
                            }
        #pickle.dump(k,open("C:\\Users\\harsh\\OneDrive\\Desktop\\TripAdvisor\\Restuarents_Data\\Hotel_Info.p","wb"))
        df=pd.DataFrame.from_dict(k,orient='index') 
        df.to_csv("C:\\Users\\harsh\\OneDrive\\Desktop\\TripAdvisor\\Hotels\\Hotel_Reviews.csv",sep=',',header=True,index_label='Review_ID',encoding='utf-8',mode='a')
    return(df)

          

if __name__=="__main__":
    main()