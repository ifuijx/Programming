from bs4 import BeautifulSoup
import requests
import urllib
from urllib import request
import os
import time


class FirstSpider:
    def __init__(self, root_dir, root_url, base_url, depth):
        self._root_dir = root_dir
        self._root_url = root_url
        self._base_url = base_url
        self._depth = depth


    def run(self):
        count = 0
        cur_url = self._root_url
        while count < self._depth:
            print('cur_url:', cur_url)
            print()

            targets = self._get_picture_group(cur_url)
            
            for title, url in targets:
                url = self._base_url + url
                print(title)
                pic_urls = self._get_picture_urls(url)

                dest_dir = os.path.join(self._root_dir, title)
                if not os.path.exists(dest_dir):
                    os.mkdir(dest_dir)
                else:
                    continue

                self._download_pictures(pic_urls, dest_dir)
            
            get_url = self._get_next_url(cur_url)
            if get_url:
                cur_url = self._base_url + get_url
            else:
                break
            
            print()
            count += 1
    

    def _get_picture_group(self, url):
        soup = self._get_soup(url)

        tags = soup.find_all('div', attrs={'class': 'il_img'})
        targets = [(tag.a['title'], tag.a['href']) for tag in tags]
        
        return targets


    def _get_picture_urls(self, url):
        soup = self._get_soup(url)

        tags = soup.find_all('div', attrs={'class': 'il_img'})
        targets = [tag.img['src'] for tag in tags]

        return targets
    

    def _get_next_url(self, url):
        soup = self._get_soup(url)

        tags = soup.find_all('a', attrs={'class': 'page-next'})
        
        if not tags:
            return None
        
        return tags[0]['href']
    

    def _download_pictures(self, img_urls, dest_dir):
        count = 1
        for img_url in img_urls:
            req = request.Request(img_url)
            try:
                get_img = request.urlopen(req).read()
            except urllib.error.HTTPError as err:
                print('download error', img_url, err)
                continue
        
            with open(os.path.join(dest_dir, str(count) + '.jpg'), 'wb') as fp:
                fp.write(get_img)
            
            count += 1
    

    def _get_soup(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup


if __name__ == '__main__':
    spider = FirstSpider(r'E:\test', r'http://www.ivsky.com/tupian/', r'http://www.ivsky.com', 3)
    begin = time.clock()
    spider.run()
    end = time.clock()
    print('consume time', end - begin, 'seconds')
