from llama_index import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index.llms.palm import PaLM
from llama_index import ServiceContext
from llama_index import StorageContext
import os


class RAGPaLMQuery:
    def __init__(self, session_state):
        self.session_state = session_state
        # Create a folder for data if it doesn't exist
        if not os.path.exists("data"):
            os.makedirs("data")

        # Load documents from the data folder
        self.documents = SimpleDirectoryReader("./data").load_data()

        # Set up API key for PaLM
        os.environ['GOOGLE_API_KEY'] = 'AIzaSyAyV606wdn10w78WeuJOsXSpPZg9xC_fW0'

        # Initialize PaLM and Hugging Face embedding model
        self.llm = PaLM()
        self.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")

        # Set up service context
        self.service_context = ServiceContext.from_defaults(llm=self.llm, embed_model=self.embed_model, chunk_size=800, chunk_overlap=20)

        # Create a VectorStoreIndex from the documents
        self.index = VectorStoreIndex.from_documents(self.documents, service_context=self.service_context)

        # Persist the index to storage
        self.index.storage_context.persist()

        # Create a query engine
        self.query_engine = self.index.as_query_engine()

    def query_response(self, query):


        response = self.query_engine.query(query)
        return response
        
    # def query_response(self, query):
    #         # Perform a query
    #         trained_topics = ["photosynthesis", "dna" ]

    #         if query in trained_topics:
    #             response = self.query_engine.query(query)
    #             return response
    #         else:
    #             return "I'm sorry, I don't have information on that topic. Can I help with something else?"

