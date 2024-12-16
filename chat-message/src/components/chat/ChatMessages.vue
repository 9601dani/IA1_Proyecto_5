<template>
  <div ref="chatRef" class="flex-1 overflow-y-auto p-4">
    <div class="flex flex-col space-y-2">
      <!-- Mostrar los mensajes -->
      <ChatBubble v-for="message in messages" :key="message.id" v-bind="message" />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import ChatBubble from './ChatBubble.vue';

// Recibir los mensajes desde props
const props = defineProps({
  messages: {
    type: Array,
    required: true,
  },
});

const chatRef = ref(null);

// Usar watch en la longitud de los mensajes para detectar cambios
watch(
  () => props.messages.length, // Observamos el tamaño del arreglo
  () => {
    if (chatRef.value) {
      setTimeout(() => {
        chatRef.value?.scrollTo({
          top: chatRef.value.scrollHeight,
          behavior: 'smooth',
        });
      }, 100);
    }
  },
);
</script>
