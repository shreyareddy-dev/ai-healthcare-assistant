import { useEffect, useState } from "react";
import axios from "axios";

function App() {

  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [emergency, setEmergency] = useState(false);
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);

  // ==========================================
  // FETCH CHAT HISTORY
  // ==========================================
  const fetchChatHistory = async () => {

    try {

      const res = await axios.get(
        "http://127.0.0.1:8000/chat-history"
      );

      setChatHistory(res.data.chat_history.reverse());

    } catch (error) {

      console.log(error);

    }
  };

  // ==========================================
  // SEND MESSAGE
  // ==========================================
  const sendMessage = async () => {

    if (!message.trim()) return;

    setLoading(true);

    try {

      const res = await axios.post(
        "http://127.0.0.1:8000/chat",
        {
          message: message
        }
      );

      setResponse(res.data.response);
      setEmergency(res.data.emergency);

      fetchChatHistory();

    } catch (error) {

      console.log(error);

      setResponse("Error connecting to backend.");

    } finally {

      setLoading(false);

    }
  };

  // ==========================================
  // LOAD HISTORY ON PAGE LOAD
  // ==========================================
  useEffect(() => {

    fetchChatHistory();

  }, []);

  return (

    <div className="min-h-screen bg-gradient-to-br from-blue-100 via-white to-blue-200 p-6">

      <div className="max-w-5xl mx-auto grid md:grid-cols-2 gap-6">

        {/* LEFT SIDE */}
        <div className="bg-white/70 backdrop-blur-lg shadow-2xl rounded-3xl p-8">

          <h1 className="text-4xl font-bold text-center text-blue-900 mb-6">
            AI Healthcare Assistant
          </h1>

          <textarea
            rows="5"
            placeholder="Describe your symptoms..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className="w-full p-4 rounded-2xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400 text-lg"
          />

          <button
            onClick={sendMessage}
            className="w-full mt-5 bg-blue-900 hover:bg-blue-800 transition-all text-white py-4 rounded-2xl text-lg font-semibold"
          >

            {loading ? "Analyzing..." : "Analyze Symptoms"}

          </button>

          {response && (

            <div
              className={`mt-6 p-6 rounded-2xl shadow-md ${
                emergency
                  ? "bg-red-100 border border-red-400"
                  : "bg-blue-50 border border-blue-200"
              }`}
            >

              <h2 className="text-2xl font-bold mb-3">

                {emergency
                  ? "🚨 Emergency Alert"
                  : "AI Healthcare Response"}

              </h2>

              <p className="text-lg leading-relaxed text-gray-700">
                {response}
              </p>

            </div>

          )}

        </div>

        {/* RIGHT SIDE - CHAT HISTORY */}
        <div className="bg-white/70 backdrop-blur-lg shadow-2xl rounded-3xl p-6 max-h-[90vh] overflow-y-auto">

          <h2 className="text-3xl font-bold text-blue-900 mb-5">
            Chat History
          </h2>

          {chatHistory.length === 0 ? (

            <p>No chat history available.</p>

          ) : (

            chatHistory.map((chat, index) => (

              <div
                key={index}
                className={`mb-4 p-4 rounded-2xl shadow ${
                  chat.emergency
                    ? "bg-red-50 border border-red-300"
                    : "bg-blue-50 border border-blue-200"
                }`}
              >

                <p className="font-semibold text-gray-800">
                  Symptom:
                </p>

                <p className="mb-2 text-gray-700">
                  {chat.user_input}
                </p>

                <p className="font-semibold text-gray-800">
                  Response:
                </p>

                <p className="text-gray-700">
                  {chat.response}
                </p>

              </div>

            ))

          )}

        </div>

      </div>

    </div>
  );
}

export default App;