import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
def get_page(offset):
    url='https://www.maoyan.com/board/4?offset='+str(offset)
    headers={
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'cookie':'__mta=212260395.1685276503151.1685282050639.1685289982126.20; uuid_n_v=v1; uuid=34297070FD5211EDA656FD7ECF47D2294BDDBC3C10A6434999E8E14671C417A9; _csrf=68faa9a5751c483ef9f2ee7406915c0b23cbc9bc8b4c0902d617f17dd9ec0baa; _lxsdk_cuid=188624eaa49c8-0515bc8551dd4b-15462c6c-384000-188624eaa49c8; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1685276503; WEBDFPID=v181yy99x41x5z8v04w711ywyvxyxv4w81137383372979583x013vy3-2000637730356-1685277729831KKGQAACa12a6b8169ee7736639f3ec62dbf984b3416; token=AgHMJYKoHJy2RxYqUuAiPs0Wtn1rGvTgqVQ88RewR7EH75H-ZKD7qUB32s7p4e5MdnnB39UncJYTmAAAAADFGAAA2RCpjqc-WJaKao92KgyKIDuRY0lr4p5-zt_cepX4fCeViIqfK_2HhEHderePzE1b; uid=2329047950; uid.sig=dYylqAJn9FN7yif5og2h5_w-LRs; _lxsdk=34297070FD5211EDA656FD7ECF47D2294BDDBC3C10A6434999E8E14671C417A9; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1685289982; _lxsdk_s=188631c5839-0d0-f00-6ab%7C%7C2'
    }
    response=requests.get(url,headers=headers)
    if response.status_code==200:
        return response.text



def get_data(html):
    soup=BeautifulSoup(html,'html.parser')
    names=soup.select('.name a')
    times=soup.select('.releasetime')
    stars=soup.select('.star')

    df=pd.DataFrame()

    for name,time,star in zip(names,times,stars):
        name=name.get_text()
        time = time.get_text()
        time = re.findall('上映时间：(.*)', time, re.S)[0].rstrip()
        star=star.get_text()
        star=re.findall('主演：(.*)', star, re.S)[0].rstrip()
        arr=np.array([name,time,star]).reshape((1,-1))
        df_=pd.DataFrame(arr,columns=['film_name','time','actors'],index=None)
        df=pd.concat([df,df_],axis=0)

    return df

data=pd.DataFrame()
for i in range(0,50):
    html=get_page(offset=i*10)
    df=get_data(html)
    data=pd.concat([data,df],axis=0)
    time.sleep(10)

print(data)

