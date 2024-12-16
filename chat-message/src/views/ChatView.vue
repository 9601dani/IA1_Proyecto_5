<template>
  <div class="bg-gray-100 h-screen flex flex-col max-w-lg mx-auto">
    <div class="bg-blue-500 p-4 text-white flex justify-between items-center">
      <span>ChatBot</span>
    </div>

    <!-- Chat Messages -->
    <ChatMessages :messages="messages" />

    <!-- Message Box -->
    <MessageBox @send-message="onMessage" />
  </div>
</template>

<script setup>
import ChatMessages from '@/components/chat/ChatMessages.vue';
import MessageBox from '@/components/chat/MessageBox.vue';
import { useChat } from '@/composables/useChat';

// Usamos el composable para manejar la lógica del chat
const { messages, onMessage } = useChat();
</script>
