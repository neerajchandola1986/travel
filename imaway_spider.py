from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os,json,time, base64,re

def lambda_handler(event, context):
    # TODO implement
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1366x768')
    chrome_options.add_argument('--user-data-dir=/tmp/user-data')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--data-path=/tmp/data-path')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium"
    driver = webdriver.Chrome(os.getcwd() + "/bin/chromedriver",chrome_options=chrome_options)
    # driver = webdriver.Chrome(chrome_options=chrome_options)
    page_data = ""
    url = "https://www.imaway.it/"
    i_type = event["queryStringParameters"].get("i_type", '1')
    p_0_35 = int(event["queryStringParameters"].get("p_0_35", False))
    p_0_60 = int(event["queryStringParameters"].get("p_0_60", False))
    p_61_68 = int(event["queryStringParameters"].get("p_61_68", False))
    p_69_75 = int(event["queryStringParameters"].get("p_69_75", False))
    s_date = event["queryStringParameters"].get("s_date", False)
    e_date = event["queryStringParameters"].get("e_date", False)
    destination = event["queryStringParameters"].get("destination", False)
    coupen = event["queryStringParameters"].get("coupen", False)

    if(url):
        driver.get(url)
        print("Setting Value")
        time.sleep(5)
        if(p_0_60):
            driver.execute_script(" $('#numero_assicurati_%s_0-60').val(%s); "%(i_type, p_0_60))
        if(p_61_68):
            driver.execute_script(" $('#numero_assicurati_%s_61-68').val(%s); "%(i_type, p_61_68))
        if(p_69_75):
            driver.execute_script(" $('#numero_assicurati_%s_69-75').val(%s); "%(i_type, p_69_75))
        
        if(s_date):
            driver.execute_script(" $('#data_inizio_%s').val('%s'); "%(i_type, s_date) )
            driver.execute_script(" $('#data_decorrenza_%s').val('%s'); "%(i_type, s_date) )

        if(e_date):
            driver.execute_script(" $('#data_fine_%s').val('%s'); "%(i_type, e_date))
            driver.execute_script(" $('#data_scadenza_%s').val('%s'); "%(i_type, e_date))
        
        if(coupen): 
            driver.execute_script(" $('#codice_sconto_%s').val('%s'); "%(i_type, coupen))
        driver.execute_script(" $('#destinazione_specifica_%s').val('%s'); "%(i_type, destination))
        
        driver.execute_script(" sendFormQuote('%s') "%i_type )
        print("Form Submit")
        time.sleep(5)
        response_data = {}
        price_tag = []
        for one_tag in driver.find_elements_by_xpath('//div[@class="tr"][2]/div[contains(@class, "classe-prodotto")]/span'):
            price_tag.append(one_tag.text.replace(' ','_').lower())
        price = []
        for one_price in driver.find_elements_by_xpath('//div[@class="tr"][3]/div[contains(@class, "classe-prodotto")]/span[@class="premio text-primary"]'):
            price.append((one_price.text).encode('ascii', 'ignore').decode("utf-8").strip())
        primary_data = dict(zip(price_tag, price))
        if(coupen):
            old_price = []
            for one_price in driver.find_elements_by_xpath('//div[@class="tr"][3]/div[contains(@class, "classe-prodotto")]//span[@class="strike"]'):
                old_price.append((one_price.text).encode('ascii', 'ignore').decode("utf-8").strip())
            without_dis_data = dict(zip(price_tag, old_price))
            response_data["discounted"] = primary_data
            response_data["without_discount"] = without_dis_data
        else:
            response_data = primary_data
        print(response_data)

    driver.close()
    return {
    "statusCode": 200,
    "body": json.dumps(response_data),
    "headers": {"Content-Type": "application/json"},
    }