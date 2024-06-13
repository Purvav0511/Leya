# Import necessary modules
from pinecone import Pinecone, ServerlessSpec
from .openai import get_embedding
import os

# Define functions

def setup_pinecone_index():
    # Set up Pinecone index
    PINECONE_API_KEY = os.environ.get('PINECONE_KEY')
    pc = Pinecone(api_key=PINECONE_API_KEY)
    EMBEDDING_DIMENSION = 1536
    index_name = 'index01'
    existing_indexes = [index['name'] for index in pc.list_indexes()]
    print(existing_indexes)
    if index_name in existing_indexes:
        print("\nIndex already exists. Using existing index ...")
        index = pc.Index(index_name)
    else:
        print("\nCreating a new index: ", index_name)
        pc.create_index(name=index_name,
                        dimension=EMBEDDING_DIMENSION,
                        metric='cosine',
                        spec=ServerlessSpec(cloud="aws", region="us-west-2"))
        index = pc.Index(index_name)

    return index

def batch_upsert(index, vectors, batch_size=50):
    # Batch upsert vectors into Pinecone index
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        index.upsert(vectors=batch)


def embed_chunks_and_upload_to_pinecone(chunks, index, repo_name):
    # Embed chunks and upload to Pinecone
    print("\nEmbedding chunks using OpenAI ...")
    embeddings_with_ids = []

    # Counter to ensure unique identifiers
    chunk_counter = 0

    for chunk in chunks:
        function_definition = chunk['function_definition']
        embedding = get_embedding(function_definition)

        # Generate a unique identifier for the chunk
        chunk_identifier = f"{chunk['source_file_name']}_{chunk_counter}"

        metadata = {
            'function_name': chunk['function_name'],
            'function_definition': function_definition,
            'source_file_name': chunk['source_file_name'],
            'source_repo': repo_name
        }

        embeddings_with_ids.append((chunk_identifier, embedding, metadata))

        # Increment the chunk counter
        chunk_counter += 1

    print("\nUploading embeddings to Pinecone in batches ...")
    batch_upsert(index, embeddings_with_ids, batch_size=50)

    print(f"\nUploaded {len(chunks)} embeddings to Pinecone index.")

def get_most_similar_chunks_for_query(query, repo_name, function_names):
    question_embedding = get_embedding(query)
    PINECONE_API_KEY = os.environ.get('PINECONE_KEY')
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index_name = 'index01'
    index = pc.Index(name=index_name)
    # Initialize the filter query with the repository name
    filter_query = {"source_repo": repo_name}

    # Conditionally add the function names to the filter if the list is provided and not empty
    if function_names:
        filter_query['function_name'] = {"$in": function_names}

    query_results = index.query(
        vector=question_embedding,
        top_k=3,
        include_metadata=True,
        filter=filter_query
    )

    function_definitions = [
        {
            'function_name': match['metadata']['function_name'],
            'function_definition': match['metadata']['function_definition'],
            'source_file_name': match['metadata']['source_file_name']
        }
        for match in query_results['matches']
        if 'function_definition' in match['metadata']
    ]

    return function_definitions
