from flask import Flask, render_template, request, jsonify
from llama_index import SimpleDirectoryReader, LLMPredictor, PromptHelper, ServiceContext
from llama_index import StorageContext, load_index_from_storage
from llama_index import VectorStoreIndex
from langchain.chat_models import ChatOpenAI

from flask_cors import CORS

app = Flask(__name__, template_folder=".")

CORS(app, origins=['http://127.0.0.1:5501'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['GET', 'POST'])
def process_query():
    if request.method == 'POST':
        question = request.json.get('question')

    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir="./storage")

    # Set up LLMPredictor with ChatOpenAI model
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=200))

    # Set up ServiceContext
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

    # load index
    index = load_index_from_storage(storage_context = storage_context, service_context = service_context)

    # Perform the query and get the response
    query_engine = index.as_query_engine()
    response = query_engine.query(question)

    return jsonify(response=response.response)

if __name__ == '__main__':
    # Set maximum input size, num_outputs, max_chunk_overlap, and chunk_size_limit here
    max_input_size = 4096
    num_outputs = 2000
    max_chunk_overlap = 0.8
    chunk_size_limit = 200

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
    
    # Load the data and construct the index
    documents = SimpleDirectoryReader('./data').load_data()

    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist()

    # app.static_folder = 'static'
    app.run(debug=True)
