from rotate_proxy import RotateProxy
from bs4 import BeautifulSoup
import cloudscraper
import time

class SahibindenCloudScraper:
    WINDOW_SIZE = 50

    def __init__(self, website_url:str, starting_page:int, ending_page:int) -> None:
        self.website_url = website_url
        self.starting_page = starting_page
        self.ending_page = ending_page
        self.page_urls = []
        self.ad_urls = []

        # change proxy
        rotate_proxy = RotateProxy(used_proxy=None)
        self.proxy, self.seleniumwire_options, self.proxies = rotate_proxy.change_proxy()

        # run app
        self.main()

    
    def main(self):
        try:
            self._create_page_urls()
            self.scraper = cloudscraper.CloudScraper()
            self.scrape_ad_urls()
            self.scrape_ad_info()
        except KeyboardInterrupt:
            print('durduruldu')

    def scrape_ad_info(self):
        for ad_url in self.ad_urls:
            soup = self._send_request_until_valid_response(url=ad_url)

            info_box = soup.find('div', attrs={'class':'classifiedOtherBoxes'})
            try:
                firm = info_box.find('span', attrs={'class':'storeInfo classified-edr-real-estate'}).getText()
                
            except:
                firm = '-'
            finally:
                print(firm)

            try:
                phone = info_box.find('span', attrs={'class':'pretty-phone-part show-part'}).getText()
                
            except:
                phone = '-'
            finally:
                print(phone)

            print('\n-------------------------------------\n')


            time.sleep(3)


    def scrape_ad_urls(self):
        for page_url in self.page_urls:
            soup = self._send_request_until_valid_response(url=page_url)

            tbody_tag = soup.find('tbody', attrs={'class':'searchResultsRowClass'})
            tr_tags = tbody_tag.find_all('tr', attrs={'class':'searchResultsItem'})

            for tr_tag in tr_tags:
                try:
                    self.ad_urls.append('http://www.sahibinden.com'+ str(tr_tag.find('a').get('href')))
                except:
                    pass

        for ad_url in self.ad_urls:
            print(ad_url)
        print(len(self.ad_urls))


    def _create_page_urls(self):
        for page_no in range(self.starting_page, ending_page + 1):
            self.page_urls.append(f'{self.website_url}?pagingOffset={(page_no - 1) * 50}&pagingSize={self.WINDOW_SIZE}')


    def _send_request_until_valid_response(self, url:str, is_proxy:bool=False) -> BeautifulSoup | None:
        for i in range(1, 10):
            if i % 5 == 0:
                rotate_proxy = RotateProxy(used_proxy=self.proxy)
                self.proxy, self.seleniumwire_options, self.proxies = rotate_proxy.change_proxy()

            #  proxies=self.proxies,
            print(url)
            r = self.scraper.get(url, timeout=3)

            if str(r.status_code) == '200':
                soup = BeautifulSoup(r.content, 'lxml')
                print(r.status_code)
                break
            else:
                print(r.status_code)
                soup = None
                time.sleep(1.5)
        return soup


if __name__ == '__main__':
    website_url = 'http://www.sahibinden.com/otomotiv-ekipmanlari-yedek-parca'
    starting_page = 1
    ending_page = 1
    sahibinden_scraper = SahibindenCloudScraper(website_url=website_url, starting_page=starting_page, ending_page=ending_page)