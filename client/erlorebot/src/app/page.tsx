"use client";

import { useState } from "react";
import axios from "axios";
import "./page.css";
function App() {
  const [response, setResponse] = useState<string>("Hi there! How can I assist you?");
  const [value, setValue] = useState<string>("");

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) =>
    setValue(e.target.value);

  const handleSubmit = async () => {
    const response = await axios.post("http://127.0.0.1:5000/test/meow", {
      question: value,
    });
    setResponse(response.data.message);
  };

  return (
    <div className="container">
      <div>
        <input
          type="text"
          value={value}
          onChange={onChange}
        ></input>
      </div>
      <div>
        <button onClick={handleSubmit}>Click me for answers!</button>
      </div>
      <div>
        <p>Chatbot: {response}</p>
      </div>
    </div>
  );
};

export default App;
