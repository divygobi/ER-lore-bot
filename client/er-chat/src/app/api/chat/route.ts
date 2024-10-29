import { streamText, convertToCoreMessages, LoadAPIKeyError } from "ai";
import { createGoogleGenerativeAI } from '@ai-sdk/google';

// Allow streaming responses up to 30 seconds
export const maxDuration = 30;

const dotenv = require('dotenv');

dotenv.config({ path: '/Users/divygobiraj/Desktop/projects/ER_Lore_Bot/ER-lore-bot/.env' });


const google = createGoogleGenerativeAI(
  {apiKey: process.env.GOOGLE_GENERATIVE_AI_API_KEY,
  headers: {}}
);


export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = await streamText({
    model: google('gemini-1.5-flash'),
    messages: convertToCoreMessages(messages),
  });

  return result.toDataStreamResponse();
}
