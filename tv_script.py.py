from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# --- KONFIGURACJA ---
CHROMEDRIVER_PATH = "C:/Users/domin/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
CHANNELS = {
    "AXN": "https://ogladaj.in/tv/?id=axn",
    "AXN Black": "https://ogladaj.in/tv/?id=axnblack",
    "AXN White": "https://ogladaj.in/tv/?id=axnwhite",
    "AXN Spin": "https://ogladaj.in/tv/?id=axnspin",
    "HBO": "https://ogladaj.in/tv/?id=hbo",
    "HBO 2": "https://ogladaj.in/tv/?id=hbo2",
    "HBO 3": "https://ogladaj.in/tv/?id=hbo3",
    "Filmbox Premium": "https://ogladaj.in/tv/?id=filmboxpremium",
    "Filmbox Extra": "https://ogladaj.in/tv/?id=filmboxextra",
    "Filmbox Action": "https://ogladaj.in/tv/?id=filmboxaction",
    "Cinemax": "https://ogladaj.in/tv/?id=cinemax",
    "Cinemax 2": "https://ogladaj.in/tv/?id=cinemax2",
    "FX": "https://ogladaj.in/tv/?id=fx",
    "FX Code My": "https://ogladaj.in/tv/?id=fxcodemy",
    "Paramount Network": "https://ogladaj.in/tv/?id=paramountnetwork",
    "Epic Drama": "https://ogladaj.in/tv/?id=epicdrama",
    "History": "https://ogladaj.in/tv/?id=history",
    "Discovery": "https://ogladaj.in/tv/?id=discovery"
}
OUTPUT_FILE = "KanałyTV.m3u"
REFRESH_INTERVAL = 1800  # 30 minut
MAX_RETRIES = 3  # liczba ponowień przy nieudanym pobraniu

# --- FUNKCJA POBIERANIA LINKU M3U8 Z PONAWIANIEM ---
def fetch_link_with_retry(driver, url, retries=MAX_RETRIES):
    attempt = 0
    while attempt < retries:
        driver.get(url)
        time.sleep(10)
        for request in driver.requests:
            if request.response and ".m3u8" in request.url:
                driver.requests.clear()
                return request.url
        driver.requests.clear()
        attempt += 1
        print(f"⚠️ Próba {attempt}/{retries} nie powiodła się, ponawiam...")
    return None

# --- FUNKCJA POBIERANIA WSZYSTKICH LINKÓW ---
def fetch_all_links(channels):
    service = Service(CHROMEDRIVER_PATH)
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    links = {}
    for name, url in channels.items():
        print(f"Pobieranie: {name}...")
        link = fetch_link_with_retry(driver, url)
        if link:
            print(f"✅ Znaleziono link M3U8 dla {name}: {link}")
        else:
            print(f"❌ Nie znaleziono linku M3U8 dla {name} po {MAX_RETRIES} próbach")
        links[name] = link
    
    driver.quit()
    return links

# --- ZAPIS DO PLIKU M3U ---
def save_m3u_to_file(links_dict):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for name, link in links_dict.items():
            if link:
                f.write(f"#EXTINF:-1,{name}\n")
                f.write(link + "\n")
    print(f"✅ Plik {OUTPUT_FILE} został zaktualizowany")

# --- GŁÓWNA PĘTLA ---
def main():
    while True:
        print("🔄 Pobieranie aktualnych linków M3U8...")
        links = fetch_all_links(CHANNELS)
        save_m3u_to_file(links)
        time.sleep(REFRESH_INTERVAL)

if __name__ == "__main__":
    main()

