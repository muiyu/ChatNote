<template>
    <div class="input-bar">
      <input
        v-model="newMessage"
        type="text"
        placeholder="发送消息"
        class="input"
        @keyup.enter="sendMessage"
      />
      <button class="send-btn" @click="sendMessage">发送</button>
      <button class="upload-btn" @click="openFilePicker">
        📎 上传
        <input type="file" @change="uploadFile" hidden ref="fileInput"/>
      </button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';

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
      openFilePicker() {
        this.$refs.fileInput.click(); // 手动触发文件输入元素的点击事件
      },
      async uploadFile(event) {
        console.log('File input changed'); // 调试日志
        const file = event.target.files[0];
        if (!file) {
          alert('请选择一个文件。');
          return;
        }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('question', this.newMessage || '默认问题');

        try {
          const response = await axios.post('/api/upload', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });

          if (response.data && response.data.response) {
            this.$emit("send", `[文件上传成功]: ${file.name}\n${response.data.response}`);
          } else {
            this.$emit("send", `[文件上传成功，但未收到有效响应]: ${file.name}`);
          }
        } catch (error) {
          console.error('文件上传失败:', error);
          if (error.response) {
            // 后端返回的错误
            this.$emit("send", `[文件上传失败]: ${file.name}\n错误信息: ${error.response.data.error}`);
          } else if (error.request) {
            // 请求未发送到后端
            this.$emit("send", `[文件上传失败]: ${file.name}\n请求未发送到后端`);
          } else {
            // 其他错误
            this.$emit("send", `[文件上传失败]: ${file.name}\n错误信息: ${error.message}`);
          }
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
  