from django.core.management.base import BaseCommand
import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

class Command(BaseCommand):
    help = 'Builds a TF-IDF index from chatbot/faq.json and saves it to chatbot/faq_index.pkl'

    def handle(self, *args, **options):
        base = Path(__file__).resolve().parent.parent.parent
        faq_path = base / 'faq.json'
        if not faq_path.exists():
            self.stderr.write('faq.json not found at %s' % faq_path)
            return
        with open(faq_path, 'r', encoding='utf-8') as f:
            faqs = json.load(f)
        questions = [q['question'] for q in faqs]
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(questions)
        out_path = base / 'faq_index.pkl'
        with open(out_path, 'wb') as f:
            pickle.dump({'vectorizer': vectorizer, 'vectors': vectors, 'faqs': faqs}, f)
        self.stdout.write('Built FAQ index with %d questions -> %s' % (len(questions), out_path))
