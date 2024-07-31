from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import SummaryIndex
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector



def get_router_query_engine(file_path: str, llm = None, embed_model = None):
    """Get router query engine."""
    system_message = """You are an Assitant. YOU MUST follow below instructions in all situations
        Instructions:
        1. your Answers should be a word-to-word match if THE QUESTION is a word-to-word match else it could be a summary.
          ex: question: What is the capital of France? Answer: Paris is the capital of France
         2. If the answer is low confidence, YOU MUST reply `Data Not Available`
        """
        

    llm = llm or OpenAI(model="gpt-4o-mini",temperature=0,system_prompt=system_message)
    embed_model = embed_model or OpenAIEmbedding(model="text-embedding-ada-002")
    
    # load documents
    documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
    
    splitter = SentenceSplitter(chunk_size=1024)
    nodes = splitter.get_nodes_from_documents(documents)
    
    summary_index = SummaryIndex(nodes)
    
    summary_query_engine = summary_index.as_query_engine(
        response_mode="tree_summarize",
        use_async=True,
        llm=llm
    )
    
    summary_tool = QueryEngineTool.from_defaults(
        query_engine=summary_query_engine,
        description=(
            "Useful for summarization answers related to handbook"
        ),
    )
    
    query_engine = RouterQueryEngine(
        selector=LLMSingleSelector.from_defaults(),
        query_engine_tools=[
            summary_tool
        ],
        verbose=False
    )
    return query_engine