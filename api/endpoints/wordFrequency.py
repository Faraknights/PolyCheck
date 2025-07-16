from flask import Blueprint, request, jsonify
import spacy
from wordfreq import word_frequency

wordFreq_bp = Blueprint('wordFreq', __name__)

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

@wordFreq_bp.route('/', methods=['POST'])
def wordFreq():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Please provide 'text' in JSON body"}), 400

        text = data['text']
        doc = nlp(text)

        words = [token.text.lower() for token in doc if token.is_alpha]

        if not words:
            return jsonify({"error": "No valid words found in text"}), 400

        word_counts = {}
        freqs = []
        rare_words = []

        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
            freq = word_frequency(word, 'en')
            freqs.append(freq)
            if freq < 1e-5:
                rare_words.append(word)

        avg_freq = sum(freqs) / len(freqs)

        return jsonify({
            "total_words": len(words),
            "unique_words": len(set(words)),
            "average_frequency": round(avg_freq, 6),
            "rare_words": list(set(rare_words))[:10],
            "word_frequencies": word_counts
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
