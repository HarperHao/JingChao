import requests
import json
from bs4 import BeautifulSoup
from configs import *

search_api = east_money_api

config = {
    'Referer': east_money_refer,
    'User-Agent': user_agent,
    'Host': east_money_host
}


def search(keyword, page=1, limit=20):
    target_api = search_api % (page, limit, keyword)
    req = requests.post(target_api, headers=config)
    if req.status_code != 200:
        raise Exception('Post Failed')
    else:
        result = json.loads(req.text)
        if 'IsSuccess' not in result or 'Data' not in result:
            raise Exception('Invalid result')
        elif not result['IsSuccess']:
            raise Exception('Result failed')

    data = result['Data']
    # NoticeTitle - Title
    # Url - html page
    # NoticeDate - Date
    _ret = []
    for inform in data:
        tmp = {'title': inform['NoticeTitle'],
               'time': inform['NoticeDate']}

        def inner(url):
            def closure():
                _req = requests.get(url)
                if _req.status_code != 200:
                    raise Exception('Get Failed')
                soup = BeautifulSoup(_req.text, 'html.parser')
                hyper = soup.select_one('.detail-header a')
                if hyper is not None:
                    raw_url = hyper.attrs['href']
                    tar_url = 'https://pdf.dfcfw.com/pdf/%s' % raw_url.split('/')[-1]
                    # print(tar_url)
                    return tar_url
                    # return hyper.attrs['href']
            return closure

        # raw_url = inner(inform['Url'])

        # url = 'https://pdf.dfcfw.com/pdf/%s' % raw_url

        tmp['pdf_path'] = inner(inform['Url'])
        _ret.append(tmp)
    return _ret


if __name__ == '__main__':
    results = search('601668')
    print(len(results))
