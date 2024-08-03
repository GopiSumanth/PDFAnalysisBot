import os
import PyPDF2
from openai import OpenAI

class PDFReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        with open(self.file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
        return text

class Agent:
    def __init__(self, document_text, api_key, model="gpt-4o-mini"):
        self.document_text = document_text
        self.api_key = api_key
        self.model = model

    def query(self, question):
        client = OpenAI(
            # This is the default and can be omitted
            api_key=self.api_key,
        )
        system_message = """You are an Assistant. YOU MUST follow the instructions below:
            1. Your answers should be a word-to-word match if the question is a word-to-word match; otherwise, it could be a single text paragraph.
            2. If the answer is low confidence or context is not available in the system content, YOU MUST reply `Data Not Available`.
            """
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.document_text},
                {"role": "assistant", "content": system_message},
                {"role": "user", "content": question}
            ],
            temperature=0,
            seed=1234,
        )
        return response.choices[0].message.content.strip()

def get_agent(file_path: str, model="gpt-4o-mini"):
    # Fetch the OpenAI API key from the environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

    # Read the PDF document
    pdf_reader = PDFReader(file_path)
    document_text = pdf_reader.read()

    # Initialize the agent with the document text and OpenAI API key
    agent = Agent(document_text, api_key, model)
    return agent
