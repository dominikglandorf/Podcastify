from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

MIN_WORDS = int(os.getenv("MIN_WORDS"))
MAX_GENERATED_TOKENS = int(os.getenv("MAX_GENERATED_TOKENS"))
MODEL = os.getenv("MODEL")
TEMPERATURE = float(os.getenv("TEMPERATURE"))

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
    prompt = f"Generate a podcast with one speaker in '{language}' about '{topic}' on CEFR level {language_level}. Just return the text of the speaker. Do not include a title."

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

    # print(messages)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_completion_tokens=MAX_GENERATED_TOKENS)
    
    #print(completion)
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