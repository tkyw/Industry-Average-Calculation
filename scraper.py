## This file contains the method we applied in getting all the financial ratios of all compaines that are categorised in the same industry with FCW(wholesale distributors industry)
## and Eurospan(home furnishing industry)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from time import sleep
import json
import concurrent.futures

eurospan_competitors = ['AHB', 'ATTA', 'CSCENIC', 'ECOMATE', 'EUROSP', 'FACBIND', 'FIHB', 'JAYCORP', 'LIIHEN', 'MOBILIA', 'NIHSIN', 'RKI', 'SCNWOLF', 'SERNKOU', 'SHH', 'SPRING', 'SWSCAP', 'TAFI', 'WEGMANS', 'YOCB']
eurospan_competitors = [item + '_euro' for item in eurospan_competitors]
fcw_competitors = ['ACO', 'CHUAN', 'COMPUGT', 'DELEUM', 'FCW', 'HAPSENG', 'HARISON', 'JSB', 'KPSCB', 'LAMBO', 'MARCO', 'MCEHLDG', 'MRDIY', 'MYNEWS', 'OCB', 'OCR', 'PETDAG', 'PHB', 'PTT', 'SALCON', 'SAMCHEM', 'SCC', 'SIME', 'SOLID', 'TEXCHEM', 'TURBO', 'UMS']
fcw_competitors = [item + '_fcw' for item in fcw_competitors]

def find(driver, selector: str, all_=False):
    return WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector))) if not all_ else WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)) 
    )

def scraper(ticker: str):
    ticker, company = ticker.split('_')
    link = f'https://www.tradingview.com/symbols/MYX-{ticker}/financials-statistics-and-ratios/'
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(link)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    sleep(1.3)
    years = [item.text for item in find(driver, ".values-wUUYDe4m.values-2uDwgQdp .wrap-1WwaU3uo > div", all_=True)]
    
    containers = find(driver, '.container-U3SxPDnP', all_=True)
    items = {}
    items['ticker'] = ticker
    items['years'] = years
    items['company'] = company
    for container in containers:
        title = find(container, "span.title-U3SxPDnP.apply-overflow-tooltip").text
        values = [item.text.replace('\u202a', "").replace("\u202c", "").replace("—", "-").replace('−', '-') for item in find(container, ".wrap-1WwaU3uo > div", all_=True)]
        items[title] = values
    items = json.dumps(items)
    with open(r"C:\Users\USER\Python Programme\Acc Assignment\output.json", "a") as wf:
        wf.write(f"{items},\n")

if __name__ == '__main__':
    tickers = fcw_competitors + eurospan_competitors
    scraper(tickers[0])
    with open(r"C:\Users\USER\Python Programme\Acc Assignment\output.json", "w") as wf:
        wf.write(f"[\n")
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(scraper, ticker) for ticker in tickers]
    with open(r"C:\Users\USER\Python Programme\Acc Assignment\output.json", "a") as wf:
        wf.write(f"]\n")


