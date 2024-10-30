from flask import Flask, jsonify
from flask import request
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import google.generativeai as genai
from pymongo import MongoClient

import os



app = Flask(__name__)
load_dotenv(dotenv_path="/Users/divygobiraj/Desktop/projects/ER_Lore_Bot/ER-lore-bot/.env")
# print(os.getenv("PINECONE_KEY"))

pc = Pinecone(api_key=os.getenv("PINECONE_KEY"))
index = pc.Index("er-text")
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")
mongoClient = MongoClient(connect=False)
uri = os.getenv('MONGO_URI')
client = MongoClient(uri,
                             tls=True,
                             tlsAllowInvalidCertificates=True)


database = client.get_database("EldenRing")
textDB = database.get_collection("er-text")







def generate_text(prompt):
    query = "Who broke the Elden ring?"
    print("YOUR prompt is: " + prompt)

    embedding = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[prompt],
        parameters={
            "input_type": "query"
        }
    )
    if len(embedding) == 0:
        return jsonify(message="No embeddings found"), 404
    
    results = index.query(
        vector=embedding[0].values,
        top_k=3,
        include_values=False,
        include_metadata=True
    )
    
    documents = []
    foundDocs = set()
    for result in results['matches']:
        docName = result["id"]
        docName = ''.join(e for e in docName if not e.isdigit())
        #Documents are chunked so we need to search with wildcard
        docs = textDB.find({"name": {"$regex": docName }})
        fullDoc = ""
        for doc in docs:
            fullDoc += doc['text']
            fullDoc += " "

        if docName not in foundDocs and fullDoc != "":
            foundDocs.add(docName)
            documents.append({
                "name": docName,
                "text": fullDoc
            })


    print("Documents: \n", documents)
    return documents


### real endpoints
@app.route("/generate", methods=["POST"])
def generate():
    try:
        prompt = request.form['prompt']
        docs = generate_text(prompt)
        return jsonify(docs), 200
    except Exception as e:
        return jsonify(message="Error with retrieving text from", error=str(e)), 500



### test endpoints
@app.route("/test/pingdb")
def test_db():
    textDB.find_one({"test": "test"})
    return jsonify(message="Inserted!"), 200


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


@app.route("/test/retrieve")
def test_generate():
    docs = generate_text("Who broke the Elden ring?")

    try:
        return jsonify(docs), 200
    except Exception as e:
        return jsonify(message="Error with retrieving text from", error=str(e)), 500

@app.route("/test/geneneratext")
def test_generate_text():
    query = "Who broke the Elden ring?"
    print("YOUR prompt is: " + query)
    try:
        response = model.generate_content(query)
        
        return jsonify(response), 200
    except Exception as e:
        return jsonify(message="Error with generating text from gemini", error=str(e)), 500



