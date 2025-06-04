import requests
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)


def clean_company_name(company_name):
    """Cleans common suffixes from a company name."""
    if not isinstance(company_name, str):
        return ""
    replacements = [
        'Private Limited', 'Limited.', 'Pvt Ltd', 'Pvt. Ltd.',
        'Ltd', 'Limited', 'Llp', 'Private Li Mited'
    ]
    clean_name = company_name.title()
    for rep in replacements:
        clean_name = clean_name.replace(rep.title(), '')
    return clean_name.strip()


def comp_name(search_keyword):
    """Fetches company information from TheCompanyCheck API based on search keyword."""
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/json",
        "Origin": "https://www.thecompanycheck.com",
        "Priority": "u=1, i",
        "Referer": "https://www.thecompanycheck.com/",
        "User-Agent": "Mozilla/5.0"
    }

    url = "https://www.thecompanycheck.com/api/CompanySearch/Search"
    filer_name = clean_company_name(search_keyword)
    payload = {"SearchKeyword": filer_name}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)

        if response.status_code == 200:
            try:
                data = response.json()
            except json.JSONDecodeError:
                logging.error("Invalid JSON response received.")
                return {"status": 500, "message": "Invalid JSON response."}

            companies = data.get("CompanyMasterSearchModel", [])
            for company in companies:
                company_name = company.get("CompanyName", "")
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
                    return {"status": 200, "data": company_info}

            logging.info("Company not found in search results.")
            return {"status": 404, "message": "Company not found."}
        else:
            logging.error(f"Failed with status code: {response.status_code}")
            return {"status": response.status_code, "message": "Failed to fetch data."}

    except requests.exceptions.Timeout:
        logging.error("Request timed out.")
        return {"status": 504, "message": "Request timed out."}

    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {str(e)}")
        return {"status": 503, "message": "Service unavailable."}


# Example usage
if __name__ == "__main__":
    result = comp_name('SLT Infracon Private Limited')
    if result["status"] != 200:
        print(f"Error ({result['status']}): {result['message']}")
