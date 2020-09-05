from simple_salesforce import Salesforce as sf
import configparser as cfg
import webbrowser as wb
import os
import time
#webbrowser.open('http://www.python.org') 

def sessionInitiator(uname,passkey,sec):
    try:
        s = sf(username=uname,password=passkey,security_token=sec)
        #print('Connected to : '+s.base_url)
        return s
    except:
        print("[-]Session cannot be initiated")

def credParser():
    try:
        cg = cfg.ConfigParser()
        cg.read('creds.ini')
        connVals = {}
        if 'CREDS' in cg :
            connVals = {'username': cg['CREDS']['username'],
                        'password': cg['CREDS']['password'],
                        'secret': cg['CREDS']['sec'],
                        'consumer_key': cg['CREDS']['consumer_key'],
                        'consumer_secret': cg['CREDS']['consumer_secret'],
                        'access_token':cg['CREDS']['access_token'],
                        'prod_url':cg['CREDS']['prod_url'],
                        'sandbox_url':cg['CREDS']['sandbox_url']}
        return connVals
    except:
        print("[-]CredParser got an exception")
        

def recordExtractor():
    ids2ret = []
    userCred = credParser()
    check = sessionInitiator(userCred['username'],userCred['password'],userCred['secret'])
    if(check):
        url = check.base_url.split('services', 1)[0]
        optyRecIdsQuery = "select id from opportunity"
        optyRecIds = check.query_all(optyRecIdsQuery)
        for op in optyRecIds['records'] :
            #print(op['Id'])
            ids2ret.append(url+op['Id'])
    
    return ids2ret

if __name__ == '__main__' :
    ids = recordExtractor()
    userCred = credParser()
    sb_url = userCred['sandbox_url'].split('services', 1)[0]
    pr_url = userCred['prod_url'].split('services', 1)[0]
    UsrLoginUrl = pr_url+'?startURL=%2Fhome%2Fhome.jsp&un='+userCred['username']+'&pw='+userCred['password']
    wb.open(UsrLoginUrl)
    time.sleep(60)
    
    for id in ids:
        print('[+] Opening :'+id)
        wb.open(id)
        time.sleep(30)
        
    os.system("taskkill /im chrome.exe /f")
    
    k=input("press close to exit")