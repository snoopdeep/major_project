// InteractiveRagPanel Component
import { useState } from "react";
import {
  Brain,
  Upload,
  FileText,
  ChevronRight,
  CheckCircle,
  Activity,
  AlertTriangle,
  Search,
  Zap,
  MessageSquare,
} from "lucide-react";
const InteractiveRagPanel = ({ ragData }) => {
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [chatMessages, setChatMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");

  const topics = Object.keys(ragData).filter((key) => key !== "References");
  const filteredTopics = topics.filter((topic) =>
    topic.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleTopicSelect = (topic) => {
    setSelectedTopic(topic);
    setChatMessages([
      {
        type: "bot",
        content: ragData[topic],
        timestamp: new Date().toLocaleTimeString(),
      },
    ]);
  };

  const handleSendMessage = () => {
    if (!inputMessage.trim()) return;

    const newMessage = {
      type: "user",
      content: inputMessage,
      timestamp: new Date().toLocaleTimeString(),
    };

    // Simulate AI response
    const aiResponse = {
      type: "bot",
      content: `Based on your question about "${inputMessage}", I can provide additional context from the genomic analysis. ${
        selectedTopic
          ? ragData[selectedTopic].substring(0, 200) + "..."
          : "Please select a specific gene or topic for detailed information."
      }`,
      timestamp: new Date().toLocaleTimeString(),
    };

    setChatMessages((prev) => [...prev, newMessage, aiResponse]);
    setInputMessage("");
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">
      <div className="bg-gradient-to-r from-green-50 to-blue-50 p-6 border-b">
        <div className="flex items-center space-x-3">
          <Brain className="w-6 h-6 text-green-600" />
          <h3 className="text-xl font-bold text-gray-800">
            XAI Genetic Counselor
          </h3>
        </div>
        <p className="text-gray-600 mt-1">
          Interactive biological explanations
        </p>
      </div>

      <div className="flex h-96">
        {/* Topic Sidebar */}
        <div className="w-1/3 border-r bg-gray-50 p-4">
          <div className="relative mb-4">
            <Search className="w-4 h-4 absolute left-3 top-3 text-gray-400" />
            <input
              type="text"
              placeholder="Search genes..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="space-y-2 max-h-64 overflow-y-auto">
            {filteredTopics.map((topic) => (
              <button
                key={topic}
                onClick={() => handleTopicSelect(topic)}
                className={`w-full text-left p-3 rounded-lg text-sm font-medium transition-all ${
                  selectedTopic === topic
                    ? "bg-blue-100 text-blue-800 border border-blue-200"
                    : "bg-white text-gray-700 hover:bg-gray-100"
                }`}
              >
                <div className="flex items-center space-x-2">
                  <Zap className="w-4 h-4" />
                  <span>{topic}</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Chat Interface */}
        <div className="flex-1 flex flex-col">
          <div className="flex-1 p-4 overflow-y-auto bg-gray-50">
            {chatMessages.length === 0 ? (
              <div className="text-center text-gray-500 mt-8">
                <MessageSquare className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                <p>Select a gene or topic to start exploring</p>
              </div>
            ) : (
              <div className="space-y-4">
                {chatMessages.map((message, idx) => (
                  <div
                    key={idx}
                    className={`flex ${
                      message.type === "user" ? "justify-end" : "justify-start"
                    }`}
                  >
                    <div
                      className={`max-w-xs lg:max-w-md px-4 py-2 rounded-2xl ${
                        message.type === "user"
                          ? "bg-blue-600 text-white"
                          : "bg-white text-gray-800 shadow-sm border"
                      }`}
                    >
                      <p className="text-sm whitespace-pre-wrap">
                        {message.content}
                      </p>
                      <p
                        className={`text-xs mt-1 ${
                          message.type === "user"
                            ? "text-blue-200"
                            : "text-gray-500"
                        }`}
                      >
                        {message.timestamp}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Input Area */}
          <div className="p-4 border-t bg-white">
            <div className="flex space-x-2">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
                placeholder="Ask about genetic variants..."
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
              <button
                onClick={handleSendMessage}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InteractiveRagPanel;
