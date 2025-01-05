<template>
    <div class="chat">
      <div class="chat-window">
        <p v-for="(message, index) in messages" :key="index">{{ message }}</p>
      </div>
      <input
        v-model="newMessage"
        @keyup.enter="sendMessage"
        placeholder="输入消息..."
        class="chat-input"
      />
    </div>
  </template>
  
  <script>
  export default {
    props: {
      messages: {
        type: Array,
        required: true,
      },
    },
    data() {
      return {
        newMessage: "", // 用户输入的消息
      };
    },
    methods: {
      sendMessage() {
        if (this.newMessage.trim()) {
          this.messages.push(this.newMessage); // 添加消息
          this.newMessage = ""; // 清空输入框
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .chat {
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 10px;
  }
  
  .chat-window {
    max-height: 200px;
    overflow-y: auto;
    margin-bottom: 10px;
  }
  
  .chat-input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
  </style>
  