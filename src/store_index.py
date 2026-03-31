from src.helper import load_pdf, text_split, download_hugging_face_embeddings
from pinecone.grpc import PineconeGRPC as Pinecone 
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os 

load_dotenv()

class MedicalIndexStore:
    def __init__(self):
        """Initialize the Medical Index Store"""
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.pinecone_client = None
        self.vector_store = None
        self.index_name = "medicalai"
        self.initialize_pinecone()
        self.initialize_vector_store()
    
    def initialize_pinecone(self):
        """Initialize Pinecone client and create index if needed"""
        try:
            if not self.api_key:
                print("Warning: PINECONE_API_KEY not found in environment variables")
                return
            
            self.pinecone_client = Pinecone(api_key=self.api_key)
            
            # Check if index exists, create if it doesn't
            try:
                self.pinecone_client.describe_index(self.index_name)
                print(f"Pinecone index '{self.index_name}' already exists")
            except:
                print(f"Creating new Pinecone index '{self.index_name}'...")
                self.pinecone_client.create_index(
                    name=self.index_name,
                    dimension=384,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1"
                    )
                )
                print(f"Pinecone index '{self.index_name}' created successfully")
                
        except Exception as e:
            print(f"Error initializing Pinecone: {e}")
    
    def check_index_has_data(self):
        """Check if the Pinecone index already has data"""
        try:
            if not self.pinecone_client:
                return False
            
            # Get index stats to see if it has vectors
            index = self.pinecone_client.Index(self.index_name)
            stats = index.describe_index_stats()
            
            # Check if there are any vectors in the index
            total_vector_count = stats.get('total_vector_count', 0)
            print(f"Current index has {total_vector_count} vectors")
            
            return total_vector_count > 0
            
        except Exception as e:
            print(f"Error checking index data: {e}")
            return False
    
    def initialize_vector_store(self):
        """Initialize the vector store with medical documents only if empty"""
        try:
            if not self.pinecone_client:
                print("Pinecone client not available, skipping vector store initialization")
                return
            
            # Check if index already has data
            if self.check_index_has_data():
                print("Index already contains data, connecting to existing vector store...")
                # Connect to existing index without adding new documents
                embeddings = download_hugging_face_embeddings()
                if embeddings:
                    self.vector_store = PineconeVectorStore.from_existing_index(
                        index_name=self.index_name,
                        embedding=embeddings
                    )
                    print("Connected to existing vector store successfully!")
                return
            
            # Only load and process documents if index is empty
            print("Index is empty, loading medical documents...")
            extracted_data = load_pdf(data='Data/')
            
            if not extracted_data:
                print("No medical documents found in Data/ directory")
                return
            
            print(f"Loaded {len(extracted_data)} documents")
            
            # Split text into chunks
            print("Splitting text into chunks...")
            text_chunks = text_split(extracted_data)
            print(f"Created {len(text_chunks)} text chunks")
            
            # Get embeddings
            embeddings = download_hugging_face_embeddings()
            if not embeddings:
                print("Failed to load embeddings")
                return
            
            # Create vector store
            print("Creating vector store with medical documents...")
            self.vector_store = PineconeVectorStore.from_documents(
                documents=text_chunks,
                index_name=self.index_name,
                embedding=embeddings
            )
            print("Vector store created successfully!")
            
        except Exception as e:
            print(f"Error initializing vector store: {e}")
    
    def query_index(self, query, k=3):
        """Query the medical knowledge base"""
        try:
            if not self.vector_store:
                return "Medical knowledge base is not available."
            
            # Perform similarity search
            results = self.vector_store.similarity_search(query, k=k)
            
            if not results:
                return "No relevant medical information found for your query."
            
            # Combine results into a single context
            context = "\n\n".join([doc.page_content for doc in results])
            return context
            
        except Exception as e:
            print(f"Error querying index: {e}")
            return f"Error retrieving medical information: {str(e)}"
    
    def get_document_count(self):
        """Get the number of documents in the index"""
        try:
            if not self.pinecone_client:
                return 0
            
            index = self.pinecone_client.Index(self.index_name)
            stats = index.describe_index_stats()
            return stats.get('total_vector_count', 0)
            
        except Exception as e:
            print(f"Error getting document count: {e}")
            return "Unknown"
    
    def clear_index(self):
        """Clear all data from the index (use with caution!)"""
        try:
            if not self.pinecone_client:
                print("Pinecone client not available")
                return False
            
            print("⚠️  WARNING: This will delete ALL data from the index!")
            confirm = input("Type 'DELETE' to confirm: ")
            
            if confirm == "DELETE":
                try:
                    # Method 1: Try direct delete
                    print("🗑️  Attempting direct delete...")
                    index = self.pinecone_client.Index(self.index_name)
                    index.delete(delete_all=True)
                    print("✅ Index cleared successfully using direct delete!")
                    return True
                    
                except Exception as e:
                    print(f"⚠️  Direct delete failed: {e}")
                    print("🔄 Trying alternative method...")
                    
                    try:
                        # Method 2: Try to delete the entire index and recreate it
                        print("🗑️  Deleting and recreating index...")
                        
                        # Delete the index
                        self.pinecone_client.delete_index(self.index_name)
                        print("✅ Old index deleted")
                        
                        # Wait a moment
                        import time
                        time.sleep(5)
                        
                        # Recreate the index
                        self.pinecone_client.create_index(
                            name=self.index_name,
                            dimension=384,
                            metric="cosine",
                            spec=ServerlessSpec(
                                cloud="aws",
                                region="us-east-1"
                            )
                        )
                        print("✅ New index created")
                        
                        # Wait for index to be ready
                        print("⏳ Waiting for index to be ready...")
                        time.sleep(10)
                        
                        # Reinitialize vector store
                        self.initialize_vector_store()
                        print("✅ Vector store reinitialized")
                        
                        return True
                        
                    except Exception as e2:
                        print(f"❌ Alternative method also failed: {e2}")
                        print("💡 You may need to manually delete the index from Pinecone console")
                        return False
                        
            else:
                print("Operation cancelled.")
                return False
                
        except Exception as e:
            print(f"Error clearing index: {e}")
            return False
    
    def refresh_index(self):
        """Refresh the index by clearing and reloading documents"""
        try:
            print("Refreshing index (this will clear existing data)...")
            if self.clear_index():
                # Reinitialize the vector store
                self.initialize_vector_store()
                return True
            return False
            
        except Exception as e:
            print(f"Error refreshing index: {e}")
            return False

# Legacy code for backward compatibility
def create_medical_index():
    """Legacy function to create medical index"""
    store = MedicalIndexStore()
    return store

# Initialize components if run directly
if __name__ == "__main__":
    print("Initializing Medical Index Store...")
    store = MedicalIndexStore()
    print("Medical Index Store initialization complete!")
    
    # Show current status
    if store.pinecone_client:
        count = store.get_document_count()
        print(f"Index currently contains {count} vectors")