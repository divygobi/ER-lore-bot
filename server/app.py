from flask import Flask, jsonify
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import os



app = Flask(__name__)
load_dotenv(dotenv_path="/Users/divygobiraj/Desktop/projects/ER_Lore_Bot/ER-lore-bot/.env")
# print(os.getenv("PINECONE_KEY"))

pc = Pinecone(api_key=os.getenv("PINECONE_KEY"))
index = pc.Index("er-text")

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

