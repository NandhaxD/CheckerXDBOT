



import requests
import re
import json



class Checker:
  
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
       else:
            return []
            

 
         
       