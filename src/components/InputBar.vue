<template>
    <div class="input-bar">
      <input
        v-model="newMessage"
        type="text"
        placeholder="发送消息"
        class="input"
      />
      <button class="send-btn" @click="sendMessage">发送</button>
      <button class="upload-btn">
        📎 上传
        <input type="file" @change="uploadFile" hidden />
      </button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        newMessage: "",
      };
    },
    methods: {
      sendMessage() {
        if (this.newMessage.trim()) {
          this.$emit("send", this.newMessage);
          this.newMessage = ""; // 清空输入框
        }
      },
      uploadFile(event) {
        const file = event.target.files[0];
        if (file) {
          this.$emit("send", `[文件]: ${file.name}`); // 模拟发送文件名
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .input-bar {
    display: flex;
    align-items: center;
    gap: 10px;
    border: 1px solid #ddd;
    padding: 10px;
    border-radius: 5px;
  }
  
  .input {
    flex-grow: 1;
    padding: 10px;
    border: none;
    outline: none;
  }
  
  .send-btn {
    background-color: #1976d2;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
  }
  
  .upload-btn {
    background-color: #ddd;
    padding: 10px;
    border-radius: 5px;
    cursor: pointer;
  }
  </style>
  