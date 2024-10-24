import { streamText, convertToCoreMessages } from "ai";

// Allow streaming responses up to 30 seconds
export const maxDuration = 30;
const { GoogleGenerativeAI } = require("@google/generative-ai");
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = await streamText({
    model: genAI.getGenerativeModel({ model: "gemini-1.5-flash" }),
    messages: convertToCoreMessages(messages),
  });

  return result.toDataStreamResponse();
}
