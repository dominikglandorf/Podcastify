
from flask import Flask, jsonify, request
from openai import OpenAI

MIN_WORDS = 5
MAX_GENERATED_TOKENS = 96

app = Flask(__name__)

@app.route('/generate_podcast/mock', methods=['POST'])
def generate_podcast_mock():

    # mock response
    podcast_text = [
        "Bonjour et bienvenue à notre podcast !",
        "Aujourd'hui, nous parlons d'aller au supermarché.",
        "Le supermarché est un endroit pratique pour faire les courses.",
        "On peut acheter beaucoup de choses : des fruits, des légumes, du pain, et même des produits de nettoyage.",
        "Quand on arrive au supermarché, on prend un caddie ou un panier.",
        "Ensuite, on commence par choisir ce dont on a besoin.",
        "Par exemple, dans le rayon des fruits, il y a des pommes, des bananes, et des oranges.",
        "Dans le rayon des produits frais, on trouve du lait, du yaourt, et du fromage.",
        "Il est important de regarder les prix et les promotions.",
        "Après avoir tout choisi, on va à la caisse pour payer.",
        "On peut payer en espèces, par carte bancaire, ou même avec une application mobile.",
        "C'est pratique et rapide !",
        "Et voilà, c'est terminé pour aujourd'hui.",
        "Merci de nous avoir écoutés, et à bientôt pour un nouvel épisode !"
    ]

    return jsonify({"success": True, "podcast": podcast_text})

def chunk(text):
    output = []
    chunk = ""
    for word in text.split():
        chunk += word + " "
        if len(chunk.split()) >= MIN_WORDS and ("!" in word or "." in word or "?" in word):
            output.append(chunk)
            chunk = ""
    return output

@app.route('/generate_podcast/2', methods=['POST'])
def generate_podcast_2():

    language = str(request.json['language']) # for example, fr, en, ...
    language_level = str(request.json['language_level']) # for example, A1, A2, ...
    topic = str(request.json['topic']) # for example: "Going to the supermarket"
    
    # optional parameters
    history = list(request.json['history']) if 'history' in request.json else []
    new_words = list(request.json['new_words']) if 'new_words' in request.json else []
    
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
    podcast_text = chunk(text)
    return jsonify({"success": True, "podcast": podcast_text})

@app.route('/define', methods=['POST'])
def define():

    word = str(request.json['word'])
    chunk = str(request.json['chunk'])

    prompt = f"Describe the definition of '{word}' within 25 words, and explain what it means in the context of '{chunk}'."

    client = OpenAI()

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": prompt
        }
    ]

    completion = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    print(completion)
    text = completion.choices[0].message.content
    return jsonify({"success": True, "definition": text})


@app.route('/test', methods=['POST'])
def test_api():
    test1 = str(request.json['test1'])
    test2 = int(request.json['test2'])
    result = ""
    for i in range(test2):
        result += test1 + "-"
    return jsonify({"success": True, "result": result})

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5001, debug = True)
