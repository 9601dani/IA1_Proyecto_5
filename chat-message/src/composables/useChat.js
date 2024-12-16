import { ref } from 'vue';
import { sleep } from '../helpers/sleep';

export const useChat = () => {
  const messages = ref([]);

  const getHerResponse = async () => {
    const resp = await fetch('https://yesno.wtf/api');
    const data = await resp.json();
    return data;
  };

  const onMessage = async (text) => {
    if (text.length === 0) return;

    // Add user's message
    messages.value.push({
      id: new Date().getTime(),
      itsMine: true,
      message: text,
    });

    if (!text.endsWith('?')) return;
    
    await sleep(1.5);

    // Fetch response from the API
    const { answer, image } = await getHerResponse();

    // Add the response message
    messages.value.push({
      id: new Date().getTime(),
      itsMine: false,
      message: answer,
      image,
    });
  };

  return {
    // Properties
    messages,
    // Methods
    onMessage,
  };
};
