#!/usr/bin/env python3
"""
Medical AI Index Management Utility
Use this script to manage your Pinecone vector index
"""

import os
import sys
from dotenv import load_dotenv

def main():
    """Main management interface"""
    load_dotenv()
    
    print("🏥 Medical AI Index Management Utility")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please create a .env file with your PINECONE_API_KEY")
        return
    
    # Check if PINECONE_API_KEY is set
    pinecone_key = os.getenv("PINECONE_API_KEY")
    if not pinecone_key:
        print("❌ PINECONE_API_KEY not found in .env file!")
        return
    
    print("✅ Environment variables loaded")
    
    try:
        from src.store_index import MedicalIndexStore
        
        print("\n🔍 Initializing Medical Index Store...")
        store = MedicalIndexStore()
        
        if not store.pinecone_client:
            print("❌ Failed to connect to Pinecone")
            return
        
        print("✅ Connected to Pinecone successfully!")
        
        # Get current index status
        current_count = store.get_document_count()
        print(f"📊 Current index contains {current_count} vectors")
        
        # Show management options
        show_management_menu(store)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check your PINECONE_API_KEY is correct")
        print("2. Ensure you have internet connection")
        print("3. Check if Pinecone service is available")

def show_management_menu(store):
    """Show the management menu"""
    while True:
        print("\n" + "=" * 50)
        print("📋 Management Options:")
        print("1. Check index status")
        print("2. Clear all data (removes duplicates)")
        print("3. Refresh index (clear + reload documents)")
        print("4. Test query")
        print("5. Exit")
        print("=" * 50)
        
        choice = input("\nSelect an option (1-5): ").strip()
        
        if choice == "1":
            check_index_status(store)
        elif choice == "2":
            clear_index_data(store)
        elif choice == "3":
            refresh_index(store)
        elif choice == "4":
            test_query(store)
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1-5.")

def check_index_status(store):
    """Check detailed index status"""
    print("\n🔍 Checking index status...")
    
    try:
        count = store.get_document_count()
        print(f"📊 Total vectors: {count}")
        
        if count > 0:
            print("✅ Index has data")
        else:
            print("📭 Index is empty")
            
        # Check if vector store is connected
        if store.vector_store:
            print("✅ Vector store is connected")
        else:
            print("❌ Vector store is not connected")
            
        # Check Pinecone index details
        if store.pinecone_client:
            try:
                index = store.pinecone_client.Index(store.index_name)
                stats = index.describe_index_stats()
                print(f"🔧 Index dimension: {stats.get('dimension', 'Unknown')}")
                print(f"🔧 Index metric: {stats.get('metric', 'Unknown')}")
                print(f"🔧 Index status: {stats.get('status', 'Unknown')}")
            except Exception as e:
                print(f"⚠️  Could not get detailed index stats: {e}")
            
    except Exception as e:
        print(f"❌ Error checking status: {e}")

def clear_index_data(store):
    """Clear all data from the index"""
    print("\n⚠️  WARNING: This will delete ALL data from your index!")
    print("This action cannot be undone!")
    
    confirm = input("Type 'DELETE' to confirm: ").strip()
    
    if confirm == "DELETE":
        try:
            print("🔍 Attempting to clear index...")
            
            # Check if we can access the index
            if not store.pinecone_client:
                print("❌ Pinecone client not available")
                return False
            
            # Get the index
            index = store.pinecone_client.Index(store.index_name)
            
            # Check index status first
            try:
                stats = index.describe_index_stats()
                print(f"📊 Current index stats: {stats}")
            except Exception as e:
                print(f"⚠️  Warning: Could not get index stats: {e}")
            
            # Try to clear the index
            print("🗑️  Deleting all vectors...")
            index.delete(delete_all=True)
            
            print("✅ Index cleared successfully!")
            
            # Wait a moment for the operation to complete
            import time
            print("⏳ Waiting for operation to complete...")
            time.sleep(2)
            
            # Verify the index is empty
            try:
                new_stats = index.describe_index_stats()
                new_count = new_stats.get('total_vector_count', 0)
                print(f"✅ Verification: Index now contains {new_count} vectors")
            except Exception as e:
                print(f"⚠️  Could not verify index state: {e}")
            
            # Reconnect to empty index
            print("🔗 Reconnecting to empty index...")
            store.initialize_vector_store()
            
            return True
            
        except Exception as e:
            print(f"❌ Error clearing index: {e}")
            print(f"Error type: {type(e).__name__}")
            
            # Provide specific troubleshooting based on error type
            if "not found" in str(e).lower():
                print("💡 Tip: The index might not exist yet. Try option 3 (Refresh index) instead.")
            elif "permission" in str(e).lower():
                print("💡 Tip: Check if your Pinecone API key has delete permissions.")
            elif "timeout" in str(e).lower():
                print("💡 Tip: Network timeout. Try again in a moment.")
            else:
                print("💡 Tip: Try waiting a few minutes and try again, or use option 3 (Refresh index).")
            
            return False
    else:
        print("❌ Operation cancelled")

def refresh_index(store):
    """Refresh the index by clearing and reloading"""
    print("\n🔄 Refreshing index...")
    print("This will:")
    print("1. Clear all existing data")
    print("2. Reload documents from Data/ directory")
    print("3. Recreate the vector store")
    
    confirm = input("Continue? (y/N): ").strip().lower()
    
    if confirm in ['y', 'yes']:
        try:
            print("🔄 Starting refresh process...")
            
            # First try to clear the index
            if clear_index_data(store):
                print("✅ Index cleared successfully!")
                
                # Now reload documents
                print("📚 Reloading documents...")
                store.initialize_vector_store()
                
                # Check final status
                new_count = store.get_document_count()
                print(f"✅ Index refreshed successfully!")
                print(f"📊 New index contains {new_count} vectors")
                
            else:
                print("❌ Failed to clear index during refresh")
                
        except Exception as e:
            print(f"❌ Error refreshing index: {e}")
    else:
        print("❌ Operation cancelled")

def test_query(store):
    """Test a query on the index"""
    print("\n🧪 Testing index query...")
    
    if not store.vector_store:
        print("❌ Vector store not available")
        return
    
    test_question = input("Enter a test medical question (or press Enter for default): ").strip()
    
    if not test_question:
        test_question = "What are the symptoms of diabetes?"
    
    print(f"🔍 Testing query: '{test_question}'")
    
    try:
        result = store.query_index(test_question)
        print("\n📝 Query Result:")
        print("-" * 40)
        print(result[:500] + "..." if len(result) > 500 else result)
        print("-" * 40)
        
    except Exception as e:
        print(f"❌ Error testing query: {e}")

if __name__ == "__main__":
    main()
