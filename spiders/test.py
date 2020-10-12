import spiders.cninfo as spider

if __name__ == '__main__':
    result = spider.search('601668')
    for r in result:
        print(r['title'])
        print(r['time'])
        print(r['pdf_path']())
        print()
