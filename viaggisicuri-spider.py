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
    url = "https://www.viaggisicuri.com/quote/GetAQuote"
    i_type = event["queryStringParameters"].get("i_type", 'ST_ABX_N')
    mode = event["queryStringParameters"].get("mode", 'gruppo')
    p_0_16 = int(event["queryStringParameters"].get("p_0_16", False))
    p_17_65 = int(event["queryStringParameters"].get("p_17_65", False))
    book_date = event["queryStringParameters"].get("book_date", False)
    travel_cost = event["queryStringParameters"].get("travel_cost", False)
    s_date = event["queryStringParameters"].get("s_date", False)
    e_date = event["queryStringParameters"].get("e_date", False)
    destination = event["queryStringParameters"].get("destination", 'AW')
    coupen = event["queryStringParameters"].get("coupen", False)

    if(url):
        driver.get(url)
        time.sleep(5)
        driver.find_element_by_xpath('//div[@id="%s"]' %mode).click()
        if(p_17_65):
            driver.find_element_by_xpath('//select[@id="Quote_Adult"]/option[@value="%s"]' %p_17_65).click()
        if(p_0_16):
            driver.find_element_by_xpath('//select[@id="Quote_Child"]/option[@value="%s"]' %p_0_16).click()
        driver.execute_script(' $("#Quote_DateStart").attr("readonly", false); ')
        driver.execute_script(' $("#Quote_DateFinish").attr("readonly", false); ')
        driver.execute_script(' $("#Quote_AnnualStart").attr("readonly", false); ')

        if(e_date):
            driver.find_element_by_xpath('//input[@id="Quote_DateFinish"]').send_keys(e_date)
        else:
            driver.find_element_by_xpath('//label[@for="Quote_Annual_1"]').click()

        if(s_date):
            if(e_date):
                driver.find_element_by_xpath('//input[@id="Quote_DateStart"]').send_keys(s_date)
            else:
                driver.find_element_by_xpath('//input[@id="Quote_AnnualStart"]').send_keys(s_date)
        if(book_date):
            driver.execute_script(' $("#Quote_DateBooking").attr("readonly", false); ')
            driver.find_element_by_xpath('//input[@id="Quote_DateBooking"]').send_keys(book_date)
            driver.find_element_by_xpath('//input[@id="Quote_TripCost"]').send_keys(travel_cost)

        if(coupen):
            driver.find_element_by_xpath('//input[@id="Quote_PromoCode"]').send_keys(coupen)
        if(e_date):
            driver.execute_script(' $("#Country_single").val("%s") ' %destination)
        else:
            driver.execute_script(' $("#Quote_annual_AField").val("%s") ' %destination)
        driver.find_element_by_xpath('//input[@type="submit"]').click()
        print("Form Submit")
        time.sleep(5)
        info = {}
        if(book_date):
            if(coupen):
                data1 = driver.find_element_by_xpath('//tr[3]/td[1]')
                data2 = driver.find_element_by_xpath('//tr[4]/td[1]')
                info["price"] = data1.text.replace("€", "").strip()
                info["discount"] = data2.text.replace("€", "").strip()
            else:
                data = driver.find_element_by_xpath('//tr[3]/td[1]')
                info["price"] = data.text.replace("€", "").strip()
        else:
            info["price"] = {}
            info["price"]["singolo"] = {}
            info["price"]["annual"] = {}
            try:
                if(coupen):
                    info["discount"] = {}
                    info["discount"]["singolo"] = {}
                    info["discount"]["annual"] = {}
                    data1 = driver.find_elements_by_xpath('//tr[3]/td')
                    data2 = driver.find_elements_by_xpath('//tr[4]/td')

                    info["price"]["singolo"]["base"] = data1[0].text.replace("€", "").strip()
                    info["price"]["singolo"]["argento"] = data1[1].text.replace("€", "").strip()
                    info["price"]["singolo"]["oro"] = data1[2].text.replace("€", "").strip()
                    info["price"]["annual"]["base"] = data1[4].text.replace("€", "").strip()
                    info["price"]["annual"]["argento"] = data1[5].text.replace("€", "").strip()
                    info["price"]["annual"]["oro"] = data1[6].text.replace("€", "").strip()

                    info["discount"]["singolo"]["base"] = data2[0].text.replace("€", "").strip()
                    info["discount"]["singolo"]["argento"] = data2[1].text.replace("€", "").strip()
                    info["discount"]["singolo"]["oro"] = data2[2].text.replace("€", "").strip()
                    info["discount"]["annual"]["base"] = data2[4].text.replace("€", "").strip()
                    info["discount"]["annual"]["argento"] = data2[5].text.replace("€", "").strip()
                    info["discount"]["annual"]["oro"] = data2[6].text.replace("€", "").strip()
                else:
                    data = driver.find_elements_by_xpath('//tr[3]/td')
                    info["price"]["singolo"]["base"] = data[0].text.replace("€", "").strip()
                    info["price"]["singolo"]["argento"] = data[1].text.replace("€", "").strip()
                    info["price"]["singolo"]["oro"] = data[2].text.replace("€", "").strip()

                    info["price"]["annual"]["base"] = data[4].text.replace("€", "").strip()
                    info["price"]["annual"]["argento"] = data[5].text.replace("€", "").strip()
                    info["price"]["annual"]["oro"] = data[6].text.replace("€", "").strip()
            except:
                pass

    driver.close()
    return {
    "statusCode": 200,
    "body": json.dumps(info),
    "headers": {"Content-Type": "application/json"},
    }