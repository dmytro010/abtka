from __future__ import annotations

import html
import json
import re
from datetime import datetime, UTC
from pathlib import Path
from typing import Dict, List, Tuple

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup


ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"
SITE_URL = "https://abtka.com"
DEFAULT_OG_IMAGE = f"{SITE_URL}/images/abtka_logo.png"

SKIP_FILES = {
    "abtka_redesign.html",
    "abtka_redesign копія.html",
    "index_modern.html",
    "new_design.html",
    "znak_poshti_old.html",
}

SOCIAL_LINKS = [
    {"label": "YouTube", "href": "https://www.youtube.com/channel/UC105o4WQ8npQP4g2YjPk14g", "icon": "images/youtube_logo.svg"},
    {"label": "Instagram", "href": "https://www.instagram.com/abtkacom", "icon": "images/insta_logo.svg"},
    {"label": "TikTok", "href": "https://www.tiktok.com/@dmytroabtka", "icon": "images/tiktok_logo.svg"},
    {"label": "Telegram", "href": "https://t.me/abtkacom", "icon": "images/telegram_logo.svg"},
]

INDEX_CARDS = [
    {
        "href": "robota-z-textom-na-mac.html",
        "title": "Робота з текстом",
        "description": "Все, що потрібно для набору, виділення, копіювання і швидкого старту.",
        "links": [
            {"href": "yak_vidility_text_na_mac.html", "label": "Як виділити текст"},
            {"href": "yak_skopouvaty_text_na_mac.html", "label": "Копіювання та вставка"},
            {"href": "diktuvannia-tekstu.html", "label": "Диктування тексту"},
            {"href": "odna-rich-iaka-bisit-novachkiv-na-mak.html", "label": "Лайвхак для новачків"},
        ],
    },
    {
        "href": "robota-z-faylami-na-mac.html",
        "title": "Робота з файлами",
        "description": "Базові дії з папками, документами і впорядкуванням робочого простору.",
        "links": [
            {"href": "yak_stvority_papku_na_macbook.html", "label": "Створення папок"},
            {"href": "how_to_delete_file_on_mac.html", "label": "Видалення файлів"},
            {"href": "yak_shukati_na_mac.html", "label": "Пошук документів"},
            {"href": "yak_vidility_file_na_mac.html", "label": "Виділення декількох файлів"},
            {"href": "yak-ochistiti-pamiat-na-mac.html", "label": "Очищення пам'яті", "accent": True, "badge": "нове"},
        ],
    },
    {
        "href": "robota-z-programami-na-mac.html",
        "title": "Програми",
        "description": "Огляд системних застосунків і дії, які найчастіше потрібні щодня.",
        "links": [
            {"href": "znayomstvo_z_programami_na_mac.html", "label": "Огляд вбудованих програм"},
            {"href": "yak_primusovo_zavershiti_programu.html", "label": "Примусове закриття"},
            {"href": "robota-z-programami-na-mac.html", "label": "Всі гайди по софту"},
        ],
    },
    {
        "href": "klaviatura_mac.html",
        "title": "Клавіатура",
        "description": "Мова, символи, підсвітка і комбінації клавіш без зайвого технічного шуму.",
        "links": [
            {"href": "klaviatura_mac.html", "label": "Розташування клавіш"},
            {"href": "yak_peremknuti_movu_na_mac.html", "label": "Зміна мови"},
            {"href": "yak_postavity_apostrof_na_mac.html", "label": "Апостроф та символи"},
            {"href": "vimknuti-pidsvitku-klaviaturi-makbuku.html", "label": "Керування підсвіткою"},
            {"href": "main_key_shortcuts_on_mac.html", "label": "Гарячі клавіші"},
        ],
    },
    {
        "href": "poradi-brauzer-safari-na-mak.html",
        "title": "Safari",
        "description": "Нотатки про вкладки, кеш, історію і дрібні дії, що економлять час.",
        "links": [
            {"href": "poradi-brauzer-safari-na-mak.html", "label": "Safari як основний браузер"},
            {"href": "safari-na-mak-iak-onoviti-storinku.html", "label": "Робота з вкладками"},
            {"href": "iak-ochistiti-kesh-v-safari.html", "label": "Очищення кешу та історії"},
            {"href": "safari-na-mak-iak-vidnoviti-zakritu-vkladku.html", "label": "Відновлення вкладок"},
        ],
    },
    {
        "href": "robota_z_foto_na_mac.html",
        "title": "Медіа та система",
        "description": "Фото, відео, жести і скріншоти в одному спокійному наборі корисних записів.",
        "links": [
            {"href": "robota_z_foto_na_mac.html", "label": "Редагування фото без софту"},
            {"href": "znimok_ekranu_na_mac.html", "label": "Скріншоти та запис екрану"},
            {"href": "jesti_na_mac_touchpad.html", "label": "Жести трекпеду"},
            {"href": "robota_z_video_na_mac.html", "label": "Робота з відео"},
        ],
    },
]

CATEGORY_PAGES = {
    "text": {"href": "robota-z-textom-na-mac.html", "label": "Робота з текстом на мак"},
    "files": {"href": "robota-z-faylami-na-mac.html", "label": "Робота з файлами на мак"},
    "apps": {"href": "robota-z-programami-na-mac.html", "label": "Робота з програмами на мак"},
    "keyboard": {"href": "klaviatura_mac.html", "label": "Клавіатура Mac"},
    "safari": {"href": "poradi-brauzer-safari-na-mak.html", "label": "Поради по Safari"},
    "media": {"href": "robota_z_foto_na_mac.html", "label": "Медіа та система"},
}

TOP_SEARCHES = [
    {"href": "iak-postaviti-znak-poshti-na-mak.html", "label": "Як поставити знак пошти @ на Mac", "meta": "334 кліки"},
    {"href": "iak-postaviti-lapki-na-mak.html", "label": "Як поставити лапки на Mac", "meta": "221 клік"},
    {"href": "yak_postavity_komu_na_mac.html", "label": "Як поставити кому на Mac", "meta": "182 кліки"},
    {"href": "yak_postavity_apostrof_na_mac.html", "label": "Як поставити апостроф на Mac", "meta": "172 кліки"},
    {"href": "pokazuiu-iak-postaviti-slesh-na-mak.html", "label": "Як поставити слеш / на Mac", "meta": "162 кліки"},
    {"href": "pokazuiu-iak-postaviti-nizhnie-pidkreslennia-na-mak.html", "label": "Як поставити нижнє підкреслення _ на Mac", "meta": "160 кліків"},
    {"href": "iak-postaviti-znak-nomer-na-mak.html", "label": "Як поставити символ номер № на Mac", "meta": "151 клік"},
    {"href": "pokazuiu-iak-postaviti-znak-pitannia-na-mak.html", "label": "Як поставити знак питання ? на Mac", "meta": "76 кліків"},
    {"href": "safari-na-mak-iak-pereglianuti-istoriiu.html", "label": "Як переглянути історію Safari на Mac", "meta": "69 кліків"},
    {"href": "iak-postaviti-tire-na-mak.html", "label": "Як поставити тире на Mac", "meta": "66 кліків"},
]

SPECIAL_ARTICLE_CONTENT = {
    "klaviatura_mac.html": {
        "title": "Вивчаємо клавіатуру мак. Розташування, функції клавіш",
        "lead": "Клавіатура Mac має свої особливості: інші позначення клавіш, інші місця для символів і багато корисних дій, які неочевидні після Windows.",
        "body": """
<p>На цій сторінці зібрані найважливіші матеріали про розташування клавіш на Mac, популярні символи і базові функції клавіатури, до яких найчастіше повертаються нові користувачі.</p>

<figure>
  <img src="images/klaviatura_mac.webp" width="500" alt="Клавіатура макбуку">
  <figcaption>Загальний вигляд клавіатури MacBook і розташування основних клавіш.</figcaption>
</figure>

<h2>Популярні питання щодо розташування клавіш на Mac</h2>
<ul>
  <li><a href="yak_postavity_dvokrapku_na_mac.html">Як поставити двокрапку ":" на Mac</a></li>
  <li><a href="yak_postavity_apostrof_na_mac.html">Як поставити апостроф "ʼ" на Mac</a></li>
  <li><a href="yak_postavity_komu_na_mac.html">Як поставити кому "," на Mac</a></li>
  <li><a href="yak_postavity_krapku_na_mac.html">Як поставити крапку "." на Mac</a></li>
  <li><a href="iak-postaviti-krapku-z-komoiu-na-mak.html">Як поставити крапку з комою ";" на Mac</a></li>
  <li><a href="pokazuiu-iak-postaviti-znak-pitannia-na-mak.html">Як поставити знак питання "?" на Mac</a></li>
  <li><a href="pokazuiu-iak-postaviti-vidsotok-na-mak.html">Як поставити знак відсотка "%" на Mac</a></li>
  <li><a href="iak-postaviti-znak-nomer-na-mak.html">Як поставити символ номер "№" на Mac</a></li>
  <li><a href="iak-postaviti-znak-poshti-na-mak.html">Як поставити знак пошти "@" на Mac</a></li>
  <li><a href="pokazuiu-iak-postaviti-nizhnie-pidkreslennia-na-mak.html">Як поставити нижнє підкреслення "_" на Mac</a></li>
  <li><a href="pokazuiu-iak-postaviti-znak-plius-na-mak.html">Як поставити плюс "+" на Mac</a></li>
  <li><a href="iak-postaviti-dorivniuie-na-mak.html">Як поставити знак "=" на Mac</a></li>
  <li><a href="iak-postaviti-tire-na-mak.html">Як поставити тире "-" на Mac</a></li>
  <li><a href="iak-postaviti-zirochku-na-mak.html">Як поставити зірочку "*" на Mac</a></li>
  <li><a href="iak-postaviti-lapki-na-mak.html">Як поставити лапки на Mac</a></li>
  <li><a href="iak-postaviti-duzhki-na-mak.html">Як поставити дужки на Mac</a></li>
  <li><a href="bukva_yi_na_mac.html">Де буква "Ї" на клавіатурі Mac</a></li>
  <li><a href="iak-dodati-smail-na-makbutsi.html">Як відкрити клавіатуру смайлів і емодзі на Mac</a></li>
  <li><a href="yak_postavity_symbol_hrivni_na_mac.html">Символ гривні "₴" на клавіатурі Mac</a></li>
  <li><a href="pokazuiu-iak-postaviti-simvol-dolaru-na-mak.html">Як поставити символ долара "$" на Mac</a></li>
  <li><a href="iak-dodati-simvol-ievro-na-makbutsi.html">Як поставити символ євро "€" на Mac</a></li>
  <li><a href="pokazuiu-iak-postaviti-slesh-na-mak.html">Як поставити слеш "/" на Mac</a></li>
  <li><a href="pokazuiu-iak-postaviti-znak-menshe-na-mak.html">Як поставити знак менше "&lt;" на Mac</a></li>
  <li><a href="pokazuiu-iak-postaviti-znak-bilshe-na-mak.html">Як поставити знак більше "&gt;" на Mac</a></li>
</ul>

<h2>Базові клавіші та що вони роблять</h2>
<p><strong>Command</strong> — головна клавіша для більшості швидких дій на Mac. Саме з нею працюють копіювання, вставка, відкриття нової вкладки, пошук і десятки інших комбінацій.</p>
<p><strong>Option</strong> — допомагає вводити додаткові символи і відкривати альтернативні дії в macOS.</p>
<p><strong>Control</strong> — використовується в системних скороченнях і контекстних діях. Наприклад, `Control + Space` часто перемикає мову або відкриває налаштування джерел вводу.</p>
<p><strong>Enter</strong> — підтверджує дію, створює новий рядок і часто працює як кнопка "ОК" у формах та діалогах.</p>
<p><strong>Tab</strong> — переходить між полями вводу і допомагає рухатися по інтерфейсу без мишки.</p>
<p><strong>Caps Lock</strong> — вмикає великі літери. На частині Mac його також можна переналаштувати для зміни мови.</p>
<p><strong>Delete</strong> — видаляє символ ліворуч від курсора. Для видалення праворуч часто використовують `Fn + Delete`.</p>
<p><strong>Fn</strong> — змінює поведінку верхнього ряду клавіш і бере участь у навігаційних комбінаціях.</p>

<h2>Що роблять клавіші F1-F12 на MacBook</h2>
<ul>
  <li><strong>F1</strong> — зниження яскравості дисплея.</li>
  <li><strong>F2</strong> — підвищення яскравості дисплея.</li>
  <li><strong>F3</strong> — відкриття Mission Control.</li>
  <li><strong>F4</strong> — відкриття Launchpad.</li>
  <li><strong>F5</strong> — зменшення яскравості підсвітки клавіатури.</li>
  <li><strong>F6</strong> — підвищення яскравості підсвітки клавіатури.</li>
  <li><strong>F7</strong> — попередній трек.</li>
  <li><strong>F8</strong> — пауза або відтворення.</li>
  <li><strong>F9</strong> — наступний трек.</li>
  <li><strong>F10</strong> — зменшення гучності.</li>
  <li><strong>F11</strong> — вимкнення звуку.</li>
  <li><strong>F12</strong> — підвищення гучності.</li>
</ul>

<p>Якщо хочеш швидше розібратися з клавіатурою в цілому, відкрий також <a href="main_key_shortcuts_on_mac.html">головні гарячі клавіші Mac</a> і <a href="yak_peremknuti_movu_na_mac.html">гайд про перемикання мови</a>.</p>
""",
    }
}


def strip_tags(value: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", value)).strip()


def clean_html_fragment(fragment: str) -> str:
    fragment = re.sub(r"<!--.*?-->", "", fragment, flags=re.S)
    fragment = re.sub(r"\sstyle=(['\"]).*?\1", "", fragment, flags=re.S | re.I)
    fragment = re.sub(r'\sclass="[^"]*(?:title|subtitle)[^"]*"', "", fragment, flags=re.I)
    fragment = re.sub(r"<figure>\s*(?:<img[^>]*abtka_logo[^>]*>\s*)?(?:<img[^>]*ukraine[^>]*>\s*)?</figure>", "", fragment, flags=re.S | re.I)
    fragment = re.sub(r"<script\b.*?</script>", "", fragment, flags=re.S | re.I)
    fragment = re.sub(r"\s{3,}", "\n\n", fragment)
    return fragment.strip()


def normalize_local_urls(fragment: str, page_path: Path) -> str:
    asset_prefix = "../" * (len(page_path.parts) - 1)

    def repl(match: re.Match[str]) -> str:
        attr, quote, raw_value = match.groups()
        value = raw_value.strip()

        if (
            value.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:"))
            or value.startswith("/")
        ):
            return match.group(0)

        suffix = ""
        for marker in ("#", "?"):
            if marker in value:
                value, rest = value.split(marker, 1)
                suffix = marker + rest
                break

        normalized = value.lstrip("./")
        while normalized.startswith("../"):
            normalized = normalized[3:]

        if normalized.startswith(("images/", "videos/", "css/", "scripts/")):
            final_value = f"{asset_prefix}{normalized}{suffix}"
        else:
            final_value = f"{asset_prefix}{normalized}{suffix}"

        return f'{attr}={quote}{final_value}{quote}'

    return re.sub(r'(href|src)=(["\'])(.*?)\2', repl, fragment, flags=re.I)


def extract_title(text: str) -> str:
    match = re.search(r"<title>\s*(.*?)\s*</title>", text, flags=re.S | re.I)
    return strip_tags(match.group(1)) if match else "Abtka.com"


def extract_description(text: str) -> str:
    patterns = [
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
        r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']',
        r'<meta\s+description=["\'](.*?)["\']',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.S | re.I)
        if match:
            return " ".join(strip_tags(match.group(1)).split())
    return ""


def clean_seo_title(title: str) -> str:
    cleaned = title.strip()
    for suffix in ("| Abtka.com", "— Abtka.com", "- Abtka.com", ". Макбучна абетка.", "Макбучна абетка."):
        if cleaned.endswith(suffix):
            cleaned = cleaned[: -len(suffix)].strip()
    return cleaned


def iso_lastmod(path: Path) -> str:
    modified = datetime.fromtimestamp(path.stat().st_mtime, tz=UTC)
    return modified.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_url_for(page_path: Path) -> str:
    relative = page_path.as_posix()
    if relative == "index.html":
        return f"{SITE_URL}/"
    return f"{SITE_URL}/{relative}"


def build_json_ld(page_type: str, page_path: Path, meta_title: str, meta_description: str) -> str:
    canonical_url = canonical_url_for(page_path)
    payload = {
        "@context": "https://schema.org",
        "@type": "WebSite" if page_type == "website" else "Article",
        "name": meta_title,
        "url": canonical_url,
        "inLanguage": "uk",
        "publisher": {
            "@type": "Organization",
            "name": "Abtka.com",
            "url": SITE_URL,
            "logo": {
                "@type": "ImageObject",
                "url": DEFAULT_OG_IMAGE,
            },
        },
    }
    if meta_description:
        payload["description"] = meta_description
    if page_type == "article":
        payload["mainEntityOfPage"] = canonical_url
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def extract_modern_page_parts(text: str) -> Tuple[str, str, str] | None:
    header_match = re.search(r"<header class=\"article-header\">\s*(.*?)\s*</header>", text, flags=re.S | re.I)
    body_match = re.search(r'<div class="article-body">\s*(.*?)\s*</div>\s*</article>', text, flags=re.S | re.I)
    if not header_match or not body_match:
        return None

    title_match = re.search(r"<h1\b[^>]*>(.*?)</h1>", header_match.group(1), flags=re.S | re.I)
    lead_match = re.search(r"<p\b[^>]*class=[\"'][^\"']*article-lead[^\"']*[\"'][^>]*>(.*?)</p>", header_match.group(1), flags=re.S | re.I)
    title = strip_tags(title_match.group(1)) if title_match else ""
    lead = strip_tags(lead_match.group(1)) if lead_match else ""
    body = body_match.group(1).strip()
    return title, lead, body


def extract_main_article(text: str) -> str:
    if re.search(r'<meta[^>]+http-equiv=["\']refresh["\']', text, flags=re.I):
        raise ValueError("Redirect page")

    modern_match = re.search(
        r'<div class="article-body">\s*(.*?)\s*</div>\s*</article>',
        text,
        flags=re.S | re.I,
    )
    if modern_match:
        return modern_match.group(1).strip()

    legacy_match = re.search(r"<article\b[^>]*>\s*(.*?)\s*</article>", text, flags=re.S | re.I)
    if legacy_match:
        return legacy_match.group(1).strip()

    main_match = re.search(r"<main\b[^>]*>\s*(.*?)\s*</main>", text, flags=re.S | re.I)
    if main_match:
        return main_match.group(1).strip()
    raise ValueError("Article block not found")


def infer_category(file_name: str) -> str:
    lower = file_name.lower()
    if "safari" in lower:
        return "safari"
    if "docker" in lower:
        return "apps"
    if any(token in lower for token in ("foto", "zobrazh", "video", "screen", "znimok", "jesti", "zhesti")):
        return "media"
    if any(token in lower for token in ("klaviatura", "apostrof", "krapku", "movu", "symbol", "znak", "bukva", "key_shortcuts", "lapki", "tire", "duzhki")):
        return "keyboard"
    if any(token in lower for token in ("file", "papku", "shukati", "storage", "pamiat", "finder", "delete")):
        return "files"
    if any(token in lower for token in ("program", "soft", "docker")):
        return "apps"
    return "text"


def extract_article_heading(article_html: str) -> Tuple[str, str, str]:
    working = article_html
    lead = ""

    working = re.sub(r"\s*<div\b[^>]*class=[\"'][^\"']*breadcrumb[^\"']*[\"'][^>]*>.*?</div>", "", working, count=1, flags=re.S | re.I)

    wrapper_match = re.match(r"\s*<div\b[^>]*>\s*(.*?)\s*</div>", working, flags=re.S | re.I)
    if wrapper_match and re.search(r"<h1\b", wrapper_match.group(1), flags=re.I):
        intro_block = wrapper_match.group(1)
        working = working[wrapper_match.end():].lstrip()
    else:
        intro_block = working

    h1_match = re.search(r"<h1\b[^>]*>(.*?)</h1>", intro_block, flags=re.S | re.I)
    title = strip_tags(h1_match.group(1)) if h1_match else "Нотатка Abtka.com"

    subtitle_match = re.search(r"<p\b[^>]*class=[\"'][^\"']*subtitle[^\"']*[\"'][^>]*>(.*?)</p>", intro_block, flags=re.S | re.I)
    if subtitle_match:
      lead = strip_tags(subtitle_match.group(1))
    else:
      lead_match = re.search(r"<p\b[^>]*>(.*?)</p>", working, flags=re.S | re.I)
      if lead_match:
        candidate = strip_tags(lead_match.group(1))
        if 20 <= len(candidate) <= 220:
          lead = candidate

    working = re.sub(r"\s*<div\b[^>]*>\s*<h1\b.*?</div>", "", working, count=1, flags=re.S | re.I)
    working = re.sub(r"\s*<h1\b[^>]*>.*?</h1>", "", working, count=1, flags=re.S | re.I)
    working = re.sub(r"\s*<p\b[^>]*class=[\"'][^\"']*subtitle[^\"']*[\"'][^>]*>.*?</p>", "", working, count=1, flags=re.S | re.I)
    return title, lead, working.strip()


def extract_sidebar_links(text: str, page_path: Path) -> List[Dict[str, str]]:
    aside_links: List[Dict[str, str]] = []
    modern_aside = re.search(r'<ul class="aside-links">\s*(.*?)\s*</ul>', text, flags=re.S | re.I)
    if modern_aside:
        source = modern_aside.group(1)
    else:
        footer_index = text.lower().find("<footer")
        source = text[footer_index - 2500:footer_index] if footer_index > 0 else text

    seen = set()
    for href, label in re.findall(r'<a\b[^>]*href=["\'](.*?)["\'][^>]*>(.*?)</a>', source, flags=re.S | re.I):
        clean_href = href.strip()
        clean_label = " ".join(strip_tags(label).split())
        if not clean_label or clean_href in {"#", "/", page_path.name, "index.html", "./index.html"}:
            continue
        if clean_href.startswith(("http://", "https://", "mailto:", "tel:")):
            continue
        if clean_href in seen:
            continue
        seen.add(clean_href)
        aside_links.append({"href": clean_href, "label": clean_label})
        if len(aside_links) == 5:
            break
    return aside_links


def extract_backlink(aside_links: List[Dict[str, str]], file_name: str) -> Dict[str, str]:
    category_link = CATEGORY_PAGES[infer_category(file_name)]
    if category_link["href"] != file_name:
        return {"href": category_link["href"], "label": f"Повернутися: {category_link['label']}"}

    for link in aside_links:
        if link["href"] != file_name:
            return {"href": link["href"], "label": f"Повернутися: {link['label']}"}
    return {"href": "index.html#guides", "label": "Повернутися до гайдів"}


def infer_eyebrow(file_name: str) -> str:
    lower = file_name.lower()
    if "safari" in lower:
        return "Нотатка про Safari на Mac"
    if "docker" in lower:
        return "Стаття для розробників на Mac"
    if any(token in lower for token in ("foto", "zobrazh", "video", "screen", "znimok")):
        return "Нотатка про медіа та систему"
    if any(token in lower for token in ("klaviatura", "apostrof", "krapku", "movu", "symbol", "znak", "bukva")):
        return "Нотатка про клавіатуру Mac"
    if any(token in lower for token in ("file", "papku", "shukati", "storage", "pamiat")):
        return "Нотатка про файли та сховище"
    return "Нотатка Abtka.com"


def page_context(page_path: Path) -> Dict[str, object]:
    depth = len(page_path.parts) - 1
    asset_prefix = "../" * depth
    home_href = f"{asset_prefix}index.html"
    nav_items = [
        {"label": "Гайди", "href": f"{home_href}#guides"},
        {"label": "Про сайт", "href": f"{home_href}#about"},
    ]
    return {
        "asset_prefix": asset_prefix,
        "home_href": home_href,
        "nav_items": nav_items,
        "social_links": SOCIAL_LINKS,
        "canonical_url": canonical_url_for(page_path),
        "og_image": DEFAULT_OG_IMAGE,
    }


def build_index(env: Environment) -> None:
    template = env.get_template("index.html")
    page_path = Path("index.html")
    meta_title = "Abtka.com - Макбучна абетка (2026)"
    meta_description = "Прості та зрозумілі інструкції для MacBook українською. Корисні нотатки про macOS, Safari, клавіатуру, файли, фото та відео."
    output = template.render(
        meta_title=meta_title,
        meta_description=meta_description,
        og_type="website",
        json_ld=build_json_ld("website", page_path, meta_title, meta_description),
        hero_notes=["Коротко", "Зрозуміло", "Українською"],
        top_searches=TOP_SEARCHES,
        featured_link={"href": "yak-ochistiti-pamiat-na-mac.html", "label": "Що нового: очищення пам'яті"},
        cards=INDEX_CARDS,
        about_paragraphs=[
            "Мене звати Дмитро. Я зібрав тут прості пояснення для щоденних питань: від символів на клавіатурі до Safari, файлів, скріншотів та інших звичних дій у macOS.",
            "Ідея проста: менше декоративного шуму, більше швидкої допомоги, яку легко знайти й одразу застосувати.",
        ],
        **page_context(page_path),
    )
    (ROOT / "index.html").write_text(output.rstrip() + "\n", encoding="utf-8")


def build_article(env: Environment, relative_path: Path) -> None:
    absolute_path = ROOT / relative_path
    text = absolute_path.read_text(encoding="utf-8")
    special_content = SPECIAL_ARTICLE_CONTENT.get(relative_path.name)
    title_hint = clean_seo_title(extract_title(text))
    if special_content:
        article_title = special_content["title"]
        article_lead = special_content["lead"]
        article_body = special_content["body"]
    else:
        modern_parts = extract_modern_page_parts(text)
        if modern_parts:
            article_title, article_lead, article_body = modern_parts
        else:
            article_html = extract_main_article(text)
            article_title, article_lead, article_body = extract_article_heading(article_html)

    if not article_title or article_title == "Нотатка Abtka.com":
        article_title = title_hint or article_title
    if not article_lead:
        lead_match = re.search(r"<p\b[^>]*>(.*?)</p>", article_body, flags=re.S | re.I)
        if lead_match:
            candidate = strip_tags(lead_match.group(1))
            if 20 <= len(candidate) <= 220:
                article_lead = candidate

    article_body = normalize_local_urls(clean_html_fragment(article_body), relative_path)
    aside_links = extract_sidebar_links(text, relative_path)
    context = page_context(relative_path)
    template = env.get_template("article.html")
    meta_title = extract_title(text)
    meta_description = extract_description(text)

    rendered = template.render(
        meta_title=meta_title,
        meta_description=meta_description,
        og_type="article",
        json_ld=build_json_ld("article", relative_path, meta_title, meta_description),
        eyebrow=infer_eyebrow(relative_path.name),
        backlink=extract_backlink(aside_links, relative_path.name),
        article_title=article_title,
        article_lead=article_lead,
        article_body=Markup(article_body),
        aside_links=aside_links,
        **context,
    )
    absolute_path.write_text(rendered.rstrip() + "\n", encoding="utf-8")


def iter_html_pages() -> List[Path]:
    pages = sorted(
        [
            path.relative_to(ROOT)
            for path in ROOT.rglob("*.html")
            if ".git" not in path.parts and "venv" not in path.parts and path.name not in SKIP_FILES and "templates" not in path.parts
        ]
    )
    return pages


def iter_public_pages() -> List[Path]:
    public_pages = []
    for page_path in iter_html_pages():
        if page_path.name in SKIP_FILES:
            continue
        absolute_path = ROOT / page_path
        text = absolute_path.read_text(encoding="utf-8")
        if re.search(r'<meta[^>]+http-equiv=["\']refresh["\']', text, flags=re.I):
            continue
        public_pages.append(page_path)
    return public_pages


def write_sitemap() -> None:
    urls = []
    for page_path in iter_public_pages():
        absolute_path = ROOT / page_path
        urls.append(
            "\n".join(
                [
                    "<url>",
                    f"<loc>{canonical_url_for(page_path)}</loc>",
                    f"<lastmod>{iso_lastmod(absolute_path)}</lastmod>",
                    f"<priority>{'1.0' if page_path.name == 'index.html' else '0.7'}</priority>",
                    "</url>",
                ]
            )
        )

    sitemap = "\n".join(
        [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
            *urls,
            "</urlset>",
            "",
        ]
    )
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")


def write_robots() -> None:
    robots = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            "Disallow: /cgi-bin/",
            f"Sitemap: {SITE_URL}/sitemap.xml",
            "",
        ]
    )
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")


def main() -> None:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    build_index(env)
    built = []
    skipped = []

    for page_path in iter_html_pages():
        if page_path.name == "index.html":
            continue
        try:
            build_article(env, page_path)
            built.append(str(page_path))
        except Exception as exc:
            skipped.append((str(page_path), str(exc)))

    write_sitemap()
    write_robots()

    print(f"Built {len(built)} article pages.")
    if skipped:
        print(f"Skipped {len(skipped)} pages:")
        for item, reason in skipped:
            print(f"- {item}: {reason}")


if __name__ == "__main__":
    main()
