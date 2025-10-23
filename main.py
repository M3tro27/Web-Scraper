from os import mkdir, path
import requests
from bs4 import BeautifulSoup
from datetime import datetime

year = datetime.now().year

'''
This block checks directory existence. If folders are existing, it moves along, if not, it generates it.
'''
if path.exists("./data/"):
    print("Data folder exists...\n")
else:
    print("Data folder not found, creating...\n")
    mkdir("./data/")

if path.exists(f"./data/{year}"):
    print(f"{year} folder exists...\n")
else:
    print(f"{year} folder not found, creating...\n")
    mkdir(f"./data/{year}")



