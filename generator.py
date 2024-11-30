from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

MIN_WORDS = int(os.getenv("MIN_WORDS"))
MAX_GENERATED_TOKENS = int(os.getenv("MAX_GENERATED_TOKENS"))
MODEL = os.getenv("MODEL")
TEMPERATURE = float(os.getenv("TEMPERATURE"))

proficiency_descriptors = {
    "C1": "Understands a wide range of material, including non-standard usage, with attention to finer details and implicit attitudes.",
    "B2": "Understands standard language in social, professional, or academic contexts, identifying viewpoints, attitudes, and mood.",
    "B1": "Understands main points of familiar topics and narratives delivered clearly and slowly in standard language.",
    "A2": "Understands essential information in everyday matters and simple stories if delivered clearly and slowly.",
    "A1": "Can pick out concrete information (e.g. places and times) from short recordings on familiar everyday topics, provided they are delivered very slowly and clearly."
}

def describe_level(level):
    if level in proficiency_descriptors:
        return proficiency_descriptors[level]
    else:
        return ""

def chunk(text):
    output = []
    chunk = ""
    for word in text.split():
        chunk += word + " "
        if len(chunk.split()) >= MIN_WORDS and ("!" in word or "." in word or "?" in word):
            output.append(chunk)
            chunk = ""
    return output

def generate(language, language_level, topic, history=[], new_words=[]):
    prompt = f"Generate a podcast with one speaker in '{language}' about '{topic}' using language on CEFR level '{language_level}' (defined as \"{describe_level(language_level)}\"). Just return the text of the speaker. Do not include a title."

    client = OpenAI()

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": prompt
        }
    ]

    if history:
        messages.append({
            "role": "assistant", 
            "content": " ".join(history)
        })
        messages.append({
            "role": "user", 
            "content": "Continue the podcast (without talking about continuing it)."
        })

    if new_words:
        messages[-1]['content'] += " Try to use these words in the text generation: " + ", ".join(new_words)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_completion_tokens=MAX_GENERATED_TOKENS)
    
    text = completion.choices[0].message.content
    return chunk(text)

def define(word, context):
    prompt = f"Describe the definition of '{word}' within 25 words, and explain what it means in the context of '{context}'. Just output the definition."

    client = OpenAI()

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": prompt
        }
    ]

    completion = client.chat.completions.create(model="gpt-4o-mini", messages=messages)

    return completion.choices[0].message.content