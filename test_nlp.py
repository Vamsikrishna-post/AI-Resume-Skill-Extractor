import spacy
import os
from app.nlp_engine import extractor

def test_extraction():
    sample_text = """
    John Doe is a Python developer with experience in React, AWS, and Machine Learning.
    He uses Docker and Kubernetes for DevOps.
    """
    
    print("Testing Skill Extraction...")
    skills = extractor.get_skills(sample_text)
    print(f"Skills Found: {skills}")
    
    keywords = extractor.get_keywords(sample_text)
    print(f"Keywords Found: {keywords}")
    
    freq = extractor.get_skill_frequency(sample_text)
    print(f"Frequency: {freq}")

if __name__ == "__main__":
    test_extraction()
