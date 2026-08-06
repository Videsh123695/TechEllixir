// import React from 'react';
import Chatbot from './components/Chatbot';

export default function App() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <div className="bg-white p-6 rounded-xl shadow-md max-w-sm w-full text-center border border-gray-200">
        <h1 className="text-2xl font-bold text-gray-800">Apex Tech Solutions</h1>
        <p className="text-gray-600 text-sm mt-2">
          Welcome to our website! Use the chatbot in the bottom right corner to talk to us.
        </p>
      </div>

      <Chatbot />
    </div>
  );
}
