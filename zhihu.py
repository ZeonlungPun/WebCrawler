from urllib.parse import urlencode
import requests,time,pymysql
from pyquery import PyQuery as pq
base_url='https://www.zhihu.com/api/v3/feed/topstory/recommend?action=down&ad_interval=-10&'

hearders={
    'Host':'www.zhihu.com',
    'Referer':'https://www.zhihu.com/',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'X-Requested-With': 'fetch'
}


"""
https://www.zhihu.com/api/v3/feed/topstory/recommend?action=down&ad_interval=-10&after_id=17&desktop=true&page_number=4&session_token=99d240845568636a04df4c9d664302a2
https://www.zhihu.com/api/v3/feed/topstory/recommend?action=down&ad_interval=-10&after_id=23&desktop=true&page_number=5&session_token=99d240845568636a04df4c9d664302a2
https://www.zhihu.com/api/v3/feed/topstory/recommend?action=down&ad_interval=-10&after_id=29&desktop=true&page_number=6&session_token=99d240845568636a04df4c9d664302a2
"""
def get_page(page_id,page_num):
    params={
        'after_id': page_id,
        'desktop': 'true',
        'page_number': page_num,
        'session_token': '99d240845568636a04df4c9d664302a2'
    }
    url=base_url+urlencode(params)
    try:
        response=requests.get(url,headers=hearders)
        if response.status_code==200:
            return response.json()
    except requests.ConnectionError as e:
        print('error',e.args)

def parse_page(json):
    if json:
        items=json.get('data')
        for item in items:
            try:
                zhihu={}
                zhihu['id']=item['id']
                zhihu['text']=item['target']['excerpt']
                zhihu['time']=item['created_time']
                zhihu['question']=item['target']['question']['title']
                zhihu['comment_count']=item['target']['comment_count']
                zhihu['favorite_count']=item['target']['favorite_count']
                yield zhihu
            except:
                zhihu = {}
                zhihu['id'] = item['id']
                zhihu['text'] = item['target']['excerpt']
                zhihu['time'] = item['created_time']
                zhihu['question'] = item['target']['title']
                zhihu['comment_count'] = item['target']['comment_count']
                zhihu['favorite_count'] = item['target']['favorite_count']
                yield zhihu

if __name__ == '__main__':
    #write to mysql
    db=pymysql.connect(db='mysql',host='localhost',user='debian-sys-maint',password='3yjakeY3wtKA5Kra', port=3306)
    cursor=db.cursor()
    #create table
    sql_init='create table if not exists zhihu (id varchar(25),question varchar(3000),text varchar(3000), comment_count int,favorite_count int ,time varchar(50))'
    cursor.execute(sql_init)

    page_id=17
    page_num=4
    #insert data row by row
    while True:
    #for page_id,page_num in zip(range(17,47,6),range(4,10)):
        json=get_page(page_id=page_id,page_num=page_num)
        results=parse_page(json)
        for result in results:
            print(result)
            sql='insert into zhihu(id,question, text,comment_count, favorite_count,time) values ( %s,%s,%s,%s,%s,%s)'
            cursor.execute(sql,(result['id'],result['question'] ,result['text'],result['comment_count'],  result['favorite_count'], result['time'] ) )
            db.commit()
        page_num=page_num+1
        page_id=page_id+6
        if page_num >30:
            break
        time.sleep(15)
    cursor.close()
    db.close()
