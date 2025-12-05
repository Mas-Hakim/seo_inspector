# Техническое задание: MVP SEO Inspector (без Selenium)

## 1. Цель MVP

Создать минимальную версию инструмента инспекции веб-сайта, способную автоматически собрать базовые SEO-данные, обнаружить битые ссылки, проанализировать метаданные страницы и сгенерировать HTML-отчёт максимум на четыре экрана.
Все данные должны формироваться **только программно, без ИИ-генерации**.

---

## 2. Функциональные модули MVP

### 2.1. Fetcher (HTTP-загрузчик)

**Библиотека:** `requests`
**Задачи:**

1. Загрузка HTML по URL (GET).
2. Загрузка HEAD для проверки ссылок.
3. Фиксация метаданных:

   * http_status
   * redirect_chain
   * response_time_ms
   * content_type
   * content_length

### 2.2. RobotsParser

**Библиотека:** `urllib.robotparser`
**Задачи:**

1. Стянуть `robots.txt`.
2. Извлечь:

   * allow/disallow
   * crawl-delay
   * sitemap
   * флаг валидности

### 2.3. SitemapLoader

**Библиотека:** `requests`, `xml.etree`
**Задачи:**

1. Загрузить sitemap или sitemap-index.
2. Извлечь список URL + lastmod.

### 2.4. HTMLParser

**Библиотека:** `BeautifulSoup4`
**Задачи:**

1. Парсинг HTML.
2. Извлечение:

   * `<title>`
   * `<meta name=description>`
   * `<meta robots>`
   * `<link rel="canonical">`
   * H1–H6
   * внутренние ссылки
   * внешние ссылки

### 2.5. BrokenLinksChecker (статический)

**Библиотека:** `requests`
**Задачи:**

1. Проверить все ссылки HEAD-запросами.
2. Сформировать список битых ссылок:

   * href
   * источник
   * статус/ошибка

### 2.6. SEOAnalyzer

**Библиотека:** Python стандарт
**Задачи:**

1. Вычисление базовых SEO-метрик:

   * длина title
   * длина description
   * наличие H1
   * количество внутренних ссылок
   * количество внешних ссылок
2. Формирование условного комплексного показателя качества (0–100):

   * title_score
   * meta_score
   * link_score
   * robots_score
   * sitemap_score
   * итоговый weighted_score

### 2.7. ReportGenerator (HTML)

**Библиотека:** чистый Python (Jinja2 по желанию)
**Задачи:**

1. Генерация HTML-отчёта 4 экрана:

   * Блок 1: основная информация о странице
   * Блок 2: метаданные (title, meta, canonical)
   * Блок 3: список битых ссылок (с выделением)
   * Блок 4: комплексный SEO-скор
2. Вставка скриншотов, если есть (пока скриншоты не генерим).
3. Экспорт report.html + assets/

---

## 3. Архитектура классов MVP

### 3.1. Классы

1. **CrawlerController**
   – главный управляющий класс
   – orchestration всех модулей

2. **Fetcher**
   – `fetch_get(url)`
   – `fetch_head(url)`

3. **RobotsParser**
   – `load(url)`
   – `get_rules()`

4. **SitemapLoader**
   – `load(url)`
   – `extract_urls()`

5. **HTMLParser**
   – `parse(raw_html)`
   – `extract_links()`
   – `extract_metadata()`

6. **BrokenLinksChecker**
   – `check(links)` → broken_links

7. **SEOAnalyzer**
   – `score_page(data)`

8. **ReportGenerator**
   – `render_html(data)`

### 3.2. Точки входа

**main.py**:

1. Принимает аргумент `--url`.
2. Запускает `CrawlerController`.
3. Сохраняет `report.html`.

---

## 4. REST API (минимальный)

**GET /inspect?url=...**
– запуск инспекции
– возвращает JSON со всеми данными

**GET /report?task_id=...**
– отдаёт HTML-отчёт

**Инструменты:** Flask или FastAPI

---

## 5. Ограничения MVP

1. Не используем Selenium.
2. Не рендерим JS.
3. Без скриншотов.
4. Без графов ссылок.
5. Один URL за запуск.

---
