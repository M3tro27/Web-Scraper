# L1: Analýza webového sídla pro Web Scraping

Můj vybraný web je **echo24.cz**.

---

## Úkol č. 1: Rozbor robots.txt

``` robots.txt
User-agent: *

Disallow:
```

Jelikož soubor neobsahuje žádné restrikce, mám volnou ruku ve scrapování.

---

## Úkol č. 2: Průzkum struktury

### Struktura stránky

``` HTML
<body>
    <div id="st-container" class="st-container">
        <div class="l-wrapper">
            <div class="l-contentArticle">
                <div class="l-article">
                    <main class="articleNewDetail-wrapper">
                        <article class="articleNewDetail">
                            <h1 class="articleNewDetail__title">Lorem ipsum dolor sit amet</h1> // Titulek
                            <p class="articleNewDetail__genre-wrapper">
                                <span class="articleNewDetail__genre h-halfLine h-halfline--top"> // Podtitulek
                            </p>
                            <figure class="articleNewDetail__img">
                                <a href="xxx">
                                    <img src="xxx" alt="xxx"> // Obrázek
                                </a>
                                <figcaption>Lorem ipsum dolor sit amet</figcaption> // Popis obrázku
                            </figure>
                            <div class="articleNewDetail__info">
                                <ul>
                                    <li>
                                        <a rel="author" class="articleNew-opinion__author" href="xxx">Lorem ipsum</a> // Autor
                                    </li>
                                </ul>
                                <time asidemprop="datePublished" class="articleNew-online__time" datetime="2025-10-10T11:53:00+02:00">10. října 2025</time> // Datum
                            </div>
                            <div class="articleNewDetail__content js-content">
                                <p class="perex">Lorem ipsum dolor sit amet</p> // Perex
                                // Samotný obsah článku
                                <p>Lorem ipsum dolor sit amet</p>
                                .
                                <h2 class="mezititulek">Lorem ipsum</h2> // Mezititulek
                                .
                                <p>Lorem ipsum dolor sit amet</p>
                            </div>
                            <p class="articleNewDetail__tags">
                                // Tagy článku
                                <a href="/tag/iqb27" class="btn-tag" rel="tag">Lorem ipsum</a>
                                .
                                .
                                .
                                <a href="/tag/SkaMG" class="btn-tag" rel="tag">amet voluptate</a>
                            </p>
                        </article>
                        <div data-article-position="related"> // Div se souvisejícími články
                            <h2 class="heading-2 h-halfLine h-halfLine--left ">Související články</h2>
                            <ul class="list-related">
                                <li>
                                    <a href="xxx" itemprop="url">Lorem ipsum</a> // Související článek
                                </li>
                                <li>
                                    <a href="xxx" itemprop="url">Lorem ipsum</a>
                                </li>
                                <li>
                                    <a href="xxx" itemprop="url">Lorem ipsum</a>
                                </li>
                            </ul>
                        </div>
                    </main>
                </div>
            </div>
        </div>
    </div>
</body>
```

---

## Úkol č. 3: Selektory

**Titulek**
```JavaScript
titulek = document.querySelector(".articleNewDetail__title").textContent
```

**Podtitulek**
```JavaScript
podtitulek = document.querySelector('.articleNewDetail__genre').textContent
```

**Obrázek**
```JavaScript
obrazekOdkaz = document.querySelector('.articleNewDetail__img img').getAttribute('src')
```

**Popis obrázku**
```JavaScript
popisObrazku = document.querySelector('.articleNewDetail__img figcaption').textContent
```

**Autor**
```JavaScript
autor = document.querySelector('.articleNew-opinion__author').textContent
```

**Datum**
```JavaScript
datum = document.querySelector('.articleNew-online__time').getAttribute('datetime')
```
Využit atribut datetime místo textContent z důvodu standardizovaného formátu ISO 8601

**Perex**
```JavaScript
perex = document.querySelector('.perex').textContent
```

**Článek**
```JavaScript
let clanek = ''
odstavce = document.querySelectorAll('.articleNewDetail__content p:not([class]), .articleNewDetail__content h2')
for (let i = 0; i < odstavce.length; i++){
    clanek += odstavce[i].textContent + '\n'
}
```

**Tagy**
```JavaScript
let tagy = []
list = document.querySelectorAll('.articleNewDetail__tags .btn-tag')
for (let i = 0; i < list.length; i++){
    tagy.push(list[i].textContent)
}
```

**Související články**
```JavaScript
let odkazy = []
list = document.querySelectorAll('.list-related li a')
for (let i = 0; i < list.length; i++){
    odkazy.push(list[i].getAttribute('href'))
}
```





