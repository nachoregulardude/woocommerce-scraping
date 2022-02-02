from requests_html import HTMLSession
from sitedetails import main_url
import pandas as pd
import time

s = HTMLSession()

def get_links(url):
    r = s.get(url)
    items = r.html.find('div.product-inner.clearfix')
    links = [item.find('a', first=True).attrs['href'] for item in items]
    return links
def get_product(link):
    r = s.get(link)
    time.sleep(0.01)
    try:
        name = r.html.find('h1', first=True)    
    except Exception as ere:
        print(f'{ere} while scraping {link}')
        return
    if name:
        name = name.full_text.strip()
    else:
        name = 'Error while scraping'
    company = r.html.find('a.meta-value', first=True)
    if company:
        company = company.full_text.strip()
    else:
        company = 'Error while scraping'
    sku = r.html.find('span.meta-value', first=True)
    if sku:
        sku = sku.full_text.strip()
    else:
        sku = 'Error while scraping'
    category = r.html.find('span.posted_in', first=True)
    if category:
        category = category.full_text.strip()
    else:
        category = 'Error while scraping'
    category = str(category)
    if 'Category: ' in category:
        category = category.replace('Category: ', '')
    elif 'Categories: ' in category:
        category = category.replace('Categories: ', '')

    print(f'Added {name}\'s details to the file...')
    return [name, company, sku, category, link] 

main_url = 'https://www.detailersindia.com/shop/page/{page_num}/'

#Best to scrape and append pages in batch of no more than 10
page_start = int(input('Enter the page number of where we left of. Or 1 to start from the begining\n:'))
pages_end = int(input('Enter the page number to end the scraping at.. (try to keep it {page_start+9} or less)\n:'))

details = []
for page in range(page_start, pages_end+1):
    print(f'\nScraping page {page} for product links...')
    url = main_url.replace('{page_num}', str(page))
    try:
        links = get_links(url)
    except Exception as er:
        print(er)
        continue
    print(f'Found {len(links)} links.\n')
    for link in links:
        time.sleep(0.1)
        details.append(get_product(link))
    print('Waiting for 1 seconds...')
    time.sleep(1)
print('Creating a CSV and saving the details')
products_dataframe = pd.DataFrame(details, columns=['Product Name', 'Product Company', 'SKU', 'Category', 'Link'])
if page_start == 1:
    products_dataframe.to_csv('ProducDetails.csv', mode='w', index=False, header=True)
else:
    products_dataframe.to_csv('ProductDetails.csv', mode='a', index=False, header=False)
    
