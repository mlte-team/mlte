import OpenAI from 'openai';
import { createError, defineEventHandler, readBody } from "h3";
import { defaultOptions } from "~/constants/options";
import { MODEL_GPT_TURBO_3_5 } from '~/constants/models';
import { modelMap } from "../../utils/model-map";
import { useRuntimeConfig } from '#imports';

export default defineEventHandler(async (event) => {
  console.log('Request received at /api/chat');
  const { message, model, options } = await readBody(event);
  console.log('Request body:', { message, model, options });

  // Ensure the API key is set
  if (!useRuntimeConfig().private.apiKey) {
    throw createError({
      statusCode: 403,
      message: 'Missing OpenAI API Key',
    });
  }

  // Initialize OpenAI client
  const openai = new OpenAI({
    apiKey: useRuntimeConfig().private.apiKey,
  });

  // Set up requestOptions with default options if none are provided
  const requestOptions = {
    messages: [
      { role: 'system', content: 'You are a helpful assistant.' }, // System prompt
      { role: 'user', content: message }, // User message
    ],
    model: !model ? modelMap[MODEL_GPT_TURBO_3_5] : modelMap[model],
    ...defaultOptions,  // Default options
    ...(options || {})  // Override with provided options if available
  };

  try {
    // Call OpenAI API
    const chatCompletion = await openai.chat.completions.create(requestOptions);
    return (chatCompletion.choices[0] as { message: { content: string } }).message?.content;
  } catch (error) {
    throw createError({
      statusCode: 500,
      message: 'Failed to forward request to OpenAI API',
    });
  }
});
