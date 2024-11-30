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

## Example Usage

Below is an example of how to use the `GPT4oPipeline`:

```python
from gpt4o_pipeline import GPT4oPipeline

# Initialize the pipeline with specific parameters
pipeline = GPT4oPipeline(
    language_level="A1", 
    vocabulary=["Bonjour", "Le supermarché est un endroit pratique pour faire les courses"],
    session_id="test1"
)

# Run the pipeline with a single interaction
response = pipeline.run(
    input_message="I want a podcast about supermarkets", 
    next_chunk=False
)
print(response)

# Run the pipeline to fetch the next chunk of the response
response_chunk = pipeline.run(
    input_message="I want a podcast about supermarkets", 
    next_chunk=True
)
print(response_chunk)

# Access the stored session history
print(pipeline.store)
```

---

