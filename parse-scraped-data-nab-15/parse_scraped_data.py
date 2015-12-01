import json, csv, re, string

fh = open("nab15.csv", "r")
# scrape_list = fh.readlines()
# fh.close()

creader = csv.DictReader(fh)
scrape_list = []
for eaRow in creader:
    scrape_list += [eaRow]
#
fh.close()
#print("sample:", scrape_list[0:3])
#exit("Done! %s" %(len(scrape_list), ))

def fix_phone(input):
    output = re.sub(r'[^0-9a-zA-Z]', '', input)
    if output[0] == "1":
        output = output[1:]
    #
    if len(output) == 10:
        output = output[0:3]+"-"+output[3:6]+"-"+output[6:10]
    else:
        print("EXCEPTIONAL PHONE FOUND: ", input)
        output = input
    #
    return output
#


results = []

for each_scrape in scrape_list:
    # scrape_data = json.loads(each_scrape)
    scrape_data = each_scrape
    ea_info = scrape_data["info"]
    try:
        match = re.findall(r"P: ([0-9( )-+-.]+)", ea_info)
        if match:
            # print("ph::", match)
            ea_phone = fix_phone(match[0])
        else:
            ea_phone = ""
        #
        match = re.findall(r"F: ([0-9( )-+-.]+)", ea_info)
        if match:
            ea_fax = fix_phone(match[0])
        else:
            ea_fax = ""
        #
        match = re.findall(r"\n(.+), ([A-Z][A-Z]) (\d{5})", ea_info)
        if match:
            # print("addr::", match)
            ea_csz = match[0][0] + ", " + match[0][1] + " " + match[0][2]
            ea_city = match[0][0]
            ea_state = match[0][1]
            ea_zip = match[0][2]

            match = re.findall(r"(.+)\n(.+)?\n?"+ea_city, ea_info)
            if match:
                # print("street::", match)
                ea_addr = ', '.join(filter(None, match[0]))
            else:
                ea_addr = ""
            #
        else:
            ea_csz = ""
            ea_city = ""
            ea_state = ""
            ea_zip = ""
            ea_addr = ""
        #
        company_name = scrape_data["name"]
        company_name_filtered = filter(lambda x: x in string.printable, company_name)
        print(company_name_filtered, ea_phone, ea_fax, ea_csz, ea_city, ea_addr)
        results += [[company_name_filtered, ea_phone, ea_fax, ea_addr, ea_city, ea_state, ea_zip]]
    except:
        pass


oh = open("parse.csv", "w")
csvdoc = csv.writer(oh)
csvdoc.writerows(results)
oh.close()

