import spacy
from spacy.matcher import PhraseMatcher
from spacy.pipeline import EntityRuler
import os

SKILL_DB = {
    "Programming Languages": ["Python", "JavaScript", "Java", "C++", "C#", "Ruby", "Go", "Rust", "TypeScript", "PHP", "Swift", "Kotlin"],
    "Web Technologies": ["React", "Angular", "Vue", "Node.js", "Express", "Django", "Flask", "HTML", "CSS", "Tailwind", "Bootstrap", "Next.js"],
    "Data Science & AI": ["Machine Learning", "Deep Learning", "NLP", "PyTorch", "TensorFlow", "Scikit-Learn", "Pandas", "Numpy", "OpenCV", "Data Visualization", "SQL", "Tableau", "PowerBI"],
    "Cloud & DevOps": ["AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Jenkins", "Terraform", "GitHub Actions", "CI/CD", "Linux"],
    "Soft Skills": ["Leadership", "Communication", "Teamwork", "Problem Solving", "Agile", "Scrum", "Project Management", "Critical Thinking"]
}

def build_skill_model():
    print("Initializing Model Building Process...")
    
    try:
        nlp = spacy.load("en_core_web_sm")
    except:
        print("Model not found. Downloading 'en_core_web_sm'...")
        os.system("python -m spacy download en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")

    # Add EntityRuler to the pipeline
    if "entity_ruler" not in nlp.pipe_names:
        ruler = nlp.add_pipe("entity_ruler", before="ner")
    else:
        ruler = nlp.get_pipe("entity_ruler")

    patterns = []
    for category, skills in SKILL_DB.items():
        for skill in skills:
            patterns.append({
                "label": "SKILL", 
                "pattern": skill, 
                "id": category
            })
            # Add lowercase versions for better matching
            if skill.lower() != skill:
                patterns.append({
                    "label": "SKILL", 
                    "pattern": skill.lower(), 
                    "id": category
                })

    ruler.add_patterns(patterns)
    
    # Save the expanded model
    model_path = "app/models/skill_nlp_model"
    if not os.path.exists("app/models"):
        os.makedirs("app/models")
    
    nlp.to_disk(model_path)
    print(f"Model successfully built and saved to {model_path}")

if __name__ == "__main__":
    build_skill_model()
