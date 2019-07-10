# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 03:07:10 2019

@author: harsh
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 03:53:41 2019

@author: harsh
"""

#"HotelID","HotelName","CityID","AreaID","StarClass","NbRooms","Amenities","Daily","Reviews","PageUrl"

import requests
import random
import time
import sys
from bs4 import BeautifulSoup

base_url=['/'+'Hotels-g60745-Boston_Massachusetts-Hotels.html']

url='https://www.tripadvisor.com'
timeDelay=random.randrange(0,20)

#Scraping all the pages from the main page
def pages(url,base_url):
    pages_list=["".join(base_url)]
    page=requests.get(url+base_url[0])
    soup = BeautifulSoup(page.text, 'html.parser')
    page_numbers=soup.find(class_='pageNumbers')
    page_info=page_numbers.find_all('a')
    for i in range(0,len(page_info)):
        time.sleep(timeDelay)
        page_urls=page_info[i]['href']
        print("fecthing page",page_urls)
        pages_list.append(page_urls)
    return pages_list
all_pages=pages(url,base_url)


def amenities(new_url):
    Amenities=[]
    timeDelay=random.randrange(0,20)
    reviews_pages=requests.get(new_url)
    #print(reviews_pages)
    soup2 = BeautifulSoup(reviews_pages.text, 'html.parser')
    time.sleep(timeDelay)
    reviews=soup2.find(class_="hotels-hotel-review-about-with-photos-Reviews__seeAllReviews--3PpLR")
    amenities=soup2.find_all(class_="hotels-hotel-review-about-with-photos-Amenity__name--2IUMR")
    attractions_nearby=soup2.find(class_="hotels-hotel-review-location-layout-Highlight__number--S3wsZ hotels-hotel-review-location-layout-Highlight__blue--2qc3K")
    walkable_grade=soup2.find(class_="hotels-hotel-review-location-layout-Highlight__number--S3wsZ hotels-hotel-review-location-layout-Highlight__green--3lccI")
    try:
        Walkable_Grade=walkable_grade.text
    except:
        Walkable_Grade='NA'
    try:
        Attractions_NearBy=attractions_nearby.text
    except:
        Attractions_NearBy='NA'       
    if(len(amenities)>0):
        for j in range(0,len(amenities)):
            Amenities.append((amenities[j].text))
    else:
        Amenities.append('NA')
    try:
        Reviews=reviews.text
    except:
        Reviews='NA'        
    nbrooms=soup2.find_all(class_="hotels-hotel-review-about-addendum-AddendumItem__content--iVts5")
    try:
        type(int(nbrooms[-1].text))==int
        NbRooms=int(nbrooms[-1].text)
        print(NbRooms)
    except:
        NbRooms='NA'
    starclass=soup2.find_all(class_="hotels-hotel-review-about-with-photos-layout-TextItem__textitem--3kv6J")
    try:
        type(int((starclass[-1].find('span')['class'])[1][5:]))==int
        StarClass=int((starclass[-1].find('span')['class'])[1][5:])/10
    except:
        StarClass='NA'
    Daily=1
    return({"Amenties":",".join(Amenities),"Reviews":Reviews,"NbRooms":NbRooms,
            "StarClass":StarClass,"Daily":Daily,
            "Attractions_NearBy":Attractions_NearBy,"Walkable_Grade":Walkable_Grade})

    
#Scraping all the HotelName,HotelId,CityID,AreaID,       
def  hotels(all_pages):
    hotel_details=[]
    if(len(all_pages)<1):
        print("Not able to fetch any pages..Exiting program")
        print("Pages:{}".format(all_pages))
        sys.exit()
    else:
        print("feteched all pages")
        print("Page URLS{}".format(all_pages))
        for i in range(0,len(all_pages)):
            time.sleep(timeDelay)
            page=requests.get(url+"".join(all_pages[i]))
            print("Fectching the details of {}".format(url+"".join(all_pages[i])))
            soup = BeautifulSoup(page.text, 'html.parser')
            hotel_containers=soup.find_all(class_='ui_column is-8 main_col allowEllipsis ')
            for j in range(0,len(hotel_containers)):
                HotelID=hotel_containers[j].find('a')['id'].split('property_')[1]
                HotelName=hotel_containers[j].find('a').text
                CityID=hotel_containers[j].find('a')['href'].split('-')[1][1:]
                AreaID=CityID
                hotel_url=hotel_containers[j].find('a')['href']
                PageUrl=url+hotel_url
                details=amenities(PageUrl)
                Amenities=details['Amenties']
                NbRooms=details['NbRooms']
                StarClass=details['StarClass']
                Daily=details['Daily']
                Reviews=details['Reviews']
                Attractions_NearBy=details['Attractions_NearBy']
                Walkable_Grade= details['Walkable_Grade']              
                hotel_details.append({"HotelID":HotelID,
                                      "HotelName":HotelName,
                                      "CityID":CityID,
                                      "AreaID":AreaID,
                                      "StarClass":StarClass,
                                      "NbRooms":NbRooms,
                                      "Amenities":Amenities,
                                      "Daily":Daily,
                                      "Reviews":Reviews,
                                      "PageUrl":PageUrl,
                                      "Attractions_NearBy":Attractions_NearBy,
                                      "Walkable_Grade":Walkable_Grade                                      
                                      })
    return hotel_details
    
data=hotels(all_pages)

import pandas as pd
hotel_info=pd.DataFrame(data)



hotel_info.to_csv("C:\\Users\\harsh\\OneDrive\\Desktop\\TripAdvisor\\Hotels\\Hotel_Info.csv",
          header=True,columns=["HotelID","HotelName","CityID","AreaID","StarClass"
                               ,"NbRooms","Amenities","Daily","Reviews",
                               "PageUrl","Attractions_NearBy","Walkable_Grade"],
          index=False,encoding='utf-8')


hotel_info.head()


import pandas as pd
df=pd.read_csv("C:\\Users\\harsh\\OneDrive\\Desktop\\TripAdvisor\\Hotels\\Hotel_Info.csv",encoding='utf-8')


