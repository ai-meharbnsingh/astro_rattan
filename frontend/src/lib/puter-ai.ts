/**
 * Puter.js AI utility — free client-side AI provider.
 * Loaded via <script src="https://js.puter.com/v2/"></script> in index.html.
 * Falls back gracefully when Puter.js is blocked (ad-blocker, network issue).
 */

declare global {
  interface Window {
    puter?: {
      ai: {
        chat: (
          prompt: string | Array<{ role: string; content: string }>,
          options?: { model?: string; stream?: boolean },
        ) => Promise<any>;
      };
    };
  }
}

/** Default Vedic astrology system prompt shared across AI features. */
export const VEDIC_SYSTEM_PROMPT =
  'You are an expert Vedic astrologer. You provide accurate, helpful astrological guidance based on Vedic principles. Respond in a warm, knowledgeable tone. If the user shares birth details, analyze their chart. Include relevant planetary positions, doshas, and remedies.';

/** Check whether the Puter.js runtime is available. */
export function isPuterAvailable(): boolean {
  return typeof window !== 'undefined' && !!window.puter?.ai;
}

/**
 * Send a single-shot chat request via Puter.js.
 * Returns the assistant's text content.
 */
export async function puterChat(
  prompt: string,
  systemPrompt?: string,
): Promise<string> {
  if (!isPuterAvailable()) {
    throw new Error('Puter.js not loaded');
  }

  const messages: Array<{ role: string; content: string }> = [];
  if (systemPrompt) messages.push({ role: 'system', content: systemPrompt });
  messages.push({ role: 'user', content: prompt });

  const response = await window.puter!.ai.chat(messages, { model: 'gpt-4o' });
  return response?.message?.content || response?.text || '';
}

/**
 * Stream a chat response via Puter.js.
 * Calls `onChunk` with the *accumulated* text so the UI can display it
 * progressively. Returns the full text when done.
 */
export async function puterChatStream(
  prompt: string,
  systemPrompt?: string,
  onChunk?: (accumulated: string) => void,
): Promise<string> {
  if (!isPuterAvailable()) {
    throw new Error('Puter.js not loaded');
  }

  const messages: Array<{ role: string; content: string }> = [];
  if (systemPrompt) messages.push({ role: 'system', content: systemPrompt });
  messages.push({ role: 'user', content: prompt });

  const resp = await window.puter!.ai.chat(messages, {
    model: 'gpt-4o',
    stream: true,
  });

  let full = '';
  for await (const part of resp) {
    const text = part?.text || '';
    full += text;
    onChunk?.(full);
  }
  return full;
}
