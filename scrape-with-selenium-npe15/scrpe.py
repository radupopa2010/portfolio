from selenium import webdriver
import time
import json

''' to begin using it  '''

driver = webdriver.Remote("http://localhost:4444/wd/hub", webdriver.DesiredCapabilities.CHROME)
driver.implicitly_wait(4)

#start url
baseurl="http://npe15.mapyourshow.com/6_0/exhibitor/exhibitor-details.cfm?ExhID="

#import a list of exhibitor IDs

fh = open("npe-exh-id-list.txt", "r")
id_list = fh.readlines()
fh.close()


results = []

for eachId in id_list:
    print "working with id", eachId
    eachUrl = baseurl + eachId
    time.sleep(3)
    driver.get(eachUrl)
    each_result = {}
    selected_element = driver.find_element_by_xpath('//*[@id="jq-exhibitor-details"]/div/div[1]/h1')
    each_result["name"] = selected_element.text
    selected_element = driver.find_element_by_xpath('//*[@id="jq-exhibitor-details"]/div/div[1]/div/div[1]/p')
    each_result["info"] = selected_element.text
    try:
        selected_element = driver.find_element_by_xpath('//*[@id="mys-exhibitor-details-wrapper"]/div[4]/div/div/ul')
        each_result["categories"] = selected_element.text
    except:
        try:
            selected_element = driver.find_element_by_xpath('//*[@id="mys-exhibitor-details-wrapper"]/div[3]/div/div/ul')
            each_result["categories"] = selected_element.text
        except:
            each_result["categories"] = ""
    print(json.dumps(each_result))
    results += [json.dumps(each_result)]


fh2 = open("results.json", "w")
fh2.writelines(results)
fh2.close()

