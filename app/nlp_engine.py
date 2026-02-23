import spacy
import re
import pandas as pd
from collections import Counter
import os

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

class SkillExtractor:
    def __init__(self):
        self.nlp = nlp

    def extract_text(self, text):
        """Standardize text for processing"""
        return text.strip()

    def get_skills(self, text):
        doc = self.nlp(text)
        categorized = {}
        
        # 1. NER-based extraction (Custom EntityRuler)
        for ent in doc.ents:
            if ent.label_ == "SKILL":
                category = ent.ent_id_ if ent.ent_id_ else "General"
                skill_name = ent.text.title()
                if category not in categorized:
                    categorized[category] = set()
                categorized[category].add(skill_name)
        
        # 2. Hybrid Fallback (Keyword Matching)
        # This ensures we get results even if the model isn't fully trained
        from .model_builder import SKILL_DB
        text_lower = text.lower()
        for category, skills in SKILL_DB.items():
            for skill in skills:
                if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower):
                    if category not in categorized:
                        categorized[category] = set()
                    categorized[category].add(skill.title())
            
        return {cat: sorted(list(skills)) for cat, skills in categorized.items()}

    def get_keywords(self, text, top_n=12):
        """Extract important keywords using Noun Chunks and POS tagging"""
        doc = self.nlp(text)
        
        # Combine noun chunks and important nouns
        candidates = []
        for chunk in doc.noun_chunks:
            if not chunk.root.is_stop and len(chunk.text) > 2:
                candidates.append(chunk.text.lower())
        
        for token in doc:
            if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop and len(token.text) > 2:
                candidates.append(token.text.lower())
        
        return [k for k, _ in Counter(candidates).most_common(top_n)]

    def get_skill_frequency(self, text):
        doc = self.nlp(text)
        freq = {}
        for ent in doc.ents:
            if ent.label_ == "SKILL":
                name = ent.text.title()
                freq[name] = freq.get(name, 0) + 1
 
        if freq:
            return freq
 
        from .model_builder import SKILL_DB
        text_lower = text.lower()
        for _, skills in SKILL_DB.items():
            for skill in skills:
                pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                matches = re.findall(pattern, text_lower)
                if matches:
                    name = skill.title()
                    freq[name] = freq.get(name, 0) + len(matches)
        return freq

extractor = SkillExtractor()
