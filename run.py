from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

opsi = webdriver.ChromeOptions()
opsi.add_argument('--headless')
servis = Service('chromedriver.exe')
driver = webdriver.Chrome(service=servis, options=opsi)

shopee_link = "https://www.bukalapak.com/products?search%5Bkeywords%5D=iphone"
driver.set_window_size(1300,800)
driver.get(shopee_link)

rentang = 500
for i in range(1,7):
    akhir = rentang * i 
    perintah = "window.scrollTo(0,"+str(akhir)+")"
    driver.execute_script(perintah)
    print("loading ke-"+str(i))
    time.sleep(1)

time.sleep(5)
driver.save_screenshot("iphone.png")
content = driver.page_source
driver.quit()

data = BeautifulSoup(content,'html.parser')

i = 1
base_url = "https://www.bukalapak.com/"

list_nama,list_gambar,list_harga,list_link,list_rating=[],[],[],[],[]

for area in data.find_all('div',class_="bl-flex-item mb-8"):
    print('proses data ke-'+str(i))
    nama = area.find('section',class_="bl-product-card-new__name").get_text()
    gambar = area.find('img')['src']
    harga = area.find('section',class_="bl-product-card-new__prices").get_text()
    link = base_url + area.find('a')['href']
    
    list_nama.append(nama)
    list_gambar.append(gambar)
    list_harga.append(harga)
    list_link.append(link)
    i+=1
    print("------")

df = pd.DataFrame({'Nama':list_nama,'Gambar':list_gambar,'Harga':list_harga,'Link':list_link})
writer = pd.ExcelWriter('Iphone.xlsx')
df.to_excel(writer,'Sheet1',index=False)
writer.close()
