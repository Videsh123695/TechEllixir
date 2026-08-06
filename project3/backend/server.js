const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const { GoogleGenAI } = require('@google/genai');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;
// Middleware

// Remove your old app.use(cors()) and replace it with this:
app.use(cors({
  origin: "http://localhost:5173", // Points exactly to your React UI
  methods: ["GET", "POST"],
  allowedHeaders: ["Content-Type"]
}));

app.use(express.json());
const ai = new GoogleGenAI({apiKey:process.env.GEMINI_API_KEY});

// Strict system prompt for dual-track user routing (Clients vs Students)
const SYSTEM_INSTRUCTION = `
You are "ApexBot," the official AI Assistant for Apex Tech Solutions. Your dual mission is to acquire business clients for our IT services and recruit students for our training/internship programs.

### Identity & Tone
- Persona: Professional yet approachable, tech-savvy, and highly organized.
- Style: Keep responses short and easy to scan. Use clear markdown bullet points.
- Greeting: Always offer a dual greeting, for example: "Hello! Welcome to Apex Tech Solutions. Are you looking to build a digital solution for your business, or are you a student looking for tech training?"

### Dual-Track Workflows (Strict Routing)

#### TRACK 1: Business Clients (Project Leads)
- Target: Businesses looking for Web/App Development, Custom Software, or Digital Marketing.
- Action: Qualify the lead. Politely ask for: 
  1. Contact Name
  2. Business Email or Phone Number
  3. Brief project requirements or goals
- Note: Never invent prices or project timelines. Say: "Our project managers will review your requirements and provide a custom quote."

#### TRACK 2: Students & Trainees (Internships/Courses)
- Target: Students looking for Industrial Training, Tech Internships, or Upskilling.
- Action: Guide them to enrollment. Provide info on available courses (MERN Stack, Python AI, UI/UX) and ask for: 
  1. Student Name 
  2. Contact Number
  3. Technology of interest

### Safety & Fallback Guardrails
- Focus: Decline questions completely unrelated to our company, IT services, or training programs.
- Fallback: If stuck or unable to answer a complex question, use: "I want to make sure you get the exact information. Please leave your email, or reach our team directly at info@apextech.com."
`;

app.get('/',(req,res)=>{
  res.send("the server is running")
})

app.post('/api/chat', async (req, res) => {
  try {
    const { messageHistory } = req.body; 

    if (!messageHistory || !Array.isArray(messageHistory)) {
      return res.status(400).json({ error: "Invalid message history format." });
    }

    // Modern @google/genai package initialization syntax
    // const model = ai.models.get("gemini-3.5-flash-lite");

    // Re-format history to fit the strict API input schema
    const contents = messageHistory.map(msg => ({
      role: msg.role === 'model' ? 'model' : 'user',
      parts: [{ text: msg.text }]
    }));

    // Call the model cleanly using the contents history stack
    const response = await ai.models.generateContent({
      model: 'gemini-3.5-flash-lite',
      contents: contents,
      config: {
        systemInstruction: SYSTEM_INSTRUCTION
      }
    });

    const responseText = response.text;

    // MOCK DATABASE HAND-OFF LOGIC
    const lowcaseText = responseText.toLowerCase();
    if (lowcaseText.includes("project") || lowcaseText.includes("business email")) {
      console.log("➡️ [DB MOCK SAVE] Lead Type: Business Client.");
    } else if (lowcaseText.includes("course") || lowcaseText.includes("internship")) {
      console.log("➡️ [DB MOCK SAVE] Lead Type: Student / Trainee.");
    }

    res.json({ text: responseText });
  } catch (error) {
    console.error("Gemini API Internal Crash Logs:", error.message);
    res.status(500).json({error: error.message});
  }
});



app.listen(PORT, () => {
  console.log(`🚀 Chatbot backend running smoothly on port http://localhost:${PORT}`);
});