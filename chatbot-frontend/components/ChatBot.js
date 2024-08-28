import { useState } from 'react';
export default function ChatBot() {
    const [message, setMessage] = useState('');
    const [chatHistory, setChatHistory] = useState([]);
    const [state, setState] = useState(null); 

    const handleSendMessage = async () => {
        try {
            const res = await fetch('http://127.0.0.1:5000/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message, state }), 
            });

            const data = await res.json();
            setChatHistory([...chatHistory, { sender: 'user', text: message }, { sender: 'bot', text: data.message }]);
            setState(data.state);

            // Clear the message input field
            setMessage('');
        } catch (error) {
            console.error('Error:', error);
        }
    };
    return (
        <div className="flex justify-center items-center min-h-screen bg-gradient-to-br from-purple-300 to-blue-400">
        <div className="bg-white rounded-xl shadow-lg w-full max-w-md p-4 animate-float">
            {/* Header with floating animation */}
            <div className="bg-gradient-to-r from-orange-400 to-red-400 text-white rounded-t-xl p-4 flex items-center justify-between">
                <div>
                    <h2 className="font-bold text-xl">Welcome to Amazon Assistant</h2>
                    <p className="text-sm italic animate-bounce">We reply immediately</p>
                </div>
                <span className="text-3xl">👋</span>
            </div>
        
                    {/* Chat Window */}
                    <div className="p-4 overflow-y-auto h-80">
                        {chatHistory.map((msg, index) => (
                            <div 
                                key={index} 
                                className={`mb-4 p-3 rounded-lg ${msg.sender === 'user' ? 'bg-orange-500 text-white text-right ml-auto' : 'bg-blue-100 text-blue-900 text-left mr-auto'}`}
                            >
                                {msg.text}
                            </div>
                        ))}
                    </div>
        
                    {/* Input Container */}
                    <div className="flex items-center border-t border-gray-300 p-4">
                        <input
                            className="flex-grow p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring focus:border-blue-300"
                            type="text"
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                            placeholder="Enter your message..."
                        />
                        <button 
                            className="ml-4 bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600" 
                            onClick={handleSendMessage}
                        >
                            Send
                        </button>
                    </div>
                </div>
            </div>
        );
    
}




