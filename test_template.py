#!/usr/bin/env python3
"""
Test script to verify Flask template directory setup
"""

import os
import sys

def test_template_structure():
    """Test if the template directory structure is correct"""
    print("🔍 Testing Template Directory Structure")
    print("=" * 50)
    
    # Get current directory
    current_dir = os.getcwd()
    print(f"📁 Current working directory: {current_dir}")
    
    # Check if we're in the right place
    if not os.path.exists('app.py'):
        print("❌ app.py not found in current directory")
        print("   Please run this script from the Medical-AI project root")
        return False
    
    # Check template directory
    template_dir = os.path.join(current_dir, 'template')
    print(f"📁 Template directory: {template_dir}")
    
    if not os.path.exists(template_dir):
        print("❌ Template directory not found")
        print("   Expected: template/")
        print("   Current structure:")
        for item in os.listdir(current_dir):
            print(f"     - {item}")
        return False
    
    # Check if template directory contains index.html
    index_file = os.path.join(template_dir, 'index.html')
    print(f"📄 Index file: {index_file}")
    
    if not os.path.exists(index_file):
        print("❌ index.html not found in template directory")
        print("   Template directory contents:")
        for item in os.listdir(template_dir):
            print(f"     - {item}")
        return False
    
    print("✅ Template directory structure is correct!")
    
    # Check file size
    file_size = os.path.getsize(index_file)
    print(f"📊 index.html file size: {file_size} bytes")
    
    if file_size < 1000:
        print("⚠️  Warning: index.html seems very small, might be empty")
    
    return True

def test_flask_template_loading():
    """Test if Flask can load the template"""
    print("\n🔍 Testing Flask Template Loading")
    print("=" * 50)
    
    try:
        # Import Flask and create app
        from flask import Flask
        
        # Get the current directory where app.py is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(current_dir, 'template')
        
        print(f"📁 Flask template directory: {template_dir}")
        
        # Create Flask app with explicit template folder
        app = Flask(__name__, template_folder=template_dir)
        
        # Test template loading
        with app.app_context():
            try:
                template = app.jinja_env.get_template('index.html')
                print("✅ Flask successfully loaded index.html template")
                print(f"📄 Template source: {template.filename}")
                return True
            except Exception as e:
                print(f"❌ Flask failed to load template: {e}")
                return False
                
    except ImportError:
        print("❌ Flask not installed. Run: pip install flask")
        return False
    except Exception as e:
        print(f"❌ Error testing Flask template loading: {e}")
        return False

def main():
    """Main test function"""
    print("🏥 Medical AI - Template Directory Test")
    print("=" * 50)
    
    # Test 1: Directory structure
    structure_ok = test_template_structure()
    
    if not structure_ok:
        print("\n❌ Template directory structure test failed!")
        print("Please fix the directory structure before running the Flask app.")
        return False
    
    # Test 2: Flask template loading
    flask_ok = test_flask_template_loading()
    
    if not flask_ok:
        print("\n❌ Flask template loading test failed!")
        print("Please check Flask installation and configuration.")
        return False
    
    print("\n🎉 All tests passed!")
    print("✅ Your template directory is properly configured")
    print("✅ Flask can find and load the index.html template")
    print("\nYou can now run: python app.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
