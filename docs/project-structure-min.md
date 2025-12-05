# **Минимальная рабочая структура проекта**

## **1. Входные данные**

* URL сайта
* Настройки: user-agent, timeout, depth=1

---

# **2. Модули и функции**

## **2.1. Модуль: `fetch.py`**

Функции:

1. `fetch_html(url)` — получает HTML через `requests`
2. `fetch_headers(url)` — HEAD запрос
3. `fetch_robots(url)` — использует `urllib.robotparser`
4. `fetch_sitemap(url)` — ищет вручную + парсит XML

---

## **2.2. Модуль: `parse_html.py`**

Функции:

1. `parse_title(html)`
2. `parse_description(html)`
3. `parse_h1(html)`
4. `parse_links(html)` — `<a>`
5. `parse_images(html)` — `<img>` + alt
6. `parse_meta_robots(html)` — `<meta name="robots">`

Библиотека: **BeautifulSoup4**

---

## **2.3. Модуль: `crawler.py`**

Функции:

1. `check_links(links)` — проверка статусов (200/404/301)
2. `check_images(images)` — статус изображений
3. `check_lighthouse_basic(url)` — если нужно Selenium (минимум)

---

## **2.4. Модуль: `seo_metrics.py`**

Функции вычислений (только формулы, никаких ИИ):

1. **Title Quality Score**
2. **Meta Description Score**
3. **H1 Presence Score**
4. **Broken Links Score**
5. **Image Alt Score**
6. **robots.txt Compliance Score**
7. **Sitemap Presence Score**

Финальный показатель:

```
SEO_QUALITY = weighted_sum(metrics)
```

---

## **2.5. Модуль: `report_html.py`**

Генерация HTML-файла на 4 экрана (примерно 2000–2500px высоты):

Блоки:

1. Основная информация (URL, время сканирования)
2. Технические данные (robots/sitemap/headers)
3. Контентные данные (title/description/h1/images)
4. Ссылки (внутренние/внешние/битые)
5. Финальная метрика SEO_QUALITY

---

# **3. Дерево проекта (минимум)**

```
seo_auditor/
    main.py
    fetch.py
    parse_html.py
    crawler.py
    seo_metrics.py
    report_html.py
    templates/
        report_template.html
```

---

# **4. Рабочий процесс (pipeline)**

1. Ввод URL →
2. Проверка robots.txt →
3. Загрузка HTML →
4. Парсинг →
5. Проверка ссылок и изображений →
6. Расчет метрик →
7. Генерация HTML-отчёта →
8. Сохранение отчёта → завершено.

---
