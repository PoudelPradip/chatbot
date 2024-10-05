import faiss  # Use FAISS for vector similarity search (or any other vector DB)
import numpy as np
import json
import os

# Assuming you store your embeddings in a FAISS index
index = faiss.IndexFlatL2(768)  # Assuming the OpenAI embeddings have 768 dimensions

# Load stored embeddings (for example, from a file or database)
def load_embeddings():
    with open('embeddings.json', 'r') as f:
        return json.load(f)

embeddings_data = load_embeddings()

# Insert embeddings into the FAISS index
for i, data in enumerate(embeddings_data):
    embedding = np.array(data['embedding']).astype('float32')
    index.add(np.expand_dims(embedding, axis=0))

# Function to search for the closest embeddings to the user query
def search_embeddings(query):
    query_embedding = get_embedding(query)  # Generate embedding for the user's query
    query_embedding = np.array(query_embedding).astype('float32')
    distances, indices = index.search(np.expand_dims(query_embedding, axis=0), k=5)  # Find top 5 closest embeddings
    
    # Retrieve the corresponding chunks based on indices
    results = [embeddings_data[i]['chunk'] for i in indices[0]]
    return results

# New endpoint to query the chatbot
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query')

    if not query:
        return jsonify({'error': 'No query provided.'}), 400
    
    # Perform semantic search
    relevant_chunks = search_embeddings(query)

    # Use OpenAI's GPT to generate a response based on the relevant chunks
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query},
            {"role": "assistant", "content": "\n".join(relevant_chunks)}
        ]
    )

    return jsonify({"response": response['choices'][0]['message']['content']})


def load_embeddings():
    if not os.path.exists('embeddings.json'):
        # Create an empty embeddings.json file if it does not exist
        with open('embeddings.json', 'w') as f:
            json.dump({}, f)  # Create an empty JSON object
            print("Created an empty 'embeddings.json' file.")
    
    with open('embeddings.json', 'r') as f:
        return json.load(f)