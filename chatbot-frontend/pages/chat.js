import React, { useState } from 'react';
import axios from 'axios';
// import '../styles/globals.css'; 


const Chat = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    const sendMessage = async () => {
        if (input.trim() !== '') {
            const userMessage = { role: 'user', content: input };
            setMessages([...messages, userMessage]);

            try {
                const response = await axios.post('http://localhost:5000/send_message', { message: input });
                const botMessage = { role: 'bot', content: response.data.message };
                setMessages([...messages, userMessage, botMessage]);
            } catch (error) {
                console.error('Error sending message:', error);
            }

            setInput('');
        }
    };

    return (
        <div className="flex justify-center items-center min-h-screen bg-gray-100">
            <div className="bg-white rounded-xl shadow-lg w-full max-w-md p-4">
                {/* Chat Box */}
                <div className="h-80 overflow-y-auto p-4">
                    {messages.map((msg, index) => (
                        <div
                            key={index}
                            className={`mb-4 p-3 rounded-lg ${msg.role === 'user' ? 'bg-blue-500 text-white text-right ml-auto' : 'bg-gray-200 text-gray-800 text-left mr-auto'}`}
                        >
                            {msg.content}
                        </div>
                    ))}
                </div>
                {/* Input and Send Button */}
                <div className="flex items-center mt-4 border-t border-gray-300 pt-4">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                        placeholder="Type a message..."
                        className="flex-grow p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring focus:border-blue-300"
                    />
                    <button
                        onClick={sendMessage}
                        className="ml-4 bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600"
                    >
                        Send
                    </button>
                </div>
            </div>
        </div>
    );
};


export default Chat;
