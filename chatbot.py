import os
from pathlib import Path

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS

from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.runnables import RunnablePassthrough


# Load environment variables

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Paths

DATA_FOLDER = Path("data")

VECTOR_FOLDER = "vector_db"


# -----------------------------
# Load all PDF documents
# -----------------------------

def load_documents():

    documents = []

    for file in DATA_FOLDER.glob("*.pdf"):

        loader = PyPDFLoader(str(file))

        docs = loader.load()

        for doc in docs:
            doc.metadata["source"] = file.name

        documents.extend(docs)


    return documents



# -----------------------------
# Create vector database
# -----------------------------

def create_vector_database():

    documents = load_documents()


    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,

        chunk_overlap=200

    )


    chunks = splitter.split_documents(documents)


    embeddings = HuggingFaceEmbeddings(

        model_name="sentence-transformers/all-MiniLM-L6-v2"

    )


    db = FAISS.from_documents(

        chunks,

        embeddings

    )


    db.save_local(VECTOR_FOLDER)


    return db



# -----------------------------
# Load Vector Database
# -----------------------------

def get_database():

    embeddings = HuggingFaceEmbeddings(

        model_name="sentence-transformers/all-MiniLM-L6-v2"

    )


    if not os.path.exists(
        f"{VECTOR_FOLDER}/index.faiss"
    ):

        return create_vector_database()


    return FAISS.load_local(

        VECTOR_FOLDER,

        embeddings,

        allow_dangerous_deserialization=True

    )



# Initialize database

db = get_database()



# -----------------------------
# Groq AI Model
# -----------------------------

llm = ChatGroq(

    model="llama-3.3-70b-versatile",

    temperature=0,

    groq_api_key=GROQ_API_KEY

)



# -----------------------------
# Prompt
# -----------------------------

prompt = ChatGPT_prompt = ChatPromptTemplate.from_template(

"""
You are the official AI assistant for NextGen Rise Academy.

Answer questions using ONLY the provided context.

If the answer is not available in the documents, say:

"I do not have enough information from NextGen Rise Academy documents to answer that."

Be helpful, professional, and concise.


Context:

{context}


Question:

{question}

"""

)



# -----------------------------
# Retrieval Chain
# -----------------------------

retriever = db.as_retriever(

    search_kwargs={"k":4}

)



def format_documents(docs):

    return "\n\n".join(

        [
            f"Source: {doc.metadata.get('source')}\n{doc.page_content}"
            for doc in docs
        ]

    )



chain = (

    {

        "context": retriever | format_documents,

        "question": RunnablePassthrough()

    }

    |

    prompt

    |

    llm

)



# -----------------------------
# Function used by app.py
# -----------------------------

def ask(question):

    response = chain.invoke(question)

    return response.content