import os
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.core import SummaryIndex
from llama_index.core.tools import QueryEngineTool
from llama_index.core.agent import FunctionCallingAgentWorker, AgentRunner

def get_agent(file_path: str, llm=None):
    """
    Initializes the AI agent with the specified LLM and loads the document.

    Args:
        file_path (str): Path to the handbook PDF.
        llm: Language model instance (default: OpenAI).

    Returns:
        AgentRunner: Configured agent instance.
    """
    system_message = """You are an Assistant. YOU MUST follow the instructions below:
    1. Your answers should be a word-to-word match if the question is a word-to-word match; otherwise, it could be a summary.
    2. If the answer is low confidence or context is not available in the handbook, YOU MUST reply `Data Not Available`.
    """
    
    # Initialize the language model
    llm = llm or OpenAI(model="gpt-4o-mini", temperature=0, system_prompt=system_message)

    # Load documents
    documents = SimpleDirectoryReader(input_files=[file_path]).load_data()

    # Split documents into nodes
    splitter = SentenceSplitter(chunk_size=1024)
    nodes = splitter.get_nodes_from_documents(documents)

    # Create a summary index
    summary_index = SummaryIndex(nodes)

    # Initialize the query engine
    summary_query_engine = summary_index.as_query_engine(
        response_mode="tree_summarize", use_async=True, llm=llm
    )

    # Create a query engine tool
    summary_tool = QueryEngineTool.from_defaults(
        query_engine=summary_query_engine,
        description="Useful for summarization answers related to handbook",
    )

    # Initialize the agent
    agent_worker = FunctionCallingAgentWorker.from_tools(
        [summary_tool], llm=llm, verbose=False, system_prompt=system_message
    )
    agent = AgentRunner(agent_worker)
    return agent
