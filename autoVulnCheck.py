#!/usr/bin/env python3

import requests
import threading
import re
from urllib.parse import *

dirBruteWordlist = "common.txt" # Try changing this wordlist
subBruteWordlist = "subdomains-top1million-20000.txt" # Try Changing this wordlist
foundDirs        = []
allDirs          = []
allSubs          = []
crawledLinks     = []

def dirBruteForcer(targetUrl):
    wordlist = dirBruteWordlist
    wordlistCont = ""
    try:
        givenWordlist = open(wordlist, "r")
        wordlistCont  = givenWordlist.read()
    except Exception:
        print("[-] Can't Open the file")
        exit()
    targetUrl = "http://" + targetUrl + "/"
    print("[+] Directory Brute Force attack started!")
    newFile = open("directoryScanOutput.txt", "a")
    for words in wordlistCont.split():
        try:
            myreq = requests.get(targetUrl + words)
            if myreq.status_code != 404:
                    foundNewDirs  = targetUrl + words
                    reqStatusCode = myreq.status_code
                    output = targetUrl + words + "   --> (Status Code) " + str(myreq.status_code)
                    print(output)
                    if reqStatusCode == 200:
                        allDirs.append(foundNewDirs)
                        foundDirs.append(foundNewDirs)
                    newFile.write(output + "\n")
        except Exception:
            pass
    while len(foundDirs) != 0:
        foundDirLen = len(foundDirs)
        for newDirs in foundDirs:
            targetUrl = newDirs + "/"
            for words in wordlistCont.split():
                try:
                    myreq = requests.get(targetUrl + words)
                    if myreq.status_code != 404:
                        foundNewDirs = targetUrl + words
                        reqStatusCode = myreq.status_code
                        output = targetUrl + words +  "   --> (Status Code) " + str(myreq.status_code)
                        print(output)
                        if reqStatusCode == 200:
                            foundDirs.append(foundNewDirs)
                            allDirs.append(foundNewDirs)
                        newFile.write(output + "\n")
                except Exception:
                    pass
        del foundDirs[:foundDirLen]
                
    newFile.close()
    print("[+] Directory Brute attack finished! and output written in -> directoryScanOutput.txt")
    
def subDomainBrutForcer(targetUrl):
    wordlist = subBruteWordlist
    wordlistCont = ""
    try:
        givenWordlist = open(wordlist, "r")
        wordlistCont  = givenWordlist.read()
    except Exception:
        print("[-] Can't Open the file")
        exit()
        
    print("[+] Sub-Domain Brute Force attack started!")
    newFile = open("subDomainScanOutput.txt", "a")
    for words in wordlistCont.split():
        try:
            testUrl = "http://" + words + "." + targetUrl
            myreq = requests.get(testUrl)
            if myreq.status_code == 200:
                output = testUrl
                allSubs.append(output)
                print(output)
                newFile.write(output + "\n")
                
        except Exception:
            pass
    print("[+] Directory Brute attack finished! and output written in -> subDomainScanOutput.txt")

def crawler(targetUrl):
    newFile = open("crawledLinks.txt", "a")
    for all_links in allDirs:
        req = requests.get(all_links)
        reqCont = req.content
        found_links = re.findall('(?:href=")(.*?)"', str(reqCont))
        for links in found_links:
            link = urljoin(targetUrl, links)
            if targetUrl in link:
                if link not in crawledLinks:
                    crawledLinks.append(link)
                    print(link)
                    newFile.write(link + "\n")
    for all_links in allSubs:
        req = requests.get(all_links)
        reqCont = req.content
        found_links = re.findall('(?:href=")(.*?)"', str(reqCont))
        for links in found_links:
            link = urljoin(targetUrl, links)
            if targetUrl in link:
                if link not in crawledLinks:
                    crawledLinks.append(link)
                    print(link)
                    newFile.write(link + "\n")

def getUrlFromUsr():
    usrUrl = str(input("Enter the url to scan >_ "))
    return usrUrl


def checkTargetAvai(targetUrl):
    targetUrl = "http://" + targetUrl + "/"
    try:
        req = requests.get(targetUrl, timeout=10)
    except Exception:
        print("[-] Please enter the valid url (Format : example.com)")
        return False
    if req.status_code == 200:
        print("[+] The given url is alive and running")
        return True
    else:
        return False
def main():
    is_true = False
    while is_true == False:
        usrUrl  = getUrlFromUsr()
        is_true = checkTargetAvai(usrUrl)
    # dirBruteForcer(usrUrl)
    # subDomainBrutForcer(usrUrl)
    # crawler(usrUrl)
    th1 = threading.Thread(target=dirBruteForcer, args=[usrUrl])
    th2 = threading.Thread(target=subDomainBrutForcer, args=[usrUrl])
    th1.start()
    th2.start()
    th1.join()
    th2.join()
    crawler(usrUrl)

main()