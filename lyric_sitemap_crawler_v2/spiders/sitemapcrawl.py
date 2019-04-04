import base64
import gzip
import random
from scrapy import cmdline
from scrapy.spiders import SitemapSpider # design for site map
import os

BASE_OUTPUT_DIR = '/home/dante0shy/PycharmProjects/homwor_gmy/data'#os.environ.get("BASE_OUTPUT_DIR")


# Spider that crawls lyrics.wikia by their sitemap
class MySpider(SitemapSpider):
    name = 'lyrics'
    sitemap_urls = ['http://lyrics.wikia.com/sitemap-newsitemapxml-index.xml']
    sitemap_rules = [('/wiki/', 'parse_sitemap_url')]

    # The function that is called for each site in the sitemap.
    def parse_sitemap_url(self, response):
        fname = response.url.split('/')[-1]
        print(response)
        htmi = base64.b64encode(gzip.compress(response.body))
        with open(os.path.join(BASE_OUTPUT_DIR , '{}&&{}'.format(fname,random.randint(0,10000))) , 'wb') as f:#
            f.write(htmi)


cmdline.execute("scrapy runspider sitemapcrawl.py --set DOWNLOAD_DELAY=1.5 --set JOBDIR=lyrics".split())

