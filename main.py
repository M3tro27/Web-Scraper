from os import makedirs, listdir, fsync
from datetime import datetime
from aiohttp import ClientSession, TCPConnector
import asyncio
from hashlib import md5
from dateparser import parse
import json
from bs4 import BeautifulSoup
import ssl, certifi
from time import sleep, perf_counter
import re

RUBRICS = ['domov', 'komentare', 'svet', 'ekonomika', 'panorama']
BASE_URL = 'https://www.echo24.cz/'
TARGET_DIR = f'./data/echo24/{datetime.now().year}/{datetime.now().month}'
REGEX = [
    r'[A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ]{2,}+(?:-?[A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ]{2,}+)?(?:\s\d+)?(?:[a-z])?', # Zkratky jako ANO, SPD, ODS, MPSV, NÚKIB, NBÚ, MZd, MZe, ...
    r'[A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ][a-záčďéěíňóřšťúůýž]+\s[A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ][a-záčďéěíňóřšťúůýž]+', # Jména ve formátu "Jmeno Prijmeni", false positives - Motorista Gregor, Dále Schillerová atd.
    r'(?:č\.|číslo)\s\d+\/\d{4}\s(?:Sb\.|Sbírky)' # Detekuje cisla zakonu napr. č. 1/1993 Sb., č. 2/1993 Sbírky, číslo 23/1742 Sb., číslo 2222/2222 Sbírky
]


def directory_creation() -> None:
    """Creates directory if it doesn't exist"""
    makedirs(TARGET_DIR, exist_ok=True)


def in_directory(file_name: str) -> bool:
    """Checks if file is in directory"""
    try:
        files = listdir(TARGET_DIR)
        print(f"File {file_name} founded, continuing...")
        return file_name in files
    except FileNotFoundError:
        return False


def write_to_file(data: dict , name: str) -> None:
    """Takes data, makes them JSON and store them to file"""
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    with open(f"{TARGET_DIR}/{name}", "w", encoding='utf-8') as file:
        file.write(json_data)


async def fetch(session: ClientSession, url: str) -> str:
    """Returns HTML content from URL asynchronously"""
    async with session.get(url, timeout=5) as response:
        response.raise_for_status()
        return await response.text()


def parse_rubric_page(html: str) -> list[tuple[str, str]]:
    """Parse rubric page for today's articles"""
    articles = []
    soup = BeautifulSoup(html, 'lxml')
    ul_tag = soup.select_one('.list-flow')
    li_tags = ul_tag.select('li')
    for li_tag in li_tags:
        try:
            article = li_tag.select_one('article')

            # Datum
            p_tag = article.find('p', class_='articleNew-default__author')
            date = ''.join(p_tag.find_all(string=True, recursive=False)).strip().strip()
            date = parse(date[2:], languages=['cs']).strftime('%d%m%Y')
            # print(f"Datum: {date}")

            if date != datetime.today().strftime('%d%m%Y'):
                continue

            # Odkaz na clanek
            url = article.find('a')['href'].strip()
            # print(f"URI: {url}")
            url_hash = md5(url.encode()).hexdigest()[-8:]
            # print(f"Zkraceny hash URL: {url_hash}")

            file_name = f"echo24-{date}-{url_hash}.json"
            # print(f"File name: {file_name}")

            if in_directory(file_name):
                continue
            else:
                articles.append((url, file_name))

        except:
            continue

    return articles


def use_regex(regexes: list[str], text:str) -> list[str]:
    matches = []
    for regex in regexes:
        matches.extend(re.findall(regex, text))
    matches = list(set(matches))
    print(matches)
    return matches


def parse_article(html: str, url: str) -> dict[str, str]:
    """Parses article and returns JSON of it"""
    soup = BeautifulSoup(html, 'lxml')

    # Titulek
    title = soup.find('h1', class_='articleNewDetail__title').text.strip()
    # print(f"Titulek: {title}")

    url = url
    # print(f"URL: {url}")

    date = soup.find('time', class_='articleNew-online__time').get('datetime')
    # print(f"Date: {date}")

    author = soup.find('a', class_='articleNew-opinion__author').text.strip()
    # print(f"Author: {author}")

    source = "echo24.cz"
    # print(f"Source: {source}")

    content_snipped = soup.find('p', class_='perex').text.strip()
    content_snipped = content_snipped.replace('\xa0', ' ')
    # print(f"Content Snipped: {content_snipped}")

    full_div = soup.select('.articleNewDetail__content p:not([class]), .articleNewDetail__content h2')
    full_content = []
    for p in full_div:
        paragraph = p.find_all(string=True, recursive=False)
        text = ''.join(t.strip() for t in paragraph)
        text = text.replace('\xa0', ' ')
        if text:
            full_content.append(text)
    full_content = '\n'.join(full_content)
    # print(f"Full Content: {full_content}")

    tags_p = soup.select('.articleNewDetail__tags .btn-tag')
    tags = [tag.text for tag in tags_p]
    tags.extend(use_regex(REGEX, full_content))
    # print(f"Tags: {tags}")

    data = {
        'title': title,
        'url': url,
        'date': date,
        'author': author,
        'source': source,
        'content_snipped': content_snipped,
        'full_content': full_content,
        'tags': tags
    }
    return data


async def scrape_rubrics(session: ClientSession, rubric: str) -> None:
    """Scrapes rubrics for today's articles"""
    rubric_url = f'{BASE_URL}s/{rubric}'
    rubric_html = await fetch(session, rubric_url)
    article_entries = parse_rubric_page(rubric_html)

    for link, file_name in article_entries:
        url = f'{BASE_URL[:-1]}{link}'
        try:
            html = await fetch(session, url)
            data = parse_article(html, url)
            write_to_file(data, file_name)
            print(f'Saved {file_name}')
        except Exception as e:
            print(f'Failed to scrape {url}: {e}')


async def main() -> None:
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
        tasks = [scrape_rubrics(session, rubric) for rubric in RUBRICS]
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    while True:
        start = perf_counter()
        directory_creation()
        asyncio.run(main())
        end = perf_counter()
        print("Run finished, waiting one hour...")
        print(f'Finished in {(end - start):.2f} seconds')
        sleep(3600)
