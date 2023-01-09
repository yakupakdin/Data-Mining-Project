import bs4
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
import requests
import os



search_URL = "https://www.trendyol.com/sr?wc=109404&os=1&sk=1"
path_to_folder_to_create = r"C:\Users\YakupAkdin\PycharmProjects\deneme"


# klasör hedefi yoksa yeni yol oluşturuyoruz.
def create_a_directory(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def download_image(url, dir_name, num):
    # linki verilen resimlerin geldiği fonksiyon ve indirilmesi.
    file_name = str(num) + '.jpg'
    response = requests.get(url)
    # 200 HTTP yanıtı site için tamam durumu anlamına gelir
    if response.status_code == 200:
        with open(os.path.join(dir_name, file_name), 'wb') as file:
            # görüntü verilerini dosyaya yazma kısmı
            file.write(response.content)


create_a_directory(path_to_folder_to_create)
# driverımızın yolunu veriyoruz.
chromeDriverPath = "C:\\Users\\YakupAkdin\\PycharmProjects\\chromedriver.exe"
# Servis sınıfından yeni bir sınıf oluşturuyoruz.
webdriver_service = service.Service(chromeDriverPath)
webdriver_service.start()
options = webdriver.ChromeOptions()
driver = webdriver.Remote(webdriver_service.service_url, options=options)
driver.get(search_URL)
x = input('Kullanıcı Girişi Bekleniyor.')
# sayfa kaynağını değişkene atıyoruz.
page_html = driver.page_source
# bs4ün anlayacağı şekilde parçalıyoruz.
pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
# sayfada parametrede belirtilen etiket ve sınıfı bulan kısım
containers = pageSoup.find_all('div', {'class': 'p-card-wrppr with-campaign-view add-to-bs-card'})
# Beautifulsoup ile şu ana kadar kaç tane kap bulduğumuzu yazdırıyoruz.
len_containers = len(containers)
print(f"{len_containers} tane konteyner bulundu.")
indirilenResimler = 0
for i in range(0, len_containers + 1):
    # trendyol.com da gereken konteynerın xpathını alıyoruz.
    xPath = f"""//*[@id="search-app"]/div/div[1]/div[2]/div[4]
    /div[1]/div/div[{i}]/div[1]/a/div[1]/div[1]/img"""
    #//*[@id="search-app"]/div/div[1]/div[2]/div[5]/div[1]/div/div[3]/div[1]/a/div[1]/div[1]/img
    #//*[@id="search-app"]/div/div[1]/div[2]/div[3]/div[1]/div/div[2]/div[1]/a/div[1]/div[1]/img
    #//*[@id="search-app"]/div/div[1]/div[2]/div[3]/div[1]/div/div[2]/div[1]/a/div[1]/div[1]/img
    #//*[@id="search-app"]/div/div[1]/div[2]/div[3]/div[1]/div/div[19]/div[1]/a/div[1]/div[1]/img
    #//*[@id="search-app"]/div/div[1]/div[2]/div[4]/div[1]/div/div[2]/div[1]/a/div[1]/div[1]/img
    #//*[@id="search-app"]/div/div[1]/div[2]/div[3]/div[1]/div/div[3]/div[1]/a/div[1]/div[1]/img
    #//*[@id="search-app"]/div/div[1]/div[2]/div[3]/div[1]/div/div[5]/div[1]/a/div[1]/div[1]/img
    #//*[@id="search-app"]/div/div[1]/div[2]/div[4]/div[1]/div/div[888]/div[1]/a/div[1]/div[1]/img
    #//*[@id="search-app"]/div/div[1]/div[2]/div[3]/div[1]/div/div[4]/div[1]/a/div[1]/div[1]/img
    #//*[@id="search-app"]/div/div[1]/div[2]/div[4]/div[1]/div/div[4]/div[1]/a/div[1]/div[1]/img
    #//*[@id="i0"]/div/a/div[1]/div[1]/div[1]/div/picture/img
    #//*[@id="i7"]/div/a/div[1]/div[1]/div[1]/div/picture/img
    #//*[@id="search-app"]/div/div[1]/div[2]/div[5]/div[1]/div/div[2]/div[1]/a/div[1]/div[1]/img
    #//*[@id="search-app"]/div/div[1]/div[2]/div[5]/div[1]/div/div[2]/div[1]/a/div[1]/div[1]/img

    try:
        imageElement = driver.find_element(by=By.XPATH, value=xPath)
        imageURL = imageElement.get_attribute("src")
    except selenium.common.exceptions.NoSuchElementException:
        print(f"{i}.Element Bulunamadı")
        continue

    indirilenResimler += 1

    download_image(imageURL,path_to_folder_to_create,indirilenResimler)
    try:
        if download_image:
            print(f"{indirilenResimler}/{len_containers} indirildi.  URL----> {imageURL}")
    except:
        print(f"{indirilenResimler}. Görüntü INDIRILEMEDI!")


print("Bitti")
print(f"{len_containers} resim içinden {indirilenResimler} tane indirildi.")

driver.quit()
webdriver_service.stop()


