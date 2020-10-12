import requests
import json
import time
#from configs import *


def get_organ_id(stockId):
    # 巨潮资讯网站
    _req = requests.post(
        'http://www.cninfo.com.cn/new/information/topSearch/query?keyWord=' + str(stockId) + '&maxNum=10')
    if not _req.status_code == 200:
        raise _req
    # response.json()的作用就是将API页面的json转化为字典
    data = _req.json()
    # 返回orgid
    return data[0]['orgId']


def search(keyword, page=1, limit=20):
    org_id = get_organ_id(keyword)
    target_url = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'
    params = {
        'stock': str(keyword) + ',' + str(org_id),
        'pageSize': limit,
        'pageNum': page
    }
    _req = requests.post(target_url, data=params)

    if _req.status_code != 200:
        raise Exception('Post Error')
    if _req.headers['Content-Type'] != 'application/json;charset=UTF-8':
        raise Exception('API Failed')

    data = _req.json()
    prefix = 'http://static.cninfo.com.cn/%s'
    announcements = data['announcements']
    return [{
        'time': time.strftime("%Y-%m-%d", time.localtime(n['announcementTime'] / 1000)),
        'title': n['announcementTitle'],
        'pdf_path': lambda: prefix % n['adjunctUrl']
    } for n in announcements]


if __name__ == '__main__':
    result = search('601668')
    print(result)
