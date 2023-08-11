from urllib.parse import urlencode
import requests,time,pymysql
from pyquery import PyQuery as pq
base_url='https://m.weibo.cn/api/container/getIndex?'

hearders={
    'Host':'m.weibo.cn',
    'Referer':'https://m.weibo.cn/u/5598574734',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


"""
Request URL: https://m.weibo.cn/api/container/getIndex?type=uid&value=5598574734&containerid=1076035598574734&since_id=4882192871981297

4916595404838131
4909581467124857
4899788716249977
4890154634580107
4882192871981297
"""
def get_page(since_id):
    params={
        'type':'uid',
        'value':'5598574734',
        'containerid':'1076035598574734',
        'since_id':str(since_id)
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
        items=json.get('data').get('cards')
        for item in items:
            item=item.get('mblog')
            weibo={}
            weibo['id']=item.get('id')
            weibo['text']=pq(item.get('text')).text()
            weibo['attitudes']=item.get('attitudes_count')
            weibo['comments']=item.get('comments_count')
            weibo['date']=item.get('created_at')
            yield weibo

if __name__ == '__main__':
    #write to mysql
    db=pymysql.connect(db='mysql',host='localhost',user='debian-sys-maint',password='3yjakeY3wtKA5Kra', port=3306)
    cursor=db.cursor()
    #create table
    sql_init='create table if not exists shan_wb (id varchar(25),text varchar(300), attitudes int,comments int ,date varchar(50))'
    cursor.execute(sql_init)

    since_id = [4916595404838131, 4909581467124857, 4899788716249977, 4874483498747923, 4882192871981297]
    #insert data row by row
    for s_id in since_id:
        json=get_page(s_id)
        results=parse_page(json)
        for result in results:
            print(result)
            sql='insert into shan(id,text, attitudes,comments,date) values ( %s,%s,%s,%s,%s)'
            cursor.execute(sql,(result['id'], result['text'][:80],result['attitudes'],  result['comments'], result['date'] ) )
            db.commit()
        time.sleep(15)
    cursor.close()
    db.close()
