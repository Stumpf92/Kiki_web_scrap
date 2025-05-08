from database import Database_qdrant, Database_postgres
from qdrant_client import models
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import ollama
from transformers import AutoTokenizer


db_qdrant = Database_qdrant("localhost", 6333)
db_qdrant.connect()

EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'
model = SentenceTransformer(EMBEDDING_MODEL_NAME)

user_prompt = "give me a biographic summary of the artist 'p.diddy'"
# user_prompt = "what can you tell me about ndas in the international music industry ?"

prompt_embedding = model.encode(user_prompt, show_progress_bar=False, device='cpu')

#print(prompt_embedding)

search_result = db_qdrant.client.search(
    collection_name="newspaper",
    query_vector=prompt_embedding,
    limit=30,
    with_payload=True,
    with_vectors=True,
)

retrieved_contexts_with_id_url = []
for i in search_result:
    retrieved_contexts_with_id_url.append({
        "id": i.payload['id'],
        "title": i.payload['title'],
        "text": i.payload['text'],
        "url": i.payload['url']  
    })

final_prompt_for_llm = f"""
You are an assistant specializing in the music industry.
Answer the following question *strictly* based on the provided newspaper articles. For *every single piece of information* you present in your answer, you *must* include the corresponding article's ID and its URL immediately following the information, enclosed in parentheses. The format should be: (ID: [article ID], URL: [article URL]).

If the provided articles do not contain the answer, you *must* state that the information is not available in the provided articles.

--- CONTEXT START ---
"""
for context in retrieved_contexts_with_id_url:
    context_info = f"ID: {context['id']}\nTitle: {context['title']}\nText:\n{context['text']}\nURL: {context['url']}\n\n---\n\n"
    final_prompt_for_llm += context_info

final_prompt_for_llm += f"""
--- CONTEXT END ---

Question: {user_prompt}

Answer:
"""
#tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3-8B")
#tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")
tokenizer = AutoTokenizer.from_pretrained("gpt2")



print(final_prompt_for_llm)
print("Länge des Prompt in Token: ",len(tokenizer.encode(final_prompt_for_llm)))

response = ollama.chat(
    model="llama3.1",
    messages=[
        {"role": "user", "content": final_prompt_for_llm}
    ]
)
print(response['message']['content'])

# print("FOLLOWING SOURCES WERE USED:")
# for i in search_result:
#     print(i.payload['id'])
#     print(i.payload['title'])
#     print(i.payload['text'])
#     print(i.payload['url'])