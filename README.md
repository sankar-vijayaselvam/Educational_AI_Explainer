# Educational AI Explainer

## Project Overview
An intelligent educational assistant that generates multilingual explanations with text-to-speech capabilities using RAG (Retrieval-Augmented Generation) and AI technologies.

---

## Features
- Multilingual Support: Generate explanations in English, Tamil, and Hindi
- Text-to-Speech: Convert generated explanations to natural-sounding audio using Indic-Parler TTS
- RAG Integration: Combines PDF content with Wikipedia knowledge for accurate explanations
- Tone Customization: Choose between friendly (for younger students) or formal (for older students) tones
- Google Translate Integration: Seamless translation between supported languages
- Vector Database: Uses ChromaDB for efficient document retrieval

---

## Tech Stack
- AI/ML: LangChain, Groq API (Llama 3.3 70B), Hugging Face Transformers
- Text-to-Speech: Indic-Parler TTS by AI4Bharat
- Translation: Deep Translator with Google Translate
- Vector Database: ChromaDB with Hugging Face embeddings
- Document Processing: PyPDF for PDF text extraction
- Audio Processing: SoundFile, NumPy

---

## Prerequisites
- Python 3.8+
- GPU (recommended for TTS generation)
- Groq API key  ( for LLM Integration)
- Google Drive (for PDF storage)
- Huggingface API key ( for TTS Model Integration )

---

## Installation & Setup

### 1 Clone Repository
```bash
git clone  https://github.com/sankar-vijayaselvam/Educational_AI_Explainer.git         
cd Educational_AI_Explainer
```

### 2 Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv/Scripts/activate      # Windows
```

### 3 Install Requirements
```bash
pip install -r requirements.txt
```

### 4 Create a folder for add pdf file and paste the file path in variable

### 5 Create .env file and add the groq_key named GROQ_API_KEY

### 6 Provide a topic name, language and tone in main.py

### 7 Run the main file
```bash
python main.py
```



  
