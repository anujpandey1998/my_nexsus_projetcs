import requests
import json

url = "https://www.thecompanycheck.com/api/CompanySearch/Search"

def write_txt(company_data):
    with open(r'C:\Users\PC\PyCharmMiscProject\data.txt', 'a', encoding='utf-8') as f:
        f.write(f"CIN: {company_data.get('CIN')}\n")
        f.write(f"Company Name: {company_data.get('CompanyName')}\n")
        f.write(f"Status: {company_data.get('Status')}\n")
        f.write(f"Location: {company_data.get('Location')}\n")
        f.write(f"Website: {company_data.get('Website')}\n")
        f.write("-" * 50 + "\n")

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/json",
    "Cookie": "_ga=GA1.1.469719065.1749018344; _ga_BJ2R3ED1FH=GS2.1.s1749018344$o1$g1$t1749018586$j44$l0$h0",
    "Origin": "https://www.thecompanycheck.com",
    "Priority": "u=1, i",
    "Referer": "https://www.thecompanycheck.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
}

payload = {
    "SearchKeyword": "tata"
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    data = response.json()
    companies = data.get("CompanyMasterSearchModel", [])

    for company in companies:
        print("CIN:", company.get("CIN"))
        print("Company Name:", company.get("CompanyName"))
        print("Status:", company.get("Status"))
        print("Location:", company.get("Location"))
        print("Website:", company.get("Website"))
        print("-" * 50)

        # Save to text file
        write_txt(company)
else:
    print("Failed to fetch data. Status code:", response.status_code)
