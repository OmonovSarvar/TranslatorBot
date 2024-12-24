import main
import requests


url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
payload = {}
headers = {}
def uz_and_eng_translator():
    if main.get_translation_buttons() == "uz_to_en":
        payload = {
                "q": "Salom, dunyo!",
                "target": "en",
                "source": "uz"
        }
        headers = {
            "x-rapidapi-key": "707c9a7aeemsh5ffec9ad5b7ac26p1582a5jsn2dd2b6a6b87b",
            "x-rapidapi-host": "google-translate1.p.rapidapi.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "application/gzip"
        }

response = requests.post(url, data=payload, headers=headers)