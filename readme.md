# French podcast generation with GPT4o


## Installation

1. Clone the repository or install the package using pip:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure you have the necessary environment variables set up (if applicable). Use a `.env` file for secure configuration:
   ```plaintext
   OPENAI_API_KEY=your_api_key_here
   ```

---

## Features

- **Language Level Configuration**: Customize responses for different levels of proficiency (e.g., A1, B2).
- **Vocabulary Integration**: Provide specific terms or phrases to be used in the output.
- **Session History Management**: Retain the context across multiple interactions using unique session IDs.
- **Chunked Responses**: Control whether the response is delivered in one go or in smaller chunks.

---

## Usage

You can either use the `generator.py` module stand-alone or the `server.py` to serve functions in a Flask server.

### Functions

- generate(language, language_level, topic, history, new_words): Create or continue a podcast with or without preferred words.
- define(word, context): Get the definition of a word within a context.