from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from src.prompt import system_prompt
import os
from dotenv import load_dotenv

load_dotenv()

class MedicalAIHelper:
    def __init__(self):
        """Initialize the Medical AI Helper with necessary components"""
        self.embeddings = None
        self.llm = None
        self.qa_chain = None
        self.vector_store = None
        self.initialize_components()
    
    def initialize_components(self):
        """Initialize the AI components"""
        try:
            # Initialize embeddings
            self.embeddings = download_hugging_face_embeddings()
            
            # Try to initialize language model (priority order)
            self.llm = self._initialize_llm()
            
            if self.llm:
                print("✅ Language model initialized successfully!")
            else:
                print("⚠️  No language model available - responses will be limited")
            
            print("Medical AI Helper components initialized successfully!")
            
        except Exception as e:
            print(f"Error initializing Medical AI Helper components: {e}")
    
    def _initialize_llm(self):
        """Initialize language model with fallback options"""
        # Option 1: Try OpenAI (if API key is available)
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if openai_api_key:
            try:
                print("🔑 Trying OpenAI...")
                llm = ChatOpenAI(
                    model_name="gpt-3.5-turbo",
                    temperature=0.1,
                    openai_api_key=openai_api_key
                )
                # Test the connection
                llm.invoke("test")
                print("✅ OpenAI initialized successfully!")
                return llm
            except Exception as e:
                print(f"⚠️  OpenAI failed: {e}")
        
        # Option 2: Try Ollama (local, free)
        try:
            print("🦙 Trying Ollama...")
            llm = Ollama(
                model="llama2:7b",  # or "mistral:7b"
                temperature=0.1,
                base_url="http://localhost:11434"
            )
            # Test the connection
            llm.invoke("test")
            print("✅ Ollama initialized successfully!")
            return llm
        except Exception as e:
            print(f"⚠️  Ollama failed: {e}")
            print("💡 Make sure Ollama is running: ollama serve")
        
        # Option 3: Try HuggingFace (free tier)
        try:
            print("🤗 Trying HuggingFace...")
            from langchain_community.llms import HuggingFaceHub
            hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
            if hf_token:
                llm = HuggingFaceHub(
                    repo_id="google/flan-t5-base",
                    huggingfacehub_api_token=hf_token,
                    model_kwargs={"temperature": 0.1, "max_new_tokens": 256}
                )
                print("✅ HuggingFace initialized successfully!")
                return llm
            else:
                print("⚠️  No HuggingFace API token found")
        except Exception as e:
            print(f"⚠️  HuggingFace failed: {e}")
        
        # Option 4: No LLM available
        print("❌ No language model could be initialized")
        print("💡 Solutions:")
        print("   1. Install Ollama: curl -fsSL https://ollama.ai/install.sh | sh")
        print("   2. Get OpenAI API key: https://platform.openai.com/")
        print("   3. Get HuggingFace token: https://huggingface.co/settings/tokens")
        return None
    
    def set_vector_store(self, vector_store):
        """Set the vector store for retrieval"""
        self.vector_store = vector_store
        if self.vector_store and self.llm:
            self._create_qa_chain()
    
    def _create_qa_chain(self):
        """Create the QA chain for answering questions"""
        try:
            if not self.vector_store or not self.llm:
                print("⚠️  Cannot create QA chain: missing vector store or LLM")
                return
            
            # Create prompt template
            prompt_template = PromptTemplate(
                template=system_prompt,
                input_variables=["context"]
            )
            
            # Create QA chain
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
                chain_type_kwargs={"prompt": prompt_template}
            )
            
            print("✅ QA Chain created successfully!")
            
        except Exception as e:
            print(f"Error creating QA chain: {e}")
    
    def generate_response(self, user_question, context_info=""):
        """Generate a response to a user's medical question"""
        try:
            print(f"🔍 MedicalAIHelper.generate_response called")
            print(f"🔍 User question: '{user_question}'")
            print(f"🔍 Context info length: {len(context_info) if context_info else 0}")
            print(f"🔍 QA chain available: {self.qa_chain is not None}")
            print(f"🔍 Vector store available: {self.vector_store is not None}")
            print(f"🔍 LLM available: {self.llm is not None}")
            
            if not self.qa_chain:
                print("⚠️  QA chain not available, using fallback response")
                return self._generate_fallback_response(user_question, context_info)
            
            if not context_info or context_info == "Medical knowledge base is not available.":
                print("⚠️  No context info available, using fallback response")
                return self._generate_fallback_response(user_question, context_info)
            
            print("🔍 Using QA chain to generate response...")
            # Use the QA chain to generate response
            response = self.qa_chain.invoke({"query": user_question})
            result = response.get("result", "I couldn't generate a response for your question.")
            
            print(f"🔍 QA chain response: {len(result)} characters")
            return result
            
        except Exception as e:
            print(f"❌ Error in generate_response: {e}")
            import traceback
            traceback.print_exc()
            return self._generate_fallback_response(user_question, context_info)
    
    def _generate_fallback_response(self, user_question, context_info=""):
        """Generate a fallback response when the main system is unavailable"""
        if context_info:
            return f"Based on the available medical information, I can provide some guidance about your question: '{user_question}'. However, I recommend consulting with a healthcare provider for accurate diagnosis and treatment."
        else:
            return f"I understand you're asking about: '{user_question}'. While I'm designed to help with medical questions, I'm currently experiencing technical difficulties. Please consult with a healthcare provider for accurate medical advice."

def load_pdf(data):
    """Load PDF documents from the specified directory"""
    try:
        loader = DirectoryLoader(data, glob="*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()
        return documents
    except Exception as e:
        print(f"Error loading PDFs: {e}")
        return []

def text_split(extracted_data):
    """Split text documents into chunks"""
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
        text_chunks = text_splitter.split_documents(extracted_data)
        return text_chunks
    except Exception as e:
        print(f"Error splitting text: {e}")
        return []

def download_hugging_face_embeddings():
    """Download and return HuggingFace embeddings"""
    try:
        embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        return embeddings
    except Exception as e:
        print(f"Error downloading embeddings: {e}")
        return None
