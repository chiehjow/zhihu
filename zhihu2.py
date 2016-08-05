# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 14:29:47 2016

@author: Chieh Jow
"""

from bs4 import BeautifulSoup as bsp
import json, urllib2,urllib
import os
import time
import thread

from os import listdir
from os.path import isfile, join
import operator
import networkx as nx
import matplotlib.pyplot as plt







global folder_name
global Cookie






folder_name="suspicious"

Cookie= '_za=544017bc-8400-485a-9d01-d41b380402a9; d_c0="ACBArFMe6gmPToRtGU-dgMk0iEpK3kBsot8=|1463110246"; _zap=73bc2227-56e5-4dee-bc13-bbaaa9541f27; q_c1=3d0be77de6ad47c19d197f611305a810|1468631021000|1463110247000; _xsrf=532e15c8360e3b36ec2cfbff13d98695; l_cap_id="ZGZhMzZhOTlhNDA2NDA4ZWJhYTU1NmNhZjY2ODQ3Nzc=|1468631020|5e52968a9feb4fd991be058c03ddfb24826c0e98"; cap_id="OGNjOGNjNTU0MmNhNGEwNGJkYzM0M2MyMTlhMWEyMTY=|1468631020|6ccf72ed789f081435a0a06e2d8b13c64b82962e"; login="ODA5NzBlNDA0NmMxNDVmMzlmMGI0ZDkyNjhiYzFkZmM=|1468631034|5cb925fd19eeafd080d9639db03ef7465a2d2e99"; z_c0=Mi4wQUJBS0VSaHZTZ2dBSUVDc1V4N3FDUmNBQUFCaEFsVk4taFN4VndDZ1N0XzltTXVDXzA5c0pHVkQtTlJYVmJTcEZ3|1468631034|ed574f144a2a48a28f59594dc4e519bfd6dd8ade; n_c=1; a_t="2.0ABAKERhvSggXAAAATxWxVwAQChEYb0oIACBArFMe6gkXAAAAYQJVTfoUsVcAoErf_ZjLgv9PbCRlQ_jUV1W0qRfHalYBn-HIDTtx-v1r6epo95QV_w=="; __utmd=1; __utma=51854390.1991766914.1467075738.1468959872.1468959872.12; __utmb=51854390.1.9.1468965218847; __utmc=51854390; __utmz=51854390.1468959872.11.7.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/38de-yu-wen-ni-shang-bu-qi; __utmv=51854390.100--|2=registration_date=20150624=1^3=entry_date=20150624=1'



def parse_voter(html):
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
    
def parse_voter_A(html):
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
    return list.split(",")    
    
    
    
    
    
    

def get_homepage_url_content(url):
    opener = urllib2.build_opener()
    Accept ='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    AcceptEncoding='utf-8'
    AcceptLanguage='zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2,ja;q=0.2'
    CacheControl='max-age=0'
    Connection='keep-alive'
#    Cookie='_za=544017bc-8400-485a-9d01-d41b380402a9; d_c0="ACBArFMe6gmPToRtGU-dgMk0iEpK3kBsot8=|1463110246"; _zap=73bc2227-56e5-4dee-bc13-bbaaa9541f27; q_c1=3d0be77de6ad47c19d197f611305a810|1468631021000|1463110247000; _xsrf=532e15c8360e3b36ec2cfbff13d98695; l_cap_id="ZGZhMzZhOTlhNDA2NDA4ZWJhYTU1NmNhZjY2ODQ3Nzc=|1468631020|5e52968a9feb4fd991be058c03ddfb24826c0e98"; cap_id="OGNjOGNjNTU0MmNhNGEwNGJkYzM0M2MyMTlhMWEyMTY=|1468631020|6ccf72ed789f081435a0a06e2d8b13c64b82962e"; login="ODA5NzBlNDA0NmMxNDVmMzlmMGI0ZDkyNjhiYzFkZmM=|1468631034|5cb925fd19eeafd080d9639db03ef7465a2d2e99"; z_c0=Mi4wQUJBS0VSaHZTZ2dBSUVDc1V4N3FDUmNBQUFCaEFsVk4taFN4VndDZ1N0XzltTXVDXzA5c0pHVkQtTlJYVmJTcEZ3|1468631034|ed574f144a2a48a28f59594dc4e519bfd6dd8ade; n_c=1; a_t="2.0ABAKERhvSggXAAAATxWxVwAQChEYb0oIACBArFMe6gkXAAAAYQJVTfoUsVcAoErf_ZjLgv9PbCRlQ_jUV1W0qRfHalYBn-HIDTtx-v1r6epo95QV_w=="; __utmd=1; __utma=51854390.1991766914.1467075738.1468959872.1468959872.12; __utmb=51854390.1.9.1468965218847; __utmc=51854390; __utmz=51854390.1468959872.11.7.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/38de-yu-wen-ni-shang-bu-qi; __utmv=51854390.100--|2=registration_date=20150624=1^3=entry_date=20150624=1'
    
    
    Host='www.zhihu.com'
    UpgradeInsecureRequests='1'
    UserAgent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
    
    
    
    
    
 
#    ContentLength= '55'
#    Accept= '*/*'
#    Origin= 'https://www.zhihu.com'
#    XRequestedWith= 'XMLHttpRequest'
    
 
#    ContentType= 'application/x-www-form-urlencoded; charset=UTF-8'
#    Referer= 'https://www.zhihu.com/people/'+userid
    


    
    
    
    
    
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
#    opener.addheaders.append(('Content-Length',ContentLength ))
#    opener.addheaders.append(('Accept',Accept ))
#    opener.addheaders.append(('Origin',Origin ))
#    opener.addheaders.append(('X-Requested-With',XRequestedWith ))
#    opener.addheaders.append(('Content-Type',ContentType ))
#    opener.addheaders.append(('Referer',Referer ))
  

    res = opener.open(url)
#    print res
#    res = urllib2.urlopen(url)
    return res.read()


def get_url_content(url):
    res = urllib2.urlopen(url)
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
  
  
  
  
def get_all_profile(userid,datatime):

    base="https://www.zhihu.com/people/"
    url=base+userid+"/activities"
 
    headers={
    'Host': 'www.zhihu.com',
    'Connection': 'keep-alive',
    'Content-Length': '55',
    'Accept': '*/*',
    'Origin': 'https://www.zhihu.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'https://www.zhihu.com/people/'+userid,
    'Accept-Encoding': 'utf-8',
    'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2,ja;q=0.2',
    'Cookie': Cookie
    }
    
    form={
    'start':datatime,
    '_xsrf':'cd0cef0103d596c37415185aaad6f8ff'
    }

    
    
    
    
    data = urllib.urlencode(form)
    req = urllib2.Request(url, data, headers)
#    req = urllib2.Request(url, data)

    response = urllib2.urlopen(req)
    the_page = response.read()
    j=json.loads(the_page.decode('utf-8'))
#    print j
    new_page=" ".join(j['msg'][1:])
    return new_page
  

def get_answer_url(userid):
    base="https://www.zhihu.com/people/"
    url=base+userid
    try:
        data=get_homepage_url_content(url)
        
    except:
        return []

    beautiful=bsp(data,"html.parser")
    url1=beautiful.find_all("a",{"class":"question_link","target":"_blank"})
    url2=beautiful.find_all("div",{"class":"zm-profile-section-item zm-item clearfix","data-type-detail":"member_voteup_answer"})
    try:     
        last_datatime=url2[-1].get("data-time")
    except:
        return []
#    print url1
    url3=beautiful.find_all("div",{"class":"zh-profile-account-status"})
    if url3==[]:  
        isbanned = False
    else:
        isbanned = True
    max_len=100
 
    ans_url=[]
    while(url2!=[] and len(ans_url)<=max_len):
        for content in url1:
            if content.get("href").find("answer")>0:
                ans_url=ans_url+[content.get("href")]
            else:
                continue
        try:
            data=get_all_profile(userid,last_datatime)
        except:
            return ans_url
        beautiful=bsp(data,"html.parser")            
        url1=beautiful.find_all("a",{"class":"question_link","target":"_blank"})
        url2=beautiful.find_all("div",{"class":"zm-profile-section-item zm-item clearfix","data-type-detail":"member_voteup_answer"})
        try:
            last_datatime=url2[-1].get("data-time") 
        except:
            return ans_url

    return ans_url

#userid='liu-si-yu-69-44'
#get_all_profile(userid)
#a=get_answer_url(userid)






def filter_user(userid):
    base="https://www.zhihu.com/people/"
    url=base+userid
    asks="/people/"+userid+"/asks"
    answers="/people/"+userid+"/answers"
    posts="/people/"+userid+"/posts"
    collections="/people/"+userid+"/collections"
    logs="/people/"+userid+"/logs"
    
    try:
        data=get_homepage_url_content(url)
    except:
        print "user:",userid,"need to reconnect."
    beautiful=bsp(data,"html.parser")
    url1=beautiful.find_all("a",{"class":"item","href":asks})[0].span.string
    url2=beautiful.find_all("a",{"class":"item","href":answers})[0].span.string
    url3=beautiful.find_all("a",{"class":"item","href":posts})[0].span.string
    url4=beautiful.find_all("a",{"class":"item","href":collections})[0].span.string
    url5=beautiful.find_all("a",{"class":"item","href":logs})[0].span.string
    
    
    return [int(url1),int(url2),int(url3),int(url4),int(url5)]

#a=filter_user("five-81-72")
#print a

#a=get_answer_url("xiao-lei-71-89")



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





def convert_sci(string):
    try:
        s=int(string)
     
    except:
        try:
            s_last=string.lower()[-1]
            s_pre=string.lower()[:-1]
            s_pre=float(s_pre)
            if s_last=="k":
                mod_str=s_pre*1000
            elif s_last=="m":
                mod_str=s_pre*1000000
            elif s_last=="g":
                mod_str=s_pre*1000000000
            elif s_last=="t":
                mod_str=s_pre*1000000000000
            else:
                mod_str=string  
            s=int(mod_str)
        except:
            print "Input must be SI prefix."
            return "Non SI"

    return str(s)





def find_sybil_in_answer(ansurl): 
    i=ansurl.split("/")
    k="_".join(i)
    path="answer_base"+"\\"+k
    filename=path+"\\"+k+".txt"
    if not os.path.isfile(filename):    
        ans1=find_all_voter(ansurl)
        ans_list=[]
        
        for i in ans1:
    
            x=parse_voter_A(i)
            if len(x)<4:
                continue
            x=[x[0]]+x[-4:]
            for j in range(1,len(x[1:])+1):
                x[j]=convert_sci(x[j])
    
            x=",".join(x)
            ans_list+=[x]
        
        if not os.path.exists(path):
            os.makedirs(path)
        if not os.path.isfile(filename):
            user=open(filename,"wb")
            for i in ans_list:
                user.write(i+"\r\n")
            user.close()
    upvote=open(filename,"r").readlines()
    for i in upvote:
        user_data=i.split(",")
        u=user_data[0]
        filt=user_data[1:]
        four_zero=map(int,filt)
        dicision=sum(four_zero)
        if dicision!=0:
            continue
            
        print "Crawling user: ",u

        if not os.path.isfile(path+"\\"+u+".txt"):
            user_upvote=open(path+"\\"+u+".txt","wb")
            #crawling user up-voted data
            total_answer=get_answer_url(u)
            for j in total_answer:
                user_upvote.write(j+"\r\n")
            user_upvote.close()
                
      

#s=get_answer_url("a-jiu-change")



def compare_answer(answer):
    path="answer_base"+"\\"+answer
    filenames = [f for f in listdir(path) if isfile(join(path, f))]
    compare_answer_name=answer+"_compare"
    try:
        filenames.remove(answer+".txt")
        filenames.remove(compare_answer_name+".txt")
    except:
        pass
    
    Hash={}
    for filename in filenames:

        data=open(path+'\\' +filename,'r').readlines()      
        
        for i in data:
            j=i[:-2]
            if j in Hash:
                value=Hash[j]
                value[0]+=1
                value[1].append(filename)
                Hash.update({j:value})

            else:
                Hash.update({j:[1,[filename]]})
            
    
    sort_Hash=sorted(Hash.items(), key=operator.itemgetter(1))[::-1]
    return sort_Hash




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
                parse=parse_voter(j)
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
 






def make_bundle_user(userid, folder):
    path=folder+'\\'+userid
    if not os.path.exists(path):
        os.makedirs(path)
    total_answer=get_answer_url(userid)
    for i in total_answer:
        m=i
        i=i.split("/")
        k="_".join(i)
        filename=str(path+"\\"+k+".txt")
    #        print os.path.isfile(filename)
        if not os.path.isfile(filename):
            list = find_all_voter(m)
            with open(filename, 'wb') as f:
                for j in list:
                    parse=parse_voter(j)
                    if parse=="":
                        continue
                    f.write(parse.encode('utf-8')+'\r\n'.encode('utf-8'))
            f.close()




   
def compare_user(userid):
    path=folder_name+'\\'+userid
    filenames = [f for f in listdir(path) if isfile(join(path, f))]
    try:
        
        filenames.remove(userid+"_compare.txt")
        filenames.remove(userid+"_compare_zero.txt")
        filenames.remove(userid+".txt")
    except:
        pass
    
    Hash={}
    for filename in filenames:

        data=open(folder_name+'\\'+userid+'\\' +filename,'rb').read()
        if data=="":
            continue
        filename='/'.join(filename[:-4].split('_'))        
        data=data.split("\r\n")

        for i in data:
            user_data=i.split(",")
            IV_zero=user_data[-4:]
            if IV_zero==[""]:
                continue
            for x in range(len(IV_zero)):
                IV_zero[x]=convert_sci(IV_zero[x])
            try:
                four_zero=map(int,IV_zero)
            except:
                continue
#            dicision=sum(four_zero)
            
            
            #the following used for filter out non-four-zero users
#            if dicision!=0:
#                continue
            i=user_data[0]
            if i in Hash:
                value=Hash[i]
                value[0]+=1
                value[1].append(filename)
                Hash.update({i:value})

            else:
                Hash.update({i:[1,[filename]]})
            
    
    sort_Hash=sorted(Hash.items(), key=operator.itemgetter(1))[::-1]
    return sort_Hash



def compare_user_zero(userid):
    path=folder_name+'\\'+userid
    filenames = [f for f in listdir(path) if isfile(join(path, f))]
    try:
        
        filenames.remove(userid+"_compare.txt")
        filenames.remove(userid+"_compare_zero.txt")
        filenames.remove(userid+".txt")
    except:
        pass
    
    Hash={}
    for filename in filenames:

        data=open(folder_name+'\\'+userid+'\\' +filename,'rb').read()
        if data=="":
            continue
        filename='/'.join(filename[:-4].split('_'))        
        data=data.split("\r\n")

        for i in data:
            user_data=i.split(",")
            IV_zero=user_data[-4:]
            if IV_zero==[""]:
                continue
            for x in range(len(IV_zero)):
                IV_zero[x]=convert_sci(IV_zero[x])
            try:
                four_zero=map(int,IV_zero)
            except:
                continue
            dicision=sum(four_zero)
            
            
            #the following used for filter out non-four-zero users
            if dicision!=0:
                continue
            i=user_data[0]
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
def make_compared_text(compare_file,folder_name,compare_type):
    path=folder_name+'\\'+compare_file
    filenames = [f for f in listdir(path) if isfile(join(path, f))]
    compare_answer_name=compare_file+"_compare"
    try:
        filenames.remove(compare_answer_name+".txt")
        filenames.remove(compare_file+"_compare_zero.txt")
        filenames.remove(compare_file+".txt")
    except:
        pass
        
      
    if filenames==[]:
        return
    compared_data=open(path+'\\'+compare_answer_name+'.txt','w')
    compared_data2=open(path+'\\'+compare_answer_name+'_zero.txt','w')
    
    if compare_type=="user":
        a=compare_user(compare_file)
        b=compare_user_zero(compare_file)
    elif compare_type=="answer":
        a=compare_answer(compare_file)
    else:
        print "compare_type should be 'user' or 'answer'."
        return
    for i in b:
        if len(filenames)>5:
            if i[1][0]>1:
                i=str(i)
                compared_data2.write(i+'\r\n')
        else:
            if i[1][0]>0:
                i=str(i)
                compared_data2.write(i+'\r\n')
    compared_data2.close()       
    
    for i in a:
        if len(filenames)>5:
            if i[1][0]>1:
                i=str(i)
                compared_data.write(i+'\r\n')
        else:
            if i[1][0]>0:
                i=str(i)
                compared_data.write(i+'\r\n')
    compared_data.close()
#find_sybil_in_answer("/question/48445383/answer/111438555")   
#make_compared_text("_question_48445383_answer_111438555","answer_base","answer")


     
def find_user_folder():
    suspected_userid = [f for f in listdir('.\\'+ folder_name) if os.walk(join('.\\', f))]

    suspected_userid=[ x for x in suspected_userid if ".txt" not in x]
    suspected_userid=[ x for x in suspected_userid if ".py" not in x]
    suspected_userid=[ x for x in suspected_userid if ".pyc" not in x]
    suspected_userid=[ x for x in suspected_userid if "nonsuspected" not in x]
    return suspected_userid

def make_all_text():

    suspected_userid=find_user_folder()
    for i in suspected_userid:
        make_compared_text(i,folder_name,"user")
        if not os.path.isfile(folder_name+'\\'+i+"\\"+i+".txt"):
            make_compared_text(i,folder_name,"user")
        else:
            continue

 
    

def ouput_sybil_list():
    sybil={}
    suspected_userid=find_user_folder()
    G=nx.Graph()
    sybil_zero_color={}

    for i in suspected_userid:

        try:
            data=open(folder_name+'\\'+i+'\\' +i+'_compare.txt','rb').readlines()
            data2=open(folder_name+'\\'+i+'\\' +i+'_compare_zero.txt','rb').readlines()
        except:
            print "user :",i,"does not have the compared file"
            continue
        if data==[] or data2==[]:
            continue
        m=data[0][1:-2].split(',')[1][2:]
        m=int(m)
        if m<1:
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
            G.add_edge(i,j)
            if j in sybil:
                value=sybil[j]
                value+=1
                sybil.update({j:value})
            else:
                sybil.update({j:1})
        for k in data2:
            if k=='':
                continue
            k=k[1:-2].split(',')[0][1:-1]
            sybil_zero_color.update({k:"red"})                

    values = [sybil_zero_color.get(node, "green") for node in G.nodes()]
    print sybil_zero_color
    
    nx.draw(G, cmap=plt.get_cmap('jet'), node_color=values,with_labels = False, node_size=100)
    plt.show()




      
        
#    nx.draw(G,with_labels = False)
#    plt.savefig("induced_graph.png",dpi=1000) # save as png
    sybil=sorted(sybil.items(), key=operator.itemgetter(1))[::-1]
    return sybil
    

def deep_search_sybil_users():
    make_all_text()
    hash_dict=ouput_sybil_list()
    for i in hash_dict:
        if hash_dict[i]==1:
             make_bundle_user(i,folder_name)
    make_all_text()
    print ouput_sybil_list()

#a=ouput_sybil_list()
#b={}
#for i in a:
#    if a[i]!=1:
#        b.update({i:a[i]})
#print len(b)




    
#make_all_text()
#for i in range(3):
#deep_search_sybil_users()
#make_all_text()
#ouput_sybil_list()


    
    
    
    
