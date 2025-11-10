
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from config import GROQ_API_KEY

# Create Environment Variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Initialize LLM
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.7
)

# Define the expected JSON output format
RESPONSE_JSON = {
    "text_explanation": "The generated educational explanation.",
    "audio_filename": "The relative path to the generated audio file (e.g., output/topic.mp3)."
}

# Create the LLM Prompt Template
prompt = ChatPromptTemplate.from_messages(
      [
          ("system", """You are an AI Education Assistant. Your task is to generate a concise, accurate, and age-appropriate explanation about the user's topic.

                      - **Length:** The explanation must be between 80 to 150 words.
                      - **Language:** Write the explanation entirely in English.
                      - **Tone:** Use a {tone} tone. The friendly tone is for younger students. The formal tone is for older students.
                      - **Context:** Use the provided context (RAG) AND your internal knowledge base. Prioritize accuracy.
                      - **Output:** Respond ONLY with a single JSON object that strictly adheres to the following schema. DO NOT include any other text or markdown outside the JSON object: {response_json}

                        RAG Context: {full_retrieved_context}
            """),
          ("human", "Generate an explanation for the topic: '{topic}'")
      ]
  )

