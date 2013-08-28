#! /usr/bin/env python
#
"""Foobar.py: Description of what foobar does."""

__author__      = "Carlo Andrea Conte"
__copyright__   = "Copyright 2013, Mahaya, inc."
__email__       = "carloandreaconte@icloud.com"

import json
import urllib
import sys
import argparse
import time
import calendar

outputtimeformat = "%m/%d/%y %H:%M"

def generateImageThumb(url, caption):
    return "<div style='overflow:hidden;float:left;height:350px;width:300px;margin:10px 20px;border:dashed 1px #999999'><p>"+caption+"</p><img style='max-width:300px;max-height:300px;' src='"+url+"' /></div>"

def generateThumbs(images):
    html = ""
    for image in images:
        html += (generateImageThumb(image["url"],image["caption"]))
    return html

def getData(url):
    request = urllib.urlopen(url)
    response = request.read()
    return json.loads(response)

def getVenueData(venue_id):
    request_url = "https://api.foursquare.com/v2/venues/"+venue_id+"?client_id=5Q1H45P0EPAYUA05E0AHK4PIHB0Z0P2QRLY1JKKB14PDKGBK&client_secret=J2YHXBRPNEUNNX1XRUWMGTM41GQNBHHSAUOLRPNQ2MOXJR3Z"
    data        = getData(request_url)
    
    result = {}
    result["lat"]  = data["response"]["venue"]["location"]["lat"]
    result["lng"]  = data["response"]["venue"]["location"]["lng"]
    result["name"] = data["response"]["venue"]["name"]
    
    return result
    print "<h1>Pictures from "+data["response"]["venue"]["name"]+"</h1>"

def getInstagramPhotos(lat,lng,distance,desiredtimestamp,eventlength,instagram_client_id):
    request_url = "https://api.instagram.com/v1/media/search?client_id="+instagram_client_id+"&lat="+str(lat)+"&lng="+str(lng)+"&max_timestamp="+str(desiredtimestamp+eventlength)+"&min_timestamp="+str(desiredtimestamp)+"&distance="+str(distance)
    #Pictures can be retrieved by foursquare location id as well -> higher precision but lower recall
    
    data = getData(request_url)
    pictures = []
    for photo in data["data"]:
        url = photo["images"]["low_resolution"]["url"]
        creation_time = time.gmtime(int(photo["created_time"]))
        formatted_time = time.strftime(outputtimeformat,creation_time)
        caption = str(formatted_time)
        pictures.append({"url":url, "caption":caption})
    return pictures

def getFoursquarePhotos(venue_id,desiredtimestamp,eventlength,foursquare_client_id, foursquare_client_secret):
    request_url = "https://api.foursquare.com/v2/venues/"+venue_id+"/photos?group=venue&limit=200&client_id="+foursquare_client_id+"&client_secret="+foursquare_client_secret
    data = getData(request_url)
    pictures = []
    for photo in data["response"]["photos"]["items"]:
        url = photo["url"]
        creation_time = time.gmtime(photo["createdAt"])
        formatted_time = time.strftime(outputtimeformat,creation_time)
        if int(photo["createdAt"]) - desiredtimestamp < eventlength and int(photo["createdAt"]) - desiredtimestamp > 0:
            pictures.append({"url":url, "caption":formatted_time})
    return pictures

def createWebpage(page):
    try:
        f = open("latipics_results.html", "w")
        try:
            f.write(page)
        finally:
            f.close()
    except IOError:
        print "There has been a problem with writing the file!"

def getResults(date, duration, distance, venue_id, instagram_client_id, foursquare_client_id, foursquare_client_secret, webpage = False):
        desiredtime      = time.strptime(date,"%Y%m%d%H")
        desiredtimestamp = calendar.timegm(desiredtime)
        eventlength      = int(duration)*60*60
        distance         = int(distance)
        html = ""
        pictures=[]
        try:
            venue_data = getVenueData(venue_id)
            html += "<!DOCTYPE html><html><head><title>Pictures on"+ time.strftime("%m/%d/%Y %H:00", desiredtime)+"</title></head><body>"
            html += "<h1>Pictures from "+venue_data["name"]+"</h1>"
        
            html += "<h2 style='clear:both'>Instagram Photos</h2>"
            instagramPhotos = getInstagramPhotos(venue_data["lat"],venue_data["lng"],distance,desiredtimestamp,eventlength,instagram_client_id)
            pictures.extend(instagramPhotos)
            html += generateThumbs(instagramPhotos)
        
            html += "<h2 style='clear:both'>Foursquare photos</h2>"
            foursquarePhotos = getFoursquarePhotos(venue_id,desiredtimestamp,eventlength,foursquare_client_id, foursquare_client_secret)
            pictures.extend(foursquarePhotos)
            html += generateThumbs(foursquarePhotos)
        
            html += "</body></html>"
            
            if webpage: createWebpage(html)
        except Exception as e:
            print "There has been a problem, double check venue id and your API credentials"
            print e.strerror
        finally:
            return pictures

def main():
    global outputtimeformat
    default_time = time.strftime("%Y%m%d%H",time.gmtime(time.time() - 518400))
    p = argparse.ArgumentParser()
    p.add_argument('-d',
                 '--date',
                 nargs='?',
                 default=default_time,
                 help='Insert (UTC) date and time as YYYYMMDDHH')
    p.add_argument('-v',
                 '--venue',
                 help='Insert venue ID')
    p.add_argument('-dr',
                 '--duration',
                 nargs='?',
                 default="144",
                 help='Event length in hours')
    p.add_argument('-ds',
                 '--distance',
                 nargs='?',
                 default="10",
                 help='Distance tolerance in meters')
    p.add_argument('-inst',
                 '--instagram_client_id',
                 help='Instagram client_id for API calls')
    p.add_argument('-fsid',
                 '--foursquare_client_id',
                 help='Foursquare client_id for API calls')
    p.add_argument('-fssec',
                 '--foursquare_client_secret',
                 help='Foursquare client_secret for API calls')
    args = p.parse_args()

    getResults(args.date, args.duration, args.distance, args.venue, args.instagram_client_id, args.foursquare_client_id, args.foursquare_client_secret, webpage=True)
    print "Done."
    
if __name__ == '__main__' : 
	main()