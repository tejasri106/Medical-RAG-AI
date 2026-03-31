# Medical AI Chat System Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip or conda package manager
- Medical PDF documents in the `Data/` directory

## Installation

1. **Clone or download the project**
   ```bash
   cd Medical-AI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root with the following variables:
   ```bash
   # Pinecone API Key (Required for vector database)
   PINECONE_API_KEY=your_pinecone_api_key_here
   
   # OpenAI API Key (Optional - for better AI responses)
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Flask Configuration
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

## Getting API Keys

### Pinecone API Key
1. Go to [Pinecone Console](https://app.pinecone.io/)
2. Sign up or log in
3. Create a new project
4. Get your API key from the project dashboard

### OpenAI API Key (Optional)
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key

## Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open your browser**
   Navigate to: `http://localhost:5000`

3. **Start chatting!**
   - Click "New Consultation" to start a new chat
   - Ask medical questions
   - Receive AI-powered responses based on your medical documents

## Features

- **ChatGPT-like Interface**: Modern, responsive chat interface
- **Medical Knowledge Base**: AI responses based on your medical PDF documents
- **Chat History**: Save and manage multiple consultations
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Chat**: Instant responses with typing indicators

## Troubleshooting

### Common Issues

1. **"Medical AI system is not fully initialized"**
   - Check that your `.env` file has the correct API keys
   - Ensure you have medical PDFs in the `Data/` directory
   - Check the console for specific error messages

2. **"Pinecone index creation failed"**
   - Verify your Pinecone API key is correct
   - Check your internet connection
   - Ensure you have sufficient Pinecone credits

3. **"No medical documents found"**
   - Place your medical PDF files in the `Data/` directory
   - Ensure the files are readable PDFs

### Health Check

Visit `http://localhost:5000/health` to check system status:
- Medical AI availability
- Vector store status
- Pinecone connection status

Visit `http://localhost:5000/status` for detailed component status.

## File Structure

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
└── .env                 # Environment variables (create this)
```

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and private
- The system includes medical disclaimers for user safety
- All responses are for educational purposes only

## Support

If you encounter issues:
1. Check the console output for error messages
2. Verify your API keys and configuration
3. Ensure all dependencies are properly installed
4. Check that your medical documents are accessible

## Medical Disclaimer

⚠️ **Important**: This system provides information for educational purposes only and should not replace professional medical advice. Always consult with qualified healthcare providers for proper diagnosis and treatment.
