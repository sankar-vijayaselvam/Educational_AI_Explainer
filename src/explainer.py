import soundfile as sf
import json
import time
from deep_translator import GoogleTranslator
from config import LANGUAGE_MAP, lang, DESCRIPTION
from src.large_language_model import RESPONSE_JSON, prompt, llm
from langchain_core.output_parsers import JsonOutputParser
from src.text_to_speech import generate_long_audio, model, tokenizer, description_tokenizer
from operator import itemgetter
from src.embedding_manager import embedding_creator
from config import file_path
from src.document_processor import extract_text
from langchain_community.retrievers import WikipediaRetriever



# Initialize General Knowledge Retriever (Wikipedia)
wiki_retriever = WikipediaRetriever(top_k_results=1, doc_content_chars_max=1000)
print("Wikipedia retriever initialized.")



def generate_explanation(topic: str, language: str = "English", tone: str = "formal"):
    """
    Generates a written explanation and its spoken audio for a given topic using ParlerTTS.
    """
    # Check the User input language
    if language not in LANGUAGE_MAP: 
        raise ValueError(f"Unsupported language for LLM prompt: {language}. Choose from: {list(LANGUAGE_MAP.keys())}")

    # Function to extract the Text from PDF
    pdf_text_data = extract_text(file_path)
    print("The Text data will be Extracted from the PDF file")

    # Function to Create Embeddings and stored it to Vector dB
    pdf_retriever = embedding_creator(pdf_text_data)


    # RAG Retrieval
    try:
        # Retrieve context from PDF (ChromaDB)
        pdf_docs = pdf_retriever.invoke(topic)
        pdf_context = "\n".join([d.page_content for d in pdf_docs])

        # Retrieve context from Wikipedia
        wiki_docs = wiki_retriever.invoke(topic)
        wiki_context = "\n".join([d.page_content for d in wiki_docs])

        full_context = f"PDF Context:\n---\n{pdf_context}\n\nWikipedia Context:\n---\n{wiki_context}"

        print("The Content Retrieval from Chroma db and wikipedia based on topic was successfully done")

    except Exception as e:
        print(f"Warning: RAG retrieval failed: {e}. Relying on LLM knowledge only.")
        full_context = "No specific RAG context could be retrieved."

    # LLM Generation Chain
    explanation_chain = (
        {
            "full_retrieved_context": itemgetter("full_context"),
            "topic": itemgetter("topic"),
            "tone": itemgetter("tone"),
            "response_json": lambda x: json.dumps({"text_explanation": RESPONSE_JSON["text_explanation"]}) # Pass simple JSON schema

        }
        | prompt
        | llm
        | JsonOutputParser()
    )

    try:
        llm_input = {
            "full_context": full_context,
            "topic": topic,
            "tone": tone

        }

        llm_output = explanation_chain.invoke(llm_input)
        text_explanation = llm_output.get("text_explanation", "Error: LLM failed to generate text_explanation.")
        print(f"LLM Explanation Generated:\n{text_explanation}\n")

    except Exception as e:
        print(f"Error during LLM generation: {e}")
        return {"error": "LLM generation failed.", "audio_url": "Error: LLM generation failed."}
    
    with open("output/generated_text.txt","a", encoding="utf-8") as file :
        file.write(f"{topic}\n{time.time()} LLM_Generated_Text:\n    {text_explanation}\n\n")

    # Google Translator
    try:
        google_trans = GoogleTranslator(source='auto', target=lang[language]).translate( text_explanation)
        print(f"Google Translate: {google_trans}")
    except Exception as e:
        print(f"Google Translate error: {e}")

    with open("output/generated_text.txt","a", encoding="utf-8") as file :
        file.write(f"{topic}\n{time.time()} Google_Translator_Text\n   {google_trans}\n\n")


    # ParlerTTs

    # Generate audio for long text
    print("Starting text TTS generation...")
    final_audio = generate_long_audio(model, tokenizer, description_tokenizer, google_trans, DESCRIPTION[language], max_words=40)

    audio_filename = f"output/Audio/{time.time()}_{topic}_explainer_audio.wav"
    # Save the final audio
    sf.write(audio_filename, final_audio, model.config.sampling_rate)
    print("Audio generation completed! Saved as '{topic}_explainer_audio.wav'")


    # Final Output
    return {
        "text_explanation": google_trans,
        "audio_url": audio_filename # The path/url will be the local Colab file path
    }