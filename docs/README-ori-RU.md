# SEO Inspector MVP (Python)

Минимальный инструмент технической инспекции веб-сайтов.
Выполняет базовый SEO-аудит без рендеринга JavaScript, используя только Python-модули `requests`, `urllib.robotparser`, `BeautifulSoup4` и статическую генерацию HTML-отчёта.

Отчёт формируется в виде аккуратного HTML-интерфейса на основе шаблонов Jinja2, максимум на четыре экрана, без использования ИИ или внешних сервисов.

---

## Возможности

### Основные модули

1. **Fetcher**
   – загрузка HTML и метаданных HTTP (статус, размер, цепочка редиректов, delay).

2. **RobotsParser**
   – извлечение правил robots.txt и sitemap.

3. **SitemapLoader**
   – загрузка sitemap, разбор URL и `lastmod`.

4. **HTMLParser**
   – извлечение `<title>`, `<meta>`, canonical, H1–H6, внутренних и внешних ссылок.

5. **BrokenLinksChecker**
   – проверка всех ссылок HEAD-запросами, фиксация битых адресов.

6. **SEOAnalyzer**
   – вычисление базовых SEO-метрик и сводного quality-score.

7. **ReportGenerator (HTML UI Layer)**
   – генерация красивого HTML-отчёта на основе Jinja2, со статическими стилями и иконками.

---

## Что входит в отчёт

HTML-отчёт включает:

1. **Блок: Общая информация страницы**
2. **Блок: SEO-метаданные**
3. **Блок: Битые ссылки (со статусами и визуальной маркировкой)**
4. **Блок: Комплексный SEO-скор**

Максимальный размер — четыре экрана, статичный HTML без JavaScript.

---

## Архитектура проекта

```
seo_inspector/
    controllers/
        crawler_controller.py
    core/
        fetcher.py
        robots_parser.py
        sitemap_loader.py
        html_parser.py
        broken_link_checker.py
        seo_analyzer.py
    report/
        report_generator.py
        ui_assets_manager.py
        templates/
            report.html.j2
        assets/
            styles.css
            icons/
                warning.svg
                error.svg
                check.svg
    api/
        server.py  (REST API)
main.py
README.md
requirements.txt
```

---

## REST API

Используется FastAPI или Flask.

### Запуск инспекции

```
GET /inspect?url=https://example.com
```

Возвращает JSON со всеми собранными данными.

### Получение HTML-отчёта

```
GET /report/<task_id>
```

Отдаёт готовый HTML-файл + assets.

---

## Установка

```bash
git clone https://github.com/<yourname>/seo-inspector-mvp.git
cd seo-inspector-mvp

pip install -r requirements.txt
```

---

## Запуск из командной строки

```bash
python main.py --url https://example.com
```

Результат будет сохранён в:

```
output/report.html
output/assets/
```

---

## Запуск через REST API

```bash
uvicorn api.server:app --reload
```

Проверка:

```
http://localhost:8000/inspect?url=https://example.com
http://localhost:8000/report/<task_id>
```

---

## Ограничения MVP

* Нет рендеринга JavaScript (Selenium будет во второй версии).
* Нет скриншотов.
* Один URL на запуск.
* Все данные формируются строго программно, без использования ИИ.

---

## Лицензия

MIT License.

---
