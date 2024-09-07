import os
from flask import Flask, request, jsonify
from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize Groq Langchain chat object and conversation
groq_api_key = os.environ.get('GROQ_API_KEY')
model = 'llama3-8b-8192'
groq_chat = ChatGroq(
    groq_api_key=groq_api_key, 
    model_name=model
)

system_prompt = 'You are a friendly conversational chatbot'
conversational_memory_length = 5

memory = ConversationBufferWindowMemory(k=conversational_memory_length, memory_key="chat_history", return_messages=True)

prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template("{human_input}"),
])

conversation = LLMChain(
    llm=groq_chat,
    prompt=prompt,
    verbose=False,
    memory=memory,
)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_question = data.get('question')
    
    if not user_question:
        return jsonify({"error": "No question provided"}), 400
    
    response = conversation.predict(human_input=user_question)
    return jsonify({"response": response})

if __name__ == "__main__":
    # app.run(debug=True)
    port = int(os.getenv("PORT", 5000))  # Use the PORT variable from the environment
    app.run(host="0.0.0.0", port=port)