import os

def set_environment_variables():
    """Set environment variables for Pinecone and OpenAI keys if not already set."""
    pinecone_key = os.getenv('PINECONE_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')

    if not pinecone_key:
        pinecone_key = input("Enter your Pinecone API key: ")
        os.environ['PINECONE_KEY'] = pinecone_key

    if not openai_key:
        openai_key = input("Enter your OpenAI API key: ")
        os.environ['OPENAI_API_KEY'] = openai_key