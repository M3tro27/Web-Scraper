from playwright.sync_api import sync_playwright

URL = 'https://www.scrapethissite.com/pages/ajax-javascript/'

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(URL)

    print('> Klikam 2015')
    page.click("a[id='2015']")
    page.wait_for_selector("tr.film")
    print('> Dynamicky obsah nacten')
    movie_locators = page.locator("tr.film")
    all_movies_text = movie_locators.all_inner_texts()

    print(f'> {len(all_movies_text)} nalezenych filmu')
    if all_movies_text:
        print('> Prvnich 5 nalezenych filmu')
        for i, movie in enumerate(all_movies_text[:5]):
            print(f'- {movie.strip()}')
    browser.close()