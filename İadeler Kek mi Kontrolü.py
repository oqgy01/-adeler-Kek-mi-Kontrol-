#Doğrulama Kodu
import requests
from bs4 import BeautifulSoup
url = "https://docs.google.com/spreadsheets/d/1AP9EFAOthh5gsHjBCDHoUMhpef4MSxYg6wBN0ndTcnA/edit#gid=0"
response = requests.get(url)
html_content = response.content
soup = BeautifulSoup(html_content, "html.parser")
first_cell = soup.find("td", {"class": "s2"}).text.strip()
if first_cell != "Aktif":
    exit()
first_cell = soup.find("td", {"class": "s1"}).text.strip()
print(first_cell)


import requests
import pandas as pd
from datetime import datetime

url = "https://task.haydigiy.com/FaprikaReturnXls/4KE52N/1/"

try:
    # İsteği gönder
    response = requests.get(url)
    response.raise_for_status()  # HTTP hata durumlarını kontrol et

    # Excel dosyasını oku
    df = pd.read_excel(response.content, sheet_name=0)

    # "SiparisId" sütunu hariç diğer tüm sütunları seç
    df = df[['SiparisId']]

    # Benzersiz satırları tut
    df = df.drop_duplicates()

    # Filtrelenmiş veriyi aynı Excel dosyasına üzerine yaz
    df.to_excel("Kek İçin Kontrol Linkleri.xlsx", index=False)
    
except requests.exceptions.RequestException as e:
    pass
except Exception as e:
    pass






from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import tkinter as tk
from tkinter import simpledialog
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--log-level=1') 
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  
driver = webdriver.Chrome(options=chrome_options)

login_url = "https://task.haydigiy.com/kullanici-giris/?ReturnUrl=%2Fadmin"
driver.get(login_url)

email_input = driver.find_element(By.ID, "EmailOrPhone")
email_input.send_keys("mustafa_kod@haydigiy.com")

password_input = driver.find_element(By.ID, "Password")
password_input.send_keys("123456")
password_input.send_keys(Keys.RETURN)

# Selenium'un sayfa yüklenmesini bekleyin (örneğin, 10 saniye boyunca bekleyin)
wait = WebDriverWait(driver, 10)
wait.until(EC.url_changes(login_url))






from selenium.common.exceptions import NoSuchElementException



from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By

# Aranacak metinlerin listesi
aranacak_metinler = ["GÜLSÜM ADAK", "GULSUM ADAK", "GLSM", "GÜLSÜM", "GULSUM", "İADE", "iade", "gülsüm", "gulsum", "Gülsüm", "Gulsum", "İade", "Firmaya Teslim Edildi", "Göndericisine", "GÖNDERİCİSİNE", "GONERİCİSİNE"]

# Bulunan linkleri saklamak için boş bir liste
bulunan_linkler = []

# df DataFrame'indeki her "SiparisId" için yeni bir URL oluşturup bu URL'ye git
for index, row in df.iterrows():
    siparis_id = row['SiparisId']
    new_url = f"https://task.haydigiy.com/admin/order/edit/{siparis_id}"

    # Yeni URL'ye git
    driver.get(new_url)
    

    try:
        # Butonları bulmak için XPath ifadesi
        button_xpath = "//button[contains(@onclick, 'javascript:OpenWindow')]"
        buttons = driver.find_elements(By.XPATH, button_xpath)

        # Her bir buton için işlem yap
        for button in buttons:
            try:
                # Butonun içindeki linki al
                onclick_value = button.get_attribute("onclick")
                start_index = onclick_value.find("/admin")
                end_index = onclick_value.find("', '")
                link_part = onclick_value[start_index:end_index]

                # Linkin başına ana URL'yi ekle
                full_link = f"https://task.haydigiy.com{link_part}"

                # İsteği gönder
                driver.get(full_link)
                pass

                # Sayfanın HTML içeriğini al
                page_html = driver.page_source

                # BeautifulSoup ile sayfayı parse et
                soup = BeautifulSoup(page_html, 'html.parser')

                # Sayfada aranacak metinleri kontrol et
                for metin in aranacak_metinler:
                    if soup.find(text=lambda t: t and metin in t):
                        bulunan_linkler.append(full_link)
                        break

            except Exception as e:
                print(f"Buton tıklama işleminde hata: {e}")
    except NoSuchElementException as e:
        print(f"Buton bulunamadı: {e}")

# Bulunan linkleri bir DataFrame'e dönüştür
linkler_df = pd.DataFrame(bulunan_linkler, columns=["Bulunan Linkler"])
linkler_df.to_excel("Kek İçin Kontrol Linkleri.xlsx", index=False)



driver.quit()