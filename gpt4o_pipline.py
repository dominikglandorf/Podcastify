from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
import os
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from config import Config
import uuid
import re

_ = load_dotenv(find_dotenv()) # read local .env file
api_key = os.environ['OPENAI_API_KEY']



class GPT4oPipeline():
    def __init__(self, language_level:str, vocabulary:list[str],session_id: str =str(uuid.uuid4())):
        self.language_level = language_level
        self.vocabulary = vocabulary
        self.session_id = session_id
        self.store = {}
        self.pattern = r"Chunk \d+:(.*?)eoc"



    def extract_chunks(self, text:str):
        match = re.search(self.pattern, text, re.DOTALL)
        if match:
            chunk = match.group(1)
            return chunk
    
    def get_session_history(self) -> BaseChatMessageHistory:
        if self.session_id not in self.store:
            self.store[self.session_id] = ChatMessageHistory()
        return self.store[self.session_id]
    


    def run(self,input_message:str, next_chunck:bool = False):
        model = ChatOpenAI(model = Config.LLM.model,temperature=Config.LLM.temperature,streaming=Config.LLM.streaming)
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    Config.prompt.text,
                ),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
            ]
        )
        runnable = prompt_template | model


        with_message_history = RunnableWithMessageHistory(
            runnable,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )
        if not next_chunck:
            output = with_message_history.invoke(
            {"vocabulary":self.vocabulary,"language_level":self.language_level, "input": input_message},
            config={"configurable": {"session_id": self.session_id}},
            ).content
            return self.extract_chunks(output)
            
        else:
            output = with_message_history.invoke(
            {"vocabulary":self.vocabulary,"language_level":self.language_level, "input": "Next Chunk"},
            config={"configurable": {"session_id": "abc123"}},
            ).content
            return self.extract_chunks(output)