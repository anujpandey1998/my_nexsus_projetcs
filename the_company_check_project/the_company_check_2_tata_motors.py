import requests
import json

def clean_company_name(company_name):
    # Add your cleaning logic here
    clean_name = company_name.title().replace('Private Limited', '').replace('Limited.', '').replace('Pvt Ltd',
                                                                                                     '').replace(
        'Pvt. Ltd.', '').replace('Ltd', '').replace('Limited', '').replace('Llp', '').replace('Private Li Mited', '')
    return clean_name.strip()


# Function to get Company Names
def comp_name(search_keyword):
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/json",
        "Cookie": "_ga=GA1.1.469719065.1749018344; _ga_BJ2R3ED1FH=GS2.1.s1749018344$o1$g1$t1749018586$j44$l0$h0",
        "Origin": "https://www.thecompanycheck.com",
        "Priority": "u=1, i",
        "Referer": "https://www.thecompanycheck.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    }

    url = "https://www.thecompanycheck.com/api/CompanySearch/Search"
    filer_name = clean_company_name(search_keyword)

    payload = {
        "SearchKeyword": filer_name
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        companies = data.get("CompanyMasterSearchModel", [])
        for company in companies:
            company_name = company.get("CompanyName")
            clean_comp_name = clean_company_name(company_name)
            if clean_comp_name.strip().title() == filer_name.strip().title():
                company_info = {
                    "CIN": company.get("CIN"),
                    "CompanyName": company.get("CompanyName"),
                    "Status": company.get("Status"),
                    "Location": company.get("Location"),
                    "Website": company.get("Website")
                }

                print(json.dumps(company_info, indent=4))
    else:
        print("Failed to fetch data. Status code:", response.status_code)


comp_name('tata motors limited')