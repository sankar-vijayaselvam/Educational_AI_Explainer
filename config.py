import torch
import os
from dotenv import load_dotenv

load_dotenv()

# API key Configuration 
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


LANGUAGE_MAP = {
    "English": "English",
    "Tamil": "Tamil",
    "Hindi": "Hindi"
}

# pdf file path 
file_path = "pdf_data/Class_10_English_English_Medium-2024_Edition-www.tntextbooks.in.pdf"

# Set device
device = "cuda:0" if torch.cuda.is_available() else "cpu"

# Parser Text to speech
DESCRIPTION = {
    "English" : "Mary's voice is energetic yet slightly fast in delivery, full of energy and happiness. The recording is very high quality that almost has no background noise.",
    "Tamil" : "jaya's voice is energetic yet slightly fast in delivery, full of energy and happiness. The recording is very high quality that almost has no background noise.",
    "Hindi" : "Divya's voice is energetic yet slightly fast in delivery,full of energy and happiness. The recording is very high quality that almost has no background noise.",

}

# GoogleTranslator_Config
lang = {
    "English": "en",
    "Tamil": "ta",
    "Hindi": "hi"
}

# Create output directory
OUTPUT_DIR = "output"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(f"Setup complete. Output files will be saved in: {OUTPUT_DIR}")