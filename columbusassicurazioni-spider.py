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
    url = "https://viaggiare.columbusassicurazioni.it/quickQuote.cfm"
    i_type = event["queryStringParameters"].get("i_type", 'ST_ABX_N')
    mode = event["queryStringParameters"].get("mode", 'GRP')
    p_0_2 = int(event["queryStringParameters"].get("p_0_2", False))
    p_3_17 = int(event["queryStringParameters"].get("p_3_17", False))
    p_18_64 = int(event["queryStringParameters"].get("p_18_64", False))
    p_65_69 = int(event["queryStringParameters"].get("p_65_69", False))
    p_70_74 = int(event["queryStringParameters"].get("p_70_74", False))    
    s_date = event["queryStringParameters"].get("s_date", False)
    e_date = event["queryStringParameters"].get("e_date", False)
    destination = event["queryStringParameters"].get("destination", 'L_AIT03')
    coupen = event["queryStringParameters"].get("coupen", False)

    if(url):
        driver.get(url)
        print("Setting Value")
        time.sleep(5)
        print("Value Set")
        driver.find_element_by_xpath('//label[@for="%s"]' %destination).click()
        if(p_0_2):
            driver.find_element_by_xpath('//select[@id="INF"]/option[@value="%s"]' %p_0_2).click()
        if(p_3_17):
            driver.find_element_by_xpath('//select[@id="DCH"]/option[@value="%s"]' %p_3_17).click()
        if(p_18_64):
            driver.find_element_by_xpath('//select[@id="AYG"]/option[@value="%s"]' %p_18_64).click()
        if(p_65_69):
            driver.find_element_by_xpath('//select[@id="AMD"]/option[@value="%s"]' %p_65_69).click()
        if(p_70_74):
            driver.find_element_by_xpath('//select[@id="AMR"]/option[@value="%s"]' %p_70_74).click()
        driver.find_element_by_xpath('//select[@id="groupType"]/option[@value="%s"]' %mode).click()
        if(e_date):
            driver.find_element_by_xpath('//input[@id="endDate"]').send_keys(e_date)
        if(s_date):
            driver.find_element_by_xpath('//input[@id="startDate"]').send_keys(s_date)
        if(coupen):
            driver.find_element_by_xpath('//input[@id="promotionCode"]').send_keys(coupen)
        # before = driver.get_screenshot_as_base64()
        driver.find_element_by_xpath('//select[@id="coverType"]/option[@value="%s"]' %i_type).click()
        time.sleep(5)
        driver.find_element_by_xpath('//input[@id="quickQuoteSubmitButton"]').click()
        # after = driver.get_screenshot_as_base64()
        print("Form Submit")
        info = {}
        p1 = {}
        p2 = {}
        
        p1["price"] = driver.execute_script(" return $('#AITASS_priceSpan').find('h3').text().replace('€', '') ")
        p1["with_bag"] = driver.execute_script(" return $('#AITSST_priceSpan').find('h3').text().replace('€', '') ")
        p1["with_bag_cancellation"] = driver.execute_script(" return $('#AITSSU_priceSpan').find('h3').text().replace('€', '') ")
        p1["annual"] = driver.execute_script(" return $('#AITMSU_priceSpan').find('h3').text().replace('€', '') ")
        if(coupen):
            p2["price"] = driver.execute_script(" return $('#AITASS_priceSpan').find('span').text().replace('€', '') ")
            p2["with_bag"] = driver.execute_script(" return $('#AITSST_priceSpan').find('span').text().replace('€', '') ")
            p2["with_bag_cancellation"] = driver.execute_script(" return $('#AITSSU_priceSpan').find('span').text().replace('€', '') ")
            p2["annual"] = driver.execute_script(" return $('#AITMSU_priceSpan').find('span').text().replace('€', '') ")
            info["regular"] = p2
            info["discount"] = p1
        else:
            info["regular"] = p1
        # data = str(driver.execute_script(" return $('#productsOffered').val() "))
        # print(data)
        # info = {}
        # temp = {}
        # for one_set in data.split('|'):
        #     x = one_set.split('=')
        #     temp[x[0]] = x[1]
        # print(temp)        
        # info["price"] = temp.get("AITASS","N/A")
        # info["with_bag"] = temp.get("AITSST","N/A")
        # info["with_bag_cancellation"] = temp.get("AITSSU","N/A")
        # info["annual"] = temp.get("AITMSU","N/A")
    driver.close()
    return {
    "statusCode": 200,
    "body": json.dumps(info),
    "headers": {"Content-Type": "application/json"},
    }