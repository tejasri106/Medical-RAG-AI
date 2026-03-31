#!/usr/bin/env python3
"""
Test script for Medical AI Chat System
Run this to verify all components are working correctly
"""

import os
import sys
from dotenv import load_dotenv

def test_environment():
    """Test environment variables and dependencies"""
    print("🔍 Testing Environment...")
    
    # Load environment variables
    load_dotenv()
    
    # Check required environment variables
    pinecone_key = os.getenv("PINECONE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    print(f"✅ PINECONE_API_KEY: {'Set' if pinecone_key else 'Not Set'}")
    print(f"✅ OPENAI_API_KEY: {'Set' if openai_key else 'Not Set'}")
    
    if not pinecone_key:
        print("⚠️  Warning: PINECONE_API_KEY not set. Pinecone functionality will not work.")
    
    return bool(pinecone_key)

def test_imports():
    """Test if all required modules can be imported"""
    print("\n🔍 Testing Imports...")
    
    try:
        from src.helper import MedicalAIHelper
        print("✅ MedicalAIHelper imported successfully")
    except Exception as e:
        print(f"❌ Failed to import MedicalAIHelper: {e}")
        return False
    
    try:
        from src.store_index import MedicalIndexStore
        print("✅ MedicalIndexStore imported successfully")
    except Exception as e:
        print(f"❌ Failed to import MedicalIndexStore: {e}")
        return False
    
    try:
        from flask import Flask
        print("✅ Flask imported successfully")
    except Exception as e:
        print(f"❌ Failed to import Flask: {e}")
        return False
    
    return True

def test_data_directory():
    """Test if medical data directory exists and contains PDFs"""
    print("\n🔍 Testing Data Directory...")
    
    data_dir = "Data"
    if not os.path.exists(data_dir):
        print(f"❌ Data directory '{data_dir}' not found")
        return False
    
    pdf_files = [f for f in os.listdir(data_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"⚠️  No PDF files found in '{data_dir}' directory")
        print("   Place your medical PDF documents in the Data/ directory")
        return False
    
    print(f"✅ Found {len(pdf_files)} PDF file(s) in Data directory:")
    for pdf in pdf_files:
        print(f"   - {pdf}")
    
    return True

def test_medical_ai_components():
    """Test Medical AI components initialization"""
    print("\n🔍 Testing Medical AI Components...")
    
    try:
        from src.helper import MedicalAIHelper
        from src.store_index import MedicalIndexStore
        
        # Test MedicalIndexStore initialization
        print("   Initializing MedicalIndexStore...")
        medical_store = MedicalIndexStore()
        
        if medical_store.pinecone_client:
            print("   ✅ Pinecone client initialized")
        else:
            print("   ⚠️  Pinecone client not available")
        
        if medical_store.vector_store:
            print("   ✅ Vector store initialized")
        else:
            print("   ⚠️  Vector store not available")
        
        # Test MedicalAIHelper initialization
        print("   Initializing MedicalAIHelper...")
        medical_helper = MedicalAIHelper()
        
        if medical_helper.embeddings:
            print("   ✅ Embeddings loaded")
        else:
            print("   ⚠️  Embeddings not available")
        
        if medical_helper.llm:
            print("   ✅ Language model initialized")
        else:
            print("   ⚠️  Language model not available")
        
        # Connect components
        if medical_store.vector_store:
            medical_helper.set_vector_store(medical_store.vector_store)
            if medical_helper.qa_chain:
                print("   ✅ QA Chain created")
            else:
                print("   ⚠️  QA Chain not available")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing Medical AI components: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Medical AI Chat System - System Test")
    print("=" * 50)
    
    # Run all tests
    tests = [
        ("Environment", test_environment),
        ("Imports", test_imports),
        ("Data Directory", test_data_directory),
        ("Medical AI Components", test_medical_ai_components)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your Medical AI system is ready to run.")
        print("\nTo start the chat system:")
        print("   python app.py")
        print("\nThen open your browser to: http://localhost:5000")
    else:
        print("⚠️  Some tests failed. Please check the issues above before running the system.")
        print("\nCommon solutions:")
        print("1. Create a .env file with your API keys")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Place medical PDFs in the Data/ directory")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
