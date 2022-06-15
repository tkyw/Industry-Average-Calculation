from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from time import sleep

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.get('https://www.tradingview.com/markets/stocks-malaysia/sectorandindustry-industry/wholesale-distributors/')
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
tickers = [item.text for item in WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.tv-screener-table__symbol-container-description > a.tv-screener__symbol.apply-common-tooltip'))
)]
print(tickers)