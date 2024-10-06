from flask import Flask, jsonify
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import google.generativeai as genai
import os



app = Flask(__name__)
load_dotenv(dotenv_path="/Users/divygobiraj/Desktop/projects/ER_Lore_Bot/ER-lore-bot/.env")
# print(os.getenv("PINECONE_KEY"))

pc = Pinecone(api_key=os.getenv("PINECONE_KEY"))
index = pc.Index("er-text")
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")


@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/test/upsert")
def test_pinecone():
    index.upsert(
    vectors=[
        {
            "id": "vec1", 
            "values": [0.1] * 3072, 
            "metadata": {"genre": "drama"}
        }
    ],
    namespace= "tst1")
    return jsonify(message="Upserted!"), 200


def generate_text(prompt):
    query = "Who broke the Elden ring?"

    embedding = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[prompt],
        parameters={
            "input_type": "query"
        }
    )
    
    results = index.query(
        vector=embedding[0].values,
        top_k=3,
        include_values=False,
        include_metadata=True
    )

    return results

@app.route("/test/generate")
def test_generate():
    result = generate_text("Who broke the Elden ring?")
    return jsonify(result)
