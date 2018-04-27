from bs4 import BeautifulSoup
import asyncio
import aiohttp
import os
import time


class SecondSpider:
    def __init__(self, root_dir, root_url, base_url, depth, loop):
        self._root_dir = root_dir
        self._root_url = root_url
        self._base_url = base_url
        self._depth = depth
        self._loop = loop
    

    async def run(self):
        count = 0
        cur_url = self._root_url
        while count < self._depth:
            print('cur_url:', cur_url)
            print()

            targets = await self._get_picture_group(cur_url)

            for title, url in targets:
                url = self._base_url + url
                print(title)
                pic_urls = await self._get_picture_urls(url)

                dest_dir = os.path.join(self._root_dir, title)
                if not os.path.exists(dest_dir):
                    os.mkdir(dest_dir)
                else:
                    continue
                
                await self._download_pictures(pic_urls, dest_dir)
            
            get_url = await self._get_next_url(cur_url)
            if get_url:
                cur_url = self._base_url + get_url
            else:
                break
            
            print()
            count += 1
    

    async def _get_picture_group(self, url):
        soup = await self._get_soup(url)

        tags = soup.find_all('div', attrs={'class': 'il_img'})
        targets = [(tag.a['title'], tag.a['href']) for tag in tags]

        return targets
    

    async def _get_picture_urls(self, url):
        soup = await self._get_soup(url)

        tags = soup.find_all('div', attrs={'class': 'il_img'})
        targets = [tag.img['src'] for tag in tags]

        return targets
    

    async def _get_next_url(self, url):
        soup = await self._get_soup(url)

        tags = soup.find_all('a', attrs={'class': 'page-next'})

        if not tags:
            return None
        
        return tags[0]['href']
    

    async def _download_pictures(self, img_urls, dest_dir):
        async with aiohttp.ClientSession() as session:
            length = len(img_urls)
            file_names = [os.path.join(dest_dir, str(i+1)) + '.jpg' for i in range(length)]
            await asyncio.gather(
                *[self._download_picture(session, img_urls[i], file_names[i]) for i in range(length)]
            )

    

    async def _download_picture(self, session, url, filename):
        try:
            async with session.get(url) as response:
                with open(filename, 'wb') as fp:
                    content = await response.content.read()
                    fp.write(content)
                return await response.release()
        except aiohttp.ClientError as err:
            print('get picture error', url, err)
            

    async def _get_soup(self, url):
        try:
            async with aiohttp.ClientSession(loop=self._loop) as session:
                async with session.get(url) as response:
                    text = await response.text()
                    await response.release()
                    return BeautifulSoup(text, 'html.parser')
        except aiohttp.ClientError as err:
            print('get text error', url, err)
    

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    spider = SecondSpider(r'E:\test', r'http://www.ivsky.com/tupian/', r'http://www.ivsky.com', 3, loop)
    begin = time.clock()
    loop.run_until_complete(spider.run())
    end = time.clock()
    print('consume time', end - begin, 'seconds')