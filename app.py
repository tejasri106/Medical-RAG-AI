from flask import Flask, render_template, request, jsonify
import os
from src.helper import MedicalAIHelper
from src.store_index import MedicalIndexStore
import json

# Get the current directory where app.py is located
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, 'template')

# Create Flask app with explicit template folder
app = Flask(__name__, template_folder=template_dir)

# Initialize the medical AI components
try:
    # Initialize the medical index store
    medical_store = MedicalIndexStore()
    
    # Initialize the medical AI helper
    medical_helper = MedicalAIHelper()
    
    # Connect the helper with the vector store
    if medical_store.vector_store:
        medical_helper.set_vector_store(medical_store.vector_store)
        print("Medical AI system connected successfully!")
    else:
        print("Warning: Vector store not available, Medical AI responses may be limited")
    
except Exception as e:
    print(f"Error initializing Medical AI system: {e}")
    medical_store = None
    medical_helper = None

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests and provide medical AI responses"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        chat_id = data.get('chat_id', '')
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Debug: Log the current state
        print(f"🔍 Chat request received: '{user_message}'")
        print(f"🔍 Medical helper available: {medical_helper is not None}")
        print(f"🔍 Vector store available: {medical_store is not None and medical_store.vector_store is not None}")
        print(f"🔍 QA chain available: {medical_helper.qa_chain is not None if medical_helper else False}")
        
        if not medical_helper:
            print("❌ Medical helper not available")
            return jsonify({
                'response': 'I apologize, but the Medical AI system is currently unavailable. Please try again later or contact support.'
            }), 500
        
        # Process the medical query using the existing system
        try:
            # Get relevant medical information from the stored index
            relevant_info = ""
            if medical_store and medical_store.vector_store:
                print("🔍 Querying medical knowledge base...")
                relevant_info = medical_store.query_index(user_message)
                print(f"🔍 Retrieved {len(relevant_info)} characters of relevant info")
            else:
                print("⚠️  Vector store not available for querying")
            
            # Generate response using the medical AI helper
            print("🔍 Generating AI response...")
            ai_response = medical_helper.generate_response(user_message, relevant_info)
            print(f"🔍 AI response generated: {len(ai_response)} characters")
            
            # Check if we got a fallback response
            if "recommend consulting with a healthcare professional" in ai_response:
                print("⚠️  AI system returned fallback response - this indicates an issue")
                print("🔍 Debug info:")
                print(f"   - Medical helper: {medical_helper is not None}")
                print(f"   - Vector store: {medical_store.vector_store is not None if medical_store else False}")
                print(f"   - QA chain: {medical_helper.qa_chain is not None}")
                print(f"   - Relevant info length: {len(relevant_info)}")
            
            # Format the response for better readability
            formatted_response = format_medical_response(ai_response)
            
            return jsonify({
                'response': formatted_response,
                'chat_id': chat_id,
                'relevant_info': relevant_info[:200] + "..." if len(relevant_info) > 200 else relevant_info,
                'debug_info': {
                    'medical_helper_available': medical_helper is not None,
                    'vector_store_available': medical_store.vector_store is not None if medical_store else False,
                    'qa_chain_available': medical_helper.qa_chain is not None if medical_helper else False,
                    'relevant_info_length': len(relevant_info)
                }
            })
            
        except Exception as e:
            print(f"❌ Error processing medical query: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'response': 'I encountered an issue while processing your medical question. Please try rephrasing your question or contact support if the problem persists.'
            }), 500
            
    except Exception as e:
        print(f"❌ Error in chat endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'response': 'I apologize, but I encountered an unexpected error. Please try again.'
        }), 500

def format_medical_response(response):
    """Format the AI response for better readability"""
    if not response:
        return "I'm sorry, I couldn't generate a response for your question. Please try rephrasing or ask a different question."
    
    # Clean up the response
    formatted = response.strip()
    
    # Add medical disclaimer if not present
    if "disclaimer" not in formatted.lower() and "consult" not in formatted.lower():
        formatted += "\n\n⚠️ **Important Disclaimer**: This information is for educational purposes only and should not replace professional medical advice. Always consult with a qualified healthcare provider for proper diagnosis and treatment."
    
    return formatted

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'medical_ai_available': medical_helper is not None,
        'vector_store_available': medical_store is not None and medical_store.vector_store is not None,
        'pinecone_available': medical_store is not None and medical_store.pinecone_client is not None
    })

@app.route('/status')
def status():
    """Detailed status endpoint"""
    status_info = {
        'medical_ai_helper': 'Available' if medical_helper else 'Not Available',
        'medical_index_store': 'Available' if medical_store else 'Not Available',
        'pinecone_client': 'Available' if medical_store and medical_store.pinecone_client else 'Not Available',
        'vector_store': 'Available' if medical_store and medical_store.vector_store else 'Not Available',
        'qa_chain': 'Available' if medical_helper and medical_helper.qa_chain else 'Not Available'
    }
    
    return jsonify(status_info)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.getenv('FLASK_PORT', 5001))
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    
    # Print template directory for debugging
    print(f"📁 Template directory: {template_dir}")
    print(f"📁 Current working directory: {os.getcwd()}")
    
    # Check if the medical AI system is available
    if medical_helper and medical_store:
        print("🚀 Starting Medical AI Chat Server...")
        print("✅ Medical AI system is ready")
        if medical_store.vector_store:
            print("✅ Vector store is connected")
        else:
            print("⚠️  Vector store is not available")
        print(f"🌐 Server will be available at: http://localhost:{port}")
    else:
        print("⚠️  Warning: Medical AI system is not fully initialized")
        print("🌐 Server will start but may not function properly")
    
    # Run the Flask app
    app.run(debug=True, host=host, port=port)
