import OpenAI from 'openai';
import { createError, defineEventHandler, readBody } from "h3";
import { defaultOptions } from "~/constants/options";
import { MODEL_GPT_TURBO_3_5 } from '~/constants/models';
import { modelMap } from "../../utils/model-map";
import { useRuntimeConfig } from '#imports';

export default defineEventHandler(async (event) => {
  const { messages, model, options } = await readBody(event);

  if (!useRuntimeConfig().private.apiKey) {
    throw createError({
      statusCode: 403,
      message: 'Missing OpenAI API Key',
    });
  }

  const openai = new OpenAI({
    apiKey: useRuntimeConfig().private.apiKey
  });

  const requestOptions = {
    messages,
    model: model ? modelMap[model] : modelMap[MODEL_GPT_TURBO_3_5],
    ...(options || defaultOptions)
  };

  try {
    const chatCompletion = await openai.chat.completions.create(requestOptions);
    return chatCompletion.choices.map(choice => choice.message.content).join('\n');
  } catch (error) {
    throw createError({
      statusCode: 500,
      message: 'Failed to forward request to OpenAI API',
    });
  }
});
