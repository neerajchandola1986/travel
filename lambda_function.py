from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import json
import time

def convert_base64(file_path):
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string


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
    url = event["queryStringParameters"].get("url", None)
    i_type = event["queryStringParameters"].get("i_type", 'vacanza')
    adult_0_25 = int(event["queryStringParameters"].get("adult_0_25", False))
    adult_0_30 = int(event["queryStringParameters"].get("adult_0_30", False))
    adult_26_60 = int(event["queryStringParameters"].get("adult_26_60", False))
    adult_61_75 = int(event["queryStringParameters"].get("adult_61_75", False))
    adult_76_999 = int(event["queryStringParameters"].get("adult_76_999", False))
    travel_cost =  int(event["queryStringParameters"].get("travel_cost", False))
    s_date = event["queryStringParameters"].get("s_date", '30/12/2018')
    e_date = event["queryStringParameters"].get("e_date", '31/12/2018')
    loc = event["queryStringParameters"].get("loc", 'Sri Lanka')
    if(url):
        driver.get(url)
        print("Setting Value")
        time.sleep(5)
        print("Value Set")
        image_name = '/tmp/before_fill_main_page.png'
        # driver.get_screenshot_as_file(image_name)
        driver.execute_script("$('#sq_viaggi_categoria').val('%s')" %i_type)
        if(adult_0_25):
            driver.find_element_by_xpath('//input[@id="sq_viaggi_numero_assicurati_0_25"]').send_keys(adult_0_25)
        if(adult_26_60):
            driver.find_element_by_xpath('//input[@id="sq_viaggi_numero_assicurati_26_60"]').send_keys(adult_26_60)
        if(adult_61_75):
            driver.find_element_by_xpath('//input[@id="sq_viaggi_numero_assicurati_61_75"]').send_keys(adult_61_75)
        if(adult_76_999):
            driver.find_element_by_xpath('//input[@id="sq_viaggi_numero_assicurati_76_999"]').send_keys(adult_76_999)
        if(adult_0_30):
            driver.find_element_by_xpath('//input[@id="sq_viaggi_numero_assicurati_0_30"]').send_keys(adult_0_30)
        if(travel_cost):
            driver.find_element_by_xpath('//input[@id="sq_viaggi_importo_assicurato"]').send_keys(travel_cost)
        
        driver.execute_script("$('#sq_viaggi_inizio').val('%s');" %s_date)
        driver.execute_script("$('#sq_viaggi_fine').val('%s');" %e_date )
        driver.execute_script("$('#sq_viaggi_destinazione_specifica').val('%s')" %loc )
        # driver.get_screenshot_as_file('after_fill_main_page.png') 
        print("Submitting Form")
        try:
            driver.execute_script("$('#sq_viaggi .btn-orange').click()")
        except:
            print("No click")
        # driver.get_screenshot_as_file('after_submit.png') 
        print("Form Submit")
        # driver.get_screenshot_as_file('after_wait_submit.png') 
        info = {}
        info["page_data"] = str(driver.execute_script("return $('.offer_price').text().replace(/ /g,'');"))
        info["bag_price"] = str(driver.execute_script(" return $('#bagaglio .destinazione_M,.day day_1_4').find('b').text(); "))
        print(page_data)
    driver.close()
    return {
    "statusCode": 200,
    "body": json.dumps(info),
    "headers": {"Content-Type": "application/json"},
    }
