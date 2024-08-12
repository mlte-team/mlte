import { createError } from 'h3';
import type { IChatgptClient, IMessage, IModel, IOptions } from "~/types";

export const openai = (): IChatgptClient => {
  const chatCompletion = async (messages: IMessage[], model?: IModel, options?: IOptions) => {
    try {
      return await $fetch('/api/chat-completion', {
        method: 'POST',
        body: { messages, model, options }
      });
    } catch (error) {
      throw createError({
        statusCode: 500,
        message: 'Failed to forward request to server',
      });
    }
  };

  return { chat: chatCompletion }; // Returning chatCompletion as chat
};
