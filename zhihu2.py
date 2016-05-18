# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 14:29:47 2016

@author: Chieh Jow
"""

from bs4 import BeautifulSoup as bsp
import json, urllib2
import os
import time
import thread

from os import listdir
from os.path import isfile, join
import operator



def parse_voter_X(html):
    try:
        list = ""
        s = bsp(html, 'html.parser')
        list += s.a['href'][8:]
        list += ','+s.a['title']
        list += ','+s.span.text
        all = s.find_all('li')
        list += ',' + all[0].span.text.split(' ')[0]
        list += ',' + all[1].span.text.split(' ')[0]
        list += ',' + all[2].a.text.split(' ')[0] 
        list += ',' + all[3].a.text.split(' ')[0]
    except:
#        print(html.encode('utf-8'))
        pass
    return list    

def get_homepage_url_content(url):
    opener = urllib2.build_opener()
    Accept ='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    AcceptEncoding='utf-8'
    AcceptLanguage='zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2,ja;q=0.2'
    CacheControl='max-age=0'
    Connection='keep-alive'
    Cookie='d_c0="ACBArFMe6gmPToRtGU-dgMk0iEpK3kBsot8=|1463110246"; q_c1=3d0be77de6ad47c19d197f611305a810|1463110247000|1463110247000; cap_id="NTJkNGVkMDliODhkNDBhN2JjM2JlZDI2NDFiNGJjMWI=|1463110247|bb7a29a13c77739b8ad87d2b347cd8e7509a2207"; l_cap_id="NDE1NDZhMjdmYjczNDgxZjg2NmQwZWZiNDZkMjljZWY=|1463110247|dde2da7ccaf113be7b80ee2f3e568b75bb8bb585"; login="NDFjYTBhNzVjMjA5NGZiYzlmMDgyYzE0NmY0MzhiMjg=|1463110260|bd521b1597ca1e8d4ee6e33f945572ac9d3fa469"; z_c0=Mi4wQUJBS0VSaHZTZ2dBSUVDc1V4N3FDUmNBQUFCaEFsVk5kTmRjVndBYjh4aHlTQUdqTXo4QnRHaUNGeFZHRHUzV0pB|1463110260|386f1e355aee53dc230dce83441c29481d48e5a9; _zap=73bc2227-56e5-4dee-bc13-bbaaa9541f27; __utma=51854390.584015804.1463110243.1463183249.1463369825.3; __utmb=51854390.8.10.1463369825; __utmc=51854390; __utmz=51854390.1463369825.3.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=51854390.100--|2=registration_date=20150624=1^3=entry_date=20150624=1'
    
    Host='www.zhihu.com'
    UpgradeInsecureRequests='1'
    UserAgent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
    
    opener.addheaders.pop()
    opener.addheaders.append(('Accept',Accept ))
    opener.addheaders.append(('Accept-Encoding',AcceptEncoding ))
    opener.addheaders.append(('Accept-Language',AcceptLanguage ))
    opener.addheaders.append(('Cache-Control',CacheControl ))
    opener.addheaders.append(('Connection',Connection ))
    opener.addheaders.append(('Cookie',Cookie ))
    opener.addheaders.append(('Host',Host ))
    opener.addheaders.append(('Upgrade-Insecure-Requests',UpgradeInsecureRequests ))
    opener.addheaders.append(('User-Agent',UserAgent ))

    res = opener.open(url,timeout=20)
#    print res
#    res = urllib2.urlopen(url)
    return res.read()


def get_url_content(url):
    res = urllib2.urlopen(url,timeout=20)
    return res.read()



def get_votersprofile_id(url):
    try:
        url1=get_homepage_url_content(url)
        url2=bsp(url1,"html.parser").find_all("a",{"class":"zg-anchor-hidden"})
    except:
        url2=[]
    if url2==[]:
        return 10
    voter_id=url2[0].get("name")[7:]
    return voter_id
   

def get_answer_url(userid):
    base="https://www.zhihu.com/people/"
    url=base+userid
    try:
        data=get_homepage_url_content(url)
        
    except:
        return []
    beautiful=bsp(data,"html.parser")
    url1=beautiful.find_all("a",{"class":"question_link","target":"_blank"})
    ans_url=[]
    for content in url1:
        if content.get("href").find("answer")>0:
            ans_url=ans_url+[content.get("href")]
        else:
            continue
    return ans_url


def printtime(t):
    t=int(t)
    print "Estimated remaining time: "+str(t//3600)+"h "+str((t%3600)//60)+"m "+str(t%60)+"s"
    

def find_all_voter(url):
    base = 'https://www.zhihu.com'
    url1=base+url
    id=get_votersprofile_id(url1)
    t0=time.clock()
    if id==10:
        return [0]
    try:
        data = get_homepage_url_content('https://www.zhihu.com/answer/'+id+'/voters_profile')
    except:
        return [0]         

    j = json.loads(data.decode('utf-8'))
#    print j
    total = j['paging']['total']

    list = j['payload']
    
    if total <= 10:
        return j['payload']
    
    for i in range(0, total//10):
        if i >5000:
            return list
        url = base + j['paging']['next'];
        os.system("cls")
        t1=time.clock()
        t=(t1-t0)*((total-i*10)/(i*10+0.00001))
        printtime(round(t))
        print(url)
        
        try:
            data = get_url_content(url)
            j = json.loads(data.decode('utf-8'))
            list = list + j['payload']
        except:
            return list

    return list

def multi_thread(i,path):
    m=i
    i=i.split("/")
    k="_".join(i)
    filename=str(path+"\\data_"+k+".txt")
#        print os.path.isfile(filename)
    if not os.path.isfile(filename):
        list = find_all_voter(m)
        with open(filename, 'wb') as f:
            for j in list:
                parse=parse_voter_X(j)
                if parse=="":
                    continue
                f.write(parse.encode('utf-8')+'\r\n'.encode('utf-8'))
        f.close()



def make_bundle_thread(userid):
    path=userid
    if not os.path.exists(path):
        os.makedirs(path)
    total_answer=get_answer_url(userid)
    for i in total_answer:
        try:
           thread.start_new_thread( multi_thread, (i, path, ) )
        except:
           print "Error: unable to start thread"
 
    

def make_bundle(userid):
    path='suspicious\\'+userid
    if not os.path.exists(path):
        os.makedirs(path)
    total_answer=get_answer_url(userid)
    for i in total_answer:
        m=i
        i=i.split("/")
        k="_".join(i)
        filename=str(path+"\\data_"+k+".txt")
    #        print os.path.isfile(filename)
        if not os.path.isfile(filename):
            list = find_all_voter(m)
            with open(filename, 'wb') as f:
                for j in list:
                    parse=parse_voter_X(j)
                    if parse=="":
                        continue
                    f.write(parse.encode('utf-8')+'\r\n'.encode('utf-8'))
            f.close()


   
def compare_user(userid):
    path='suspicious\\'+userid
    filenames = [f for f in listdir(path) if isfile(join(path, f))]
    
    Hash={}
    for filename in filenames:

        data=open('suspicious\\'+userid+'\\' +filename,'r').readlines()
        filename='/'.join(filename[6:-4].split('_'))        
        
        for i in data:
            i=i.split(",")[0]
            if i in Hash:
                value=Hash[i]
                value[0]+=1
                value[1].append(filename)
                Hash.update({i:value})

            else:
                Hash.update({i:[1,[filename]]})
            
    
    sort_Hash=sorted(Hash.items(), key=operator.itemgetter(1))[::-1]
    return sort_Hash

#
def make_compared_text(userid):
    path='suspicious\\'+userid
    filenames = [f for f in listdir(path) if isfile(join(path, f))]
    if filenames==[]:
        return
    compared_data=open(path+'\\'+userid+'.txt','w')
    

    a=compare_user(userid)
    for i in a:
        if len(filenames)>5:
            if i[1][0]>2:
                i=str(i)
                compared_data.write(i+'\n')
        else:
            if i[1][0]>0:
                i=str(i)
                compared_data.write(i+'\n')
def find_user_folder():
    suspected_userid = [f for f in listdir('.\\'+'suspicious') if os.walk(join('.\\', f))]

    suspected_userid=[ x for x in suspected_userid if ".txt" not in x]
    suspected_userid=[ x for x in suspected_userid if ".py" not in x]
    suspected_userid=[ x for x in suspected_userid if ".pyc" not in x]
    suspected_userid=[ x for x in suspected_userid if "nonsuspected" not in x]
    return suspected_userid

def make_all_text():

    suspected_userid=find_user_folder()
    for i in suspected_userid:
        if not os.path.isfile('suspicious\\'+i+"\\"+i+".txt"):
            make_compared_text(i)
        else:
            continue

 
    

def ouput_sybil_list():
    sybil={}
    suspected_userid=find_user_folder()


    for i in suspected_userid:

        try:
            data=open('suspicious\\'+i+'\\' +i+'.txt','r').readlines()
        except:
            print "user :",i,"does not have the compared file"
            continue
        if data==[]:
            continue
        m=data[0][1:-2].split(',')[1][2:]
        m=int(m)
        if m<3:
            continue
        for j in data:
            if j=='':
                continue


            m_j=j[1:-2].split(',')[1][2:] 
            m_j=int(m_j)
            j=j[1:-2].split(',')[0][1:-1]
            
            if m_j<m/(1.4):
                continue
            if j==i:
                continue
            if j in sybil:
                value=sybil[j]
                value+=1
                sybil.update({j:value})
            else:
                sybil.update({j:1})
#    sybil=sorted(sybil.items(), key=operator.itemgetter(1))[::-1]
    return sybil
    


def deep_search_sybil_users():
    make_all_text()
    hash_dict=ouput_sybil_list()
    for i in hash_dict:
        if hash_dict[i]==2:
             make_bundle(i)
    make_all_text()
    print ouput_sybil_list()
    
#make_all_text()   
deep_search_sybil_users()
#print ouput_sybil_list()
    

    
    
    
    
