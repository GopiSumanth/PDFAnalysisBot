from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.core import SummaryIndex
from llama_index.core.tools import QueryEngineTool


def get_query_engine(file_path: str, llm=None):
    """Get router query engine."""
    system_message = """You are an Assitant. YOU MUST follow below instructions in all situations
        Instructions:
        1. your Answers should be a word-to-word match if THE QUESTION is a word-to-word match else it could be a summary.
          ex: question: What is the capital of France? Answer: Paris is the capital of France
         2. If the answer is low confidence, YOU MUST reply `Data Not Available`
        """

    llm = llm or OpenAI(model="gpt-4o-mini", temperature=0, system_prompt=system_message,seed=123)

    # load documents
    documents = SimpleDirectoryReader(input_files=[file_path]).load_data()

    splitter = SentenceSplitter(chunk_size=1024)
    nodes = splitter.get_nodes_from_documents(documents)

    summary_index = SummaryIndex(nodes)

    summary_query_engine = summary_index.as_query_engine(
        response_mode="tree_summarize", use_async=True, llm=llm
    )

    summary_tool = QueryEngineTool.from_defaults(
        query_engine=summary_query_engine,
        description=("Useful for summarization answers related to handbook"),
    )

    return summary_tool
