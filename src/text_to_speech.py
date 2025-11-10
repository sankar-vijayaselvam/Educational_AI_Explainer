import torch
import numpy as np
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
from config import device



model = ParlerTTSForConditionalGeneration.from_pretrained("ai4bharat/indic-parler-tts").to(device)
print("TTS Model will be Initialized")
tokenizer = AutoTokenizer.from_pretrained("ai4bharat/indic-parler-tts")
print("TTS Model Tokenizer will be Initialized")
description_tokenizer = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)
print("TTS Description Tokenizer will be Initialized")

def chunk_text(text, max_words=50):
    """Split text into chunks of maximum words"""
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_words:
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def generate_long_audio(model, tokenizer, description_tokenizer, long_text, description, max_words=50):
    """Generate audio for long text by chunking"""
    device = next(model.parameters()).device

    # Prepare description once
    description_input_ids = description_tokenizer(
        description, return_tensors="pt"
    ).to(device)

    # Split long text into chunks
    text_chunks = chunk_text(long_text, max_words=max_words)

    all_audio = []

    for i, chunk in enumerate(text_chunks):
        print(f"Processing chunk {i+1}/{len(text_chunks)}: {chunk[:50]}...")

        # Prepare prompt for current chunk
        prompt_input_ids = tokenizer(chunk, return_tensors="pt").to(device)

        # Generate audio for chunk
        with torch.no_grad():
            generation = model.generate(
                input_ids=description_input_ids.input_ids,
                attention_mask=description_input_ids.attention_mask,
                prompt_input_ids=prompt_input_ids.input_ids,
                prompt_attention_mask=prompt_input_ids.attention_mask
            )

        audio_chunk = generation.cpu().numpy().squeeze()
        all_audio.append(audio_chunk)

        # Add small silence between chunks for natural flow (optional)
        silence_duration = 0.1  # 100ms silence between chunks
        silence_samples = int(silence_duration * model.config.sampling_rate)
        silence = np.zeros(silence_samples)
        all_audio.append(silence)

    # Concatenate all audio chunks
    final_audio = np.concatenate(all_audio)

    return final_audio

