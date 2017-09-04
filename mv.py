#coding=utf-8

import requests
from bs4 import BeautifulSoup
import re
import os
import time

'''
获取不同杂志的入口网址列表
'''
def get_area_list(url):
    resp=conn.get(url=url,timeout=5)
    soup=BeautifulSoup(resp.content)
    raw_list=soup.findAll('dt')
    area_list=[]
    for item in raw_list:
        if item.find('a'):
            area_list.append(item.find('a').get('href'))
    return area_list

'''
获取某一杂志的网页总页数
'''
def get_page_num(url):
    resp=conn.get(url=url,timeout=5)
    soup=BeautifulSoup(resp.content)
    _list=soup.findAll('span')
    page=0
    for item in _list:
        if item.has_attr('title'):
            ss = item.get('title')
            reg= re.compile(u'共(.+?)页')
            if reg.findall(ss):
                page=int(reg.findall(ss)[0].encode('utf8').strip())
                break
    return page

'''
为了获得页数，必须访问非图片模式网址
'''
def get_noPicMode(url):
    resp=conn.get(url=url,timeout=5)
    soup=BeautifulSoup(resp.content)
    _list=soup.findAll('a')
    url_noPicMode=''
    for item in _list:
        if item.has_attr('class'):
            if item.get('class')==['chked']:
                url_noPicMode= item.get('href')
    return url_noPicMode

'''
获得某一页所有写真集网址列表
'''
def get_album_list(url):
    resp=conn.get(url=url,timeout=5)
    soup=BeautifulSoup(resp.content)
    _list=soup.findAll('a')
    album_list=[]
    for item in _list:
        if item.has_attr('onclick'):
            if item.get('onclick')=='atarget(this)':
                album_list.append(item.get('href'))
    return album_list

'''
获得某一写真集所有图片的网址列表和该写真集名字
'''
def get_pic_list(url):
    resp=conn.get(url=url,timeout=5)
    soup=BeautifulSoup(resp.content)
    _list=soup.findAll('img')
    pic_list=[]
    for item in _list:
        if item.has_attr('file'):
            pic_list.append(item.get('file'))
    _list=soup.findAll('span')
    album_name='others'
    for item in _list:
        if item.has_attr('id'):
            if item.get('id')=='thread_subject':
                album_name = item.string
                break
    return pic_list,album_name

'''
下载并保存图片
'''
def download_pic(url,album_name,pic_num,local_path):
    local_filename = album_name
    r = conn.get(url, stream=True,timeout=5)
    s =local_filename.encode('utf-8').replace('/',' ').decode('utf-8')
    '''
    if not os.path.exists(local_path+s):
        os.makedirs(local_path+s)
    else:
        return s
    '''
    with open(local_path+s+'/'+str(pic_num)+'.jpg', 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()
    return s

'''
主程序流程:
    获得不同杂志的入口网址列表 -> 
    判断某一杂志的入口网址是否为无图模式，从而获得该杂志的网页总页数 ->
    获得某一杂志某一页的所有写真集入口网址列表 ->
    获得某一写真集所有图片的网址列表和该写真集名字 ->
    如果本地未存在该写真集，下载。
'''
if __name__=='__main__':
    local_path='c:/Users/mondon/Desktop/mv/' #自定义保存路径
    url_base='https://www.aisinei.com/' #网站基址
    log='error_log.txt' #记录访问时抛错的网址
    conn=requests.session() #创建session 传递cookie
    with open(local_path+log,'a') as fl:
        count=0
        url_list=[]
        while 1:
            count=count+1
            if count>10:
                time_now=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                fl.write(time_now+' : '+url_base+'\n')
                fl.flush()
                break
            try:
                url_list=get_area_list(url_base)
                break
            except:
                continue
        '''
        url_list=get_area_list(url_base)
        '''
        for i in range(len(url_list)):
            count=0
            url=''
            while 1:
                count=count+1
                if count>10:
                    time_now=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    fl.write(time_now+' : '+url_list[i]+'\n')
                    fl.flush()
                    break
                try:
                    if get_noPicMode(url_list[i]):
                        url=get_noPicMode(url_list[i])
                    else:
                        url=url_list[i]
                    break
                except:
                    continue
            '''
            if get_noPicMode(url_list[i]):
                url=get_noPicMode(url_list[i])
            else:
                url=url_list[i]
            '''
            count=0
            page=0
            while 1:
                count=count+1
                if count>10:
                    time_now=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    fl.write(time_now+' : '+url+'\n')
                    fl.flush()
                    break
                try:
                    page=get_page_num(url)
                    break
                except:
                    continue
            '''
            page=get_page_num(url)
            '''
            for j in range(page):
                url=url_list[i].replace('1',str(j+1))
                count=0
                url_list_1=[]
                while 1:
                    count=count+1
                    if count>10:
                        time_now=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                        fl.write(time_now+' : '+url+'\n')
                        fl.flush()
                        break
                    try:
                        url_list_1=get_album_list(url)
                        break
                    except:
                        continue
                '''
                url_list_1=get_album_list(url)
                '''
                for k in range(len(url_list_1)):
                    count=0
                    url_list_2=[]
                    while 1:
                        count=count+1
                        if count>10:
                            time_now=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                            fl.write(time_now+' : '+url_list_1[k]+'\n')
                            fl.flush()
                            break
                        try:
                            url_list_2,album_name=get_pic_list(url_list_1[k])
                            break
                        except:
                            continue

                    '''
                    url_list_2,album_name=get_pic_list(url_list_1[k])
                    '''
                    print '准备下载: '+album_name.encode('utf-8')
                    s =album_name.encode('utf-8').replace('/',' ').decode('utf-8')
                    if not os.path.exists(local_path+s):
                        os.makedirs(local_path+s)
                    else:
                        print ' '+album_name.encode('utf-8')+' 已存在'
                        continue
                    for m in range(len(url_list_2)):
                        count=0
                        while 1:
                            count=count+1
                            if count>10:
                                time_now=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                                fl.write(time_now+' : '+url_list_2[m]+'\n')
                                fl.flush()
                                break
                            try:
                                download_pic(url_list_2[m],album_name,m+1,local_path)
                                break
                            except:
                                continue
                        '''
                        download_pic(url_list_2[m],album_name,m+1,local_path)
                        '''
                        print m+1
        fl.close()


