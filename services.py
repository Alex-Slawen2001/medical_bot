import requests
import re
import feedparser
import time
import html
from deep_translator import GoogleTranslator


translator = GoogleTranslator(source='auto', target='ru')


def clean_text(text):
    text = re.sub('<[^<]+?>', '', text)
    text = html.unescape(text)
    return text.strip()


def translate_text(text):
    try:
        return translator.translate(text)
    except:
        return text


def make_long_fact(title, text):
    text = clean_text(text)
    text = translate_text(text)

    return f"<b>{translate_text(title)}</b>\n\n{text}"


def fetch_medlineplus():
    try:
        feed = feedparser.parse('https://medlineplus.gov/feeds/healthnews.xml')
        facts = []

        for entry in feed.entries[:10]:
            fact = make_long_fact(entry.title, entry.summary)
            facts.append(fact)

        return facts
    except:
        return None


def fetch_fda():
    try:
        r = requests.get(
            'https://api.fda.gov/drug/event.json',
            params={'count': 'patient.reaction.reactionmeddrapt.exact'},
            timeout=10
        )

        if r.status_code == 200:
            data = r.json()

            facts = []
            for item in data.get('results', [])[:10]:
                term = item.get('term', '')
                count = item.get('count', 0)

                text = f"Самый частый побочный эффект: {term}. Зафиксировано {count} случаев."
                facts.append(translate_text(text))

            return facts
    except:
        return None

def get_facts(source):
    if source == "med":
        return fetch_medlineplus()
    elif source == "fda":
        return fetch_fda()