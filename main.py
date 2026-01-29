import requests
from random import randint
import sqlite3
from requests.exceptions import RequestException

class DATABASE():
    @staticmethod
    def CreateDB():
        conn = sqlite3.connect('IPMAP.db')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS noip (no_ip TEXT, reason TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS yesip (yes_ip TEXT, statu TEXT)")
        conn.commit()
        conn.close()

    @staticmethod
    def SaveNoIP(IP, reason="Erisim Yok"):
        conn = sqlite3.connect('IPMAP.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO noip (no_ip, reason) VALUES (?, ?)", (IP, reason))
        conn.commit()
        conn.close()

    @staticmethod
    def SaveYesIP(IP, statu):
        conn = sqlite3.connect('IPMAP.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO yesip (yes_ip, statu) VALUES (?, ?)", (IP, statu))
        conn.commit()
        conn.close()

def get_random_public_ip():
    while True:
        first = randint(1, 223)
        if first in [10, 127, 169, 172, 192]:
            continue
        return f"{first}.{randint(0,255)}.{randint(0,255)}.{randint(0,255)}"

def start_mapping(active=False):
    print("--- IP Tarama Islemi Baslatildi ---")
    while active:
        randomIP = get_random_public_ip()
        url = f"http://{randomIP}" 
        
        try:
            response = requests.get(url, timeout=1, verify=False)
            
            if response.status_code == 200:
                print(f"[+] BULUNDU: {randomIP}")
                DATABASE.SaveYesIP(randomIP, "Aktif")
            else:
                print(f"[-] BULUNAMADI: {randomIP} (Kod: {response.status_code})")
                DATABASE.SaveNoIP(randomIP, f"Durum: {response.status_code}")
        
        except RequestException:
            print(f"[-] BULUNAMADI: {randomIP}")
            DATABASE.SaveNoIP(randomIP, "Erisim Yok")
        except KeyboardInterrupt:
            print("\nIslem durduruldu.")
            break

if __name__ == "__main__":
    DATABASE.CreateDB()
    start_mapping(True)
