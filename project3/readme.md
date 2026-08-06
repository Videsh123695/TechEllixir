# Dual-Track AI Chatbot Assistant (MERN Stack Feature)

A production-ready, highly lightweight AI chatbot feature integrated into a full-stack MERN development environment. Powered by the modern `@google/genai` SDK and Gemini 3.5 flash-lite, this bot utilizes conditional system prompt engineering to automatically classify and route incoming website users into two separate tracks: **Business Client Project Leads** or **Student Internship Trainees**.

---

## 🌟 Key Project Highlights

- **Zero Heavy Markdown Packages:** Built to run on absolute minimal dependencies. It uses a single runtime package (`lucide-react` for icons) and handles markdown structures natively using clean, lightweight CSS tricks (`whitespace-pre-line`).
- **Dual-Track Contextual Prompting:** The AI automatically detects user intent and guides business owners down a sales pipeline and students down an internship/training onboarding track.
- **Mock Database Hand-off Layer:** Designed with modularity in mind. Instead of binding to a rigid, separate local database, it features clean backend hooks that allow other core developers to connect it to their primary database (e.g., MongoDB, SQL) seamlessly.
- **Enterprise-Grade Error Handling:** Restricts operations to specific methods and origins via CORS protection. It catches API issues locally in the server log while delivering friendly error handling on the public frontend.

---

## 🛠️ System Architecture Diagram

        [React Frontend (Port 5173)]
            │
    (Secure Fetch API Payload)
                ▼
    [Node.js + Express Backend (Port 5000)]
                │
    ┌───────────┴───────────┐
    ▼                       ▼
    [Google Gemini API]                             [MockDatabaseHand-off Point]                       
    (Generates Context Response)
    (Triggers Terminal Lead Validation)


---

## 💻 Local Workspace Configuration

Follow these quick steps to get the environment running on your local machine:

### 1. Backend Server Setup
1. Open a terminal window and navigate into the backend folder:
   ```bash
   cd backend
   ```
2. Install the lightweight runtime dependencies:
   ```bash
   npm install
   ```
3. Create a `.env` file in the root of the `backend/` directory and input your credentials:
   ```env
   PORT=5000
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```
4. Boot up the local development hot-reload node environment:
   ```bash
   npm run dev
   ```

### 2. Frontend Interface Setup
1. Open a separate terminal window and navigate into the frontend folder:
   ```bash
   cd frontend
   ```
2. Install the minimalist client dependencies:
   ```bash
   npm install
   ```
3. Launch the hot-reloading Vite engine interface:
   ```bash
   npm run dev
   ```
4. Click the local server link or type this into your browser to interact with the bot: `http://localhost:5173`

---

## 🤝 Collaborative Team Integration Point

For developers looking to pipe captured chatbot leads directly into a live database layout (like a centralized MongoDB schema):
1. Navigate to your `backend/server.js` file.
2. Locate the conditional `MOCK DATABASE HAND-OFF LOGIC` block.
3. Replace the placeholder `console.log()` triggers with your specific asynchronous database operations (e.g., `await ClientLead.create({ name, email })`).