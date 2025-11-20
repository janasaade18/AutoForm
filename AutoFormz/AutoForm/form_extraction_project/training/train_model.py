import spacy
from spacy.training.example import Example
import random
import os

# EXPANDED TRAINING DATA
TRAIN_DATA = [
    # Standard Label Format
    ("Name: John Smith Major: Computer Science GPA: 3.8", 
     {"entities": [(6, 16, "STUDENT_NAME"), (24, 40, "MAJOR"), (46, 49, "GPA")]}),

    # Different Labels (Student / Program)
    ("Student: Sarah Connor. Program: Mechanical Engineering. Grade Point Average: 4.0", 
     {"entities": [(9, 21, "STUDENT_NAME"), (32, 54, "MAJOR"), (77, 80, "GPA")]}),

    # ID Card Style (Short, concise)
    ("ID: 12345  Name: Michael Jordan  Dept: Basketball  GPA: 2.5", 
     {"entities": [(17, 31, "STUDENT_NAME"), (39, 49, "MAJOR"), (56, 59, "GPA")]}),

    # Resume / Header Style
    ("CANDIDATE: Alice Wonderland | FIELD: Arts & Design | FINAL SCORE: 3.92", 
     {"entities": [(11, 27, "STUDENT_NAME"), (37, 50, "MAJOR"), (66, 70, "GPA")]}),

    # Official Document Style
    ("University of Technology. Student Name: Robert Downey Jr. Enrolled in: Physics. Cumulative GPA: 3.1", 
     {"entities": [(40, 57, "STUDENT_NAME"), (71, 78, "MAJOR"), (96, 99, "GPA")]}),

    # Lowercase / Chatty Style
    ("name is jenny lopez, she studies biology and has a gpa of 3.5", 
     {"entities": [(8, 19, "STUDENT_NAME"), (33, 40, "MAJOR"), (58, 61, "GPA")]}),

    # Reverse Order (GPA first)
    ("GPA: 3.75 - Student: Tom Hanks - Major: Drama", 
     {"entities": [(5, 9, "GPA"), (21, 30, "STUDENT_NAME"), (40, 45, "MAJOR")]}),

    # No Labels (Hard mode - relying on context)
    ("Transcript for Bruce Wayne. Major in Criminal Justice. 4.0 GPA.", 
     {"entities": [(15, 26, "STUDENT_NAME"), (37, 53, "MAJOR"), (55, 58, "GPA")]}),

    # Messy / OCR Noise
    ("StdName: Clark Kent  Mjr: Journalism  Score: 3.8", 
     {"entities": [(9, 19, "STUDENT_NAME"), (26, 36, "MAJOR"), (45, 48, "GPA")]}),

    # Decimal variations
    ("Diana Prince. Anthropology. 4.0", 
     {"entities": [(0, 12, "STUDENT_NAME"), (14, 26, "MAJOR"), (28, 31, "GPA")]})
]

def train_model():
    print("Starting AI Training with Expanded Dataset...")
    
    # Load a blank English model
    nlp = spacy.blank("en")
    
    # Add the NER (Named Entity Recognition) pipeline
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner", last=True)
    
    # Add labels from our data
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # Start training
    optimizer = nlp.begin_training()
    
    # Loop 40 times
    for itn in range(40):
        random.shuffle(TRAIN_DATA)
        losses = {}
        
        # Process batches
        for text, annotations in TRAIN_DATA:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.3, losses=losses)
            
        if (itn + 1) % 5 == 0:
            print(f"Iteration {itn+1} - Loss: {losses}")

    # Save the trained model
    output_dir = "models/custom_form_model"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    nlp.to_disk(output_dir)
    print(f"Model saved to '{output_dir}'")
    print("Training complete. The AI now understands multiple form layouts.")

if __name__ == "__main__":
    train_model()