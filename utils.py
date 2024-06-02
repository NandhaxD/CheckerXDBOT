



import requests
import re
import json
import bs4

class Checker:

    headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Infinix X6816C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.98 Mobile Safari/537.36'
    }
  
    @staticmethod
    def generator(bin_code: int, limit : int = 5):
       base_url = "https://namsogen.org/ajax.php"
              
       form_data = {
          "type": "3",
          "bin": bin_code,
          "date": "on",
          "csv": "on",
          "number": limit,
          "format": "json"
          }
       response = requests.post(base_url, data=form_data)
       if response.status_code == 200:
            data = response.text
            clean_response_text = re.sub(r'[^\x20-\x7E]+', '', data)
            clean_response_text = re.sub(r',\s*}', '}', clean_response_text)
            clean_response_text = re.sub(r',\s*]', ']', clean_response_text)
            data = json.loads(clean_response_text)
            return data
       return []
         
    @staticmethod
    def fake(country: str = 'us'):

        base_url = f"https://www.fakenamegenerator.com/advanced.php?t=country&n%5B%5D={country}&c%5B%5D={country}&gen=40&age-min=21&age-max=75"
        response = requests.get(base_url, headers=headers)
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        info_element = soup.find(class_='info')
        data = {}
        if info_element:
        # Extract name and address
           address = info_element.find('div', class_='address')
           if address:
                name = address.find('h3').get_text(strip=True)
                address_text = address.find('div', class_='adr').get_text(separator=' ', strip=True)
                data['Name'] = name
                data['Address'] = address_text

        # Extract extra details
        extra = info_element.find('div', class_='extra')
        if extra:
           # Extract all the <dl> elements
           dls = extra.find_all('dl', class_='dl-horizontal')
           for dl in dls:
              dt = dl.find('dt').get_text(strip=True)
              dd = dl.find('dd').get_text(separator=' ', strip=True)
              data[dt] = dd

        # Extract phone details
        phone_section = extra.find('h3', class_='hh3', string='Phone')
        if phone_section:
            phone_dt = phone_section.find_next('dt', string='Phone')
            if phone_dt:
                phone_dd = phone_dt.find_next('dd').get_text(strip=True)
                data['Phone'] = phone_dd

        # Extract birthday details
        birthday_section = extra.find('h3', class_='hh3', string='Birthday')
        if birthday_section:
            birthday_dt = birthday_section.find_next('dt', string='Birthday')
            if birthday_dt:
                birthday_dd = birthday_dt.find_next('dd').get_text(strip=True)
                data['Birthday'] = birthday_dd

            age_dt = birthday_section.find_next('dt', string='Age')
            if age_dt:
                age_dd = age_dt.find_next('dd').get_text(strip=True)
                data['Age'] = age_dd

        # Extract online details
        online_section = extra.find('h3', class_='hh3', string='Online')
        if online_section:
            email_dt = online_section.find_next('dt', string='Email Address')
            if email_dt:
                email_dd = email_dt.find_next('dd').get_text(separator=' ', strip=True)
                data['Email Address'] = email_dd

            username_dt = online_section.find_next('dt', string='Username')
            if username_dt:
                username_dd = username_dt.find_next('dd').get_text(strip=True)
                data['Username'] = username_dd

            password_dt = online_section.find_next('dt', string='Password')
            if password_dt:
                password_dd = password_dt.find_next('dd').get_text(strip=True)
                data['Password'] = password_dd

            website_dt = online_section.find_next('dt', string='Website')
            if website_dt:
                website_dd = website_dt.find_next('dd').get_text(strip=True)
                data['Website'] = website_dd

            browser_agent_dt = online_section.find_next('dt', string='Browser user agent')
            if browser_agent_dt:
                browser_agent_dd = browser_agent_dt.find_next('dd').get_text(strip=True)
                data['Browser user agent'] = browser_agent_dd

        # Extract finance details
        finance_section = extra.find('h3', class_='hh3', string='Finance')
        if finance_section:
            card_dt = finance_section.find_next('dt')
            if card_dt:
                card_dd = card_dt.find_next('dd').get_text(strip=True)
                data[card_dt.get_text(strip=True)] = card_dd

            expires_dt = finance_section.find_next('dt', string='Expires')
            if expires_dt:
                expires_dd = expires_dt.find_next('dd').get_text(strip=True)
                data['Expires'] = expires_dd

            cvc2_dt = finance_section.find_next('dt', string='CVC2')
            if cvc2_dt:
                cvc2_dd = cvc2_dt.find_next('dd').get_text(strip=True)
                data['CVC2'] = cvc2_dd

        # Extract employment details
        employment_section = extra.find('h3', class_='hh3', string='Employment')
        if employment_section:
            company_dt = employment_section.find_next('dt', string='Company')
            if company_dt:
                company_dd = company_dt.find_next('dd').get_text(strip=True)
                data['Company'] = company_dd

            occupation_dt = employment_section.find_next('dt', string='Occupation')
            if occupation_dt:
                occupation_dd = occupation_dt.find_next('dd').get_text(strip=True)
                data['Occupation'] = occupation_dd

        # Extract physical characteristics
        physical_section = extra.find('h3', class_='hh3', string='Physical characteristics')
        if physical_section:
            height_dt = physical_section.find_next('dt', string='Height')
            if height_dt:
                height_dd = height_dt.find_next('dd').get_text(strip=True)
                data['Height'] = height_dd

            weight_dt = physical_section.find_next('dt', string='Weight')
            if weight_dt:
                weight_dd = weight_dt.find_next('dd').get_text(strip=True)
                data['Weight'] = weight_dd

            blood_type_dt = physical_section.find_next('dt', string='Blood type')
            if blood_type_dt:
                blood_type_dd = blood_type_dt.find_next('dd').get_text(strip=True)
                data['Blood type'] = blood_type_dd

        # Extract tracking numbers
        tracking_section = extra.find('h3', class_='hh3', string='Tracking numbers')
        if tracking_section:
            ups_dt = tracking_section.find_next('dt', string='UPS tracking number')
            if ups_dt:
                ups_dd = ups_dt.find_next('dd').get_text(strip=True)
                data['UPS tracking number'] = ups_dd

            western_union_dt = tracking_section.find_next('dt', string='Western Union MTCN')
            if western_union_dt:
                western_union_dd = western_union_dt.find_next('dd').get_text(strip=True)
                data['Western Union MTCN'] = western_union_dd

            moneygram_dt = tracking_section.find_next('dt', string='MoneyGram MTCN')
            if moneygram_dt:
                moneygram_dd = moneygram_dt.find_next('dd').get_text(strip=True)
                data['MoneyGram MTCN'] = moneygram_dd

        # Extract other details
        other_section = extra.find('h3', class_='hh3', string='Other')
        if other_section:
            favorite_color_dt = other_section.find_next('dt', string='Favorite color')
            if favorite_color_dt:
                favorite_color_dd = favorite_color_dt.find_next('dd').get_text(strip=True)
                data['Favorite color'] = favorite_color_dd

            vehicle_dt = other_section.find_next('dt', string='Vehicle')
            if vehicle_dt:
                vehicle_dd = vehicle_dt.find_next('dd').get_text(strip=True)
                data['Vehicle'] = vehicle_dd

            guid_dt = other_section.find_next('dt', string='GUID')
            if guid_dt:
                guid_dd = guid_dt.find_next('dd').get_text(strip=True)
                data['GUID'] = guid_dd

            qr_code_dt = other_section.find_next('dt', string='QR Code')
            if qr_code_dt:
                qr_code_dd = qr_code_dt.find_next('dd').get_text(strip=True)
                data['QR Code'] = qr_code_dd

        if data:
           return data
        return data
        

 
         
       
