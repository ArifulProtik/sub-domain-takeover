import requests
import sys
import os
import argparse
from bs4 import BeautifulSoup

errorTexts = [
    "The specified bucket does not exit ",
       "Repository not found ",
       "ERROR\: The request could not be satisfied ",
       "There isn't a GitHub Pages site here.",
       "Sorry\, this shop is currently unavailable\. ",
       "Sorry\, We Couldn't Find That Page ",
       "Fastly error\: unknown domain\: ",

       "The feed has not been found\. ",
       "The thing you were looking for is no longer here\, or never was ",
       "no-such-app.html|<title>no such app</title>|herokucdn.com/error-pages/no-such-app.html ",
       "The gods are wise, but do not know of the site which you seek. ",
       "Whatever you were looking for doesn't currently exist at this address. ",
       "Do you want to register ",
       "Help Center Closed ",

       "Oops - We didn't find your site. ",
       "We could not find what you're looking for. ",
       "No settings were found for this company: ",
       "The specified bucket does not exist ",
       "<title>404 &mdash; File not found</title> ",
       "You are being <a href=\"https://www.statuspage.io\">redirected ",
       "This UserVoice subdomain is currently available! ",
       "project not found ",
       "This page is reserved for artistic dogs\.|Uh oh\. That page doesn't exist</h1> ",

       "<p class=\"description\">The page you are looking for doesn't exist or has been moved.</p> ",
       "<h1>The page you were looking for doesn't exist.</h1> ",
       "You may have mistyped the address or the page may have moved. ",
       "<h1>Error 404: Page Not Found</h1> ",

       "<h1>https://www.wishpond.com/404?campaign=true ",
       "Oops.</h2><p class=\"text-muted text-tight\">The page you're looking for doesn't exist. ",
       "There is no portal here \.\.\. sending you back to Aha! ",
       "to target URL: <a href=\"https://tictail.com|Start selling on Tictail. ",
       "<p class=\"bc-gallery-error-code\">Error Code: 404</p> ",
       "<h1>Oops! We couldn&#8217;t find that page.</h1> ",
       "alt=\"LIGHTTPD - fly light.\" ",

       "Double check the URL or <a href=\"mailto:help@createsend.com ",
       "The site you are looking for could not be found.|If you are an Acquia Cloud customer and expect to see your site at this address ",
       "If you need immediate assistance, please contact <a href=\"mailto:support@proposify.biz ",
       "We can't find this <a href=\"https://simplebooklet.com ",
       "With GetResponse Landing Pages, lead generation has never been easier ",
       "Looks like you've traveled too far into cyberspace. ",
       "is not a registered InCloud YouTrack. ",

       "The requested URL / was not found on this server|The requested URL was not found on this server ",
       "Domain is not configured ",
       "pingdom ",
       "Domain has been assigned ",
       "data-html-name ",
       "Unrecognized domain <strong> ",
]
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

def findsubdomains(host):
    banner()
    try:
        req = requests.get("https://findsubdomains.com/subdomains-of/"+host, headers=headers, timeout=5)
    except requests.exceptions.HTTPError:
        print("Could Not Connect To The Server")
    except requests.exceptions.ConnectionError:
        print("Check The Internet Connection")
    except requests.exceptions.Timeout:
        print("Your Internet Connection Might Be Slow")
    parsetext = req.text
    soup = BeautifulSoup(parsetext, 'html.parser')
    findingElement=soup.findAll("td", {"data-field": "Domain"})
    with open('subdomains.txt', 'w') as subdomians:
        for sublink in findingElement:
            link = sublink.find('a').text
            print(link)
            subdomians.write(link+"\n")
    subdomians.close()


def attack(mainurl):
    print("Finding Subdomains Please Wait....")
    findsubdomains(mainurl)
    count = len(open("subdomains.txt").readlines(  ))
    print("\n"+str(count) + " Subdomain found Saved As subdomains.txt")
    print("Now Checking For Vulnerbility....")
    readfile = open('subdomains.txt', 'r')
    list = readfile.read().split('\n')
    for target in list:
        if target == "":
            continue
        try:
            response = requests.get("http://"+target, headers=headers)
            response.text
        except requests.exceptions.ConnectionError:
            continue
        targetresponse = response.text
        for err in errorTexts:
            if err in targetresponse:
                print("Potential Vulnerbility Detected:" + target)
                break
        print("Not Found:" + target)
    readfile.close()
def banner():
    if (os.name in ('ce', 'nt', 'dos')):
        os.system('cls')
    elif ('posix' in os.name):
        os.system('clear')
    print("               #####################################################")
    print("               # Tool: Subdomain Takeover vulnerbility Checker     #")
    print("               # Author:  github.com/ArifulProtik                  #")
    print("               # Feel Free To Open A Issue If You Need Any Update  #")
    print("               #####################################################")
    print("\n")
def Main():
    #Initializing Argparser for Further Update
    parser = argparse.ArgumentParser()
    parser.add_argument("hostlink", help="Usage python subdomain.py example.com", type= str)
    args = parser.parse_args()
    attack(args.hostlink)
if __name__ == "__main__":
    Main()
