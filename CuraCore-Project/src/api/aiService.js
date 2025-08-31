// src/api/aiService.js

const CHATBOT_API_URL = "http://localhost:5001/chat";

// This function will now talk to your Python backend
export const getChatbotResponse = async (message) => {
  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message: message })
  };

  try {
    const response = await fetch(CHATBOT_API_URL, requestOptions);
    const data = await response.json();
    if (data.reply) {
      return data.reply;
    } else {
      console.error("API response format error:", data);
      return "Sorry, I received an unexpected response from the server.";
    }
  } catch (error) {
    console.error("Error calling the chatbot server:", error);
    return "Sorry, I'm having trouble connecting to the chatbot service.";
  }
};

export const analyzeReport = async (reportText) => {
  console.log("Sending report to Gemini for analysis...");
  const prompt = `Please explain this medical report in simple, easy-to-understand terms for a non-medical person. Focus on key findings and suggest general, non-prescriptive next steps: "${reportText}"`;

  try {
    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();
    return text;
  } catch (error) {
    console.error("Error analyzing report with Gemini:", error);
    return "Sorry, there was an error analyzing the report. Please try again.";
  }
};