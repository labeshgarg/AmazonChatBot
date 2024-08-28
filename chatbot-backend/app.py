from flask import Flask, request, jsonify
from flask_cors import CORS
from amazon_bot import chat_bot  
from chat_logger import log_chat

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        user_input = request.json.get('message')
        state = request.json.get('state', None)  
        
        conversation_id = "unique_id_1"
        user_id = "user_1"
       
        response = chat_bot(user_input, conversation_id=conversation_id, user_id=user_id, state=state)

        return jsonify({'message': response['message'], 'state': response['state']})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
