import requests

# Robots.txt
robots_page = requests.get('https://www.echo24.cz/robots.txt')
with open("robots.txt", "w") as f:
    f.write(robots_page.text)

# WebPage
page = requests.get('https://www.echo24.cz/a/Hf6u8/zpravy-domov-babis-vyzval-koncici-vladu-aby-necinila-zasadni-rozhodnuti')
with open("page.html", "w") as f:
    f.write(page.text)

# Image
image = requests.get('https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwallpaperaccess.com%2Ffull%2F2111331.jpg&f=1&nofb=1&ipt=a3f02630d4d3cf0df30decf5dc12bca18870b9d4db236a7b15d86b542cbf75de')
with open("image.png", "wb") as f:
    f.write(image.content)
