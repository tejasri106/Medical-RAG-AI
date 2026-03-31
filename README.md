# Medical AI Chat System

A modern, ChatGPT-like interface for medical AI consultations powered by your medical knowledge base.

## 🚀 Features

- **Modern Chat Interface**: Clean, responsive design similar to ChatGPT
- **Medical AI Assistant**: AI-powered responses based on your medical documents
- **Chat History**: Save and manage multiple consultations
- **Real-time Chat**: Instant responses with typing indicators
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Medical Knowledge Base**: Leverages your PDF medical documents for accurate responses

## 🏥 What It Does

This system allows users to:
- Ask medical questions in natural language
- Receive AI-generated responses based on medical literature
- Maintain chat history for ongoing consultations
- Get educational medical information (with appropriate disclaimers)

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Flask (Python)
- **AI/ML**: LangChain, OpenAI GPT, HuggingFace Transformers
- **Vector Database**: Pinecone
- **Document Processing**: PyPDF, LangChain Document Loaders

## 📁 Project Structure

```
Medical-AI/
├── app.py                 # Flask backend server
├── template/
│   └── index.html        # Frontend chat interface
├── src/
│   ├── helper.py         # Medical AI helper functions
│   ├── store_index.py    # Vector database management
│   └── prompt.py         # AI prompt templates
├── Data/                 # Medical PDF documents
├── requirements.txt      # Python dependencies
├── test_system.py       # System testing script
├── SETUP.md             # Detailed setup guide
└── README.md            # This file
```

## 🚀 Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   Create a `.env` file with your API keys:
   ```bash
   PINECONE_API_KEY=your_pinecone_api_key
   OPENAI_API_KEY=your_openai_api_key  # Optional
   ```

3. **Test the system**
   ```bash
   python test_system.py
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to: `http://localhost:5000`

## 📚 Setup Guide

For detailed setup instructions, API key configuration, and troubleshooting, see [SETUP.md](SETUP.md).

## 🔑 Required API Keys

- **Pinecone API Key**: Required for vector database functionality
- **OpenAI API Key**: Optional, but recommended for better AI responses

## 🧪 Testing

Run the test script to verify all components are working:
```bash
python test_system.py
```

## 🌐 API Endpoints

- `GET /` - Main chat interface
- `POST /chat` - Chat endpoint for AI responses
- `GET /health` - System health check
- `GET /status` - Detailed component status

## ⚠️ Important Disclaimers

- **Educational Purpose Only**: This system provides information for educational purposes only
- **Not Medical Advice**: Should not replace professional medical advice
- **Consult Healthcare Providers**: Always consult qualified healthcare providers for diagnosis and treatment
- **AI Limitations**: AI responses may not always be accurate or complete

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter issues:
1. Check the [SETUP.md](SETUP.md) troubleshooting section
2. Run `python test_system.py` to diagnose problems
3. Check console output for error messages
4. Verify your API keys and configuration

## 🔮 Future Enhancements

- User authentication and chat history persistence
- File upload for additional medical documents
- Export chat transcripts
- Integration with medical databases
- Multi-language support
- Voice input/output capabilities

---

**Built with ❤️ for the medical community**

*Remember: This tool is designed to assist and educate, not to replace professional medical care.*
