
from flask import Flask, jsonify, request
import generator
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



@app.route('/generate_podcast/2', methods=['POST'])
def generate_podcast_2():

    language = str(request.json['language']) # for example, fr, en, ...
    language_level = str(request.json['language_level']) # for example, A1, A2, ...
    topic = str(request.json['topic']) # for example: "Going to the supermarket"
    
    # optional parameters
    history = list(request.json['history']) if 'history' in request.json else []
    new_words = list(request.json['new_words']) if 'new_words' in request.json else []

    print(f"Generating podcast in {language} on topic '{topic}' at level {language_level} with history: {history} and new words: {new_words}")
    
    podcast_text = generator.generate(language, language_level, topic, history, new_words)

    print(f"Generated podcast: {podcast_text}")

    return jsonify({"success": True, "podcast": podcast_text})

@app.route('/define', methods=['POST'])
def define():

    word = str(request.json['word'])
    chunk = str(request.json['chunk'])

    print(f"Defining word '{word}' in context '{chunk}'")

    text = generator.define(word, chunk)

    print(f"Definition: {text}")
    
    return jsonify({"success": True, "definition": text})

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5001, debug = True)
