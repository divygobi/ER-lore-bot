import { streamText, convertToCoreMessages, LoadAPIKeyError } from "ai";
import { createGoogleGenerativeAI } from '@ai-sdk/google';
import { promises } from "dns";

// Allow streaming responses up to 30 seconds
export const maxDuration = 30;

const dotenv = require('dotenv');

dotenv.config({ path: '/Users/divygobiraj/Desktop/projects/ER_Lore_Bot/ER-lore-bot/.env' });


const google = createGoogleGenerativeAI(
  {apiKey: process.env.GOOGLE_GENERATIVE_AI_API_KEY,
  headers: {}}
);

async function getDocuments(message: String) {
  const documents = await fetch('http://127.0.0.1:5000/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({"prompt": message})
  });
  return documents.json();
}


export async function POST(req: Request) {
  const { messages } = await req.json();
  console.log(messages);
  
  const mostRecentMessage: String = messages[messages.length - 1].content;
  console.log(mostRecentMessage);

  const documents = await getDocuments(mostRecentMessage);
  
  console.log(documents);

  const result = await streamText({
    model: google('gemini-1.5-flash'),
    messages: convertToCoreMessages(messages),
  });

  return result.toDataStreamResponse();
}


