<template>
  <div class="input-bar">
    <textarea
      v-model="newMessage"
      placeholder="给 CloudSeek 发送消息"
      class="textarea"
      @input="autoResize"
    ></textarea>

    <button class="send-btn" :disabled="!newMessage.trim()" @click="sendMessage">
      <img
        src="@/assets/send.svg"
        alt="发送"
        class="icon"
      />
    </button>

    <button class="upload-btn" :disabled="isUploading" @click="openFilePicker">
      <img
        src="@/assets/upload.svg"
        alt="上传"
        class="icon"
      />
      <input type="file" @change="uploadFile" hidden ref="fileInput" />
    </button>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      newMessage: "",
      file: null,
      isUploading: false,
    };
  },
  methods: {
    sendMessage() {
      if (!this.newMessage.trim()&& !this.file) {
        alert('请输入问题内容！');
        return;
      }
      
      if (this.file) {
        this.uploadFile();
      } else {
        this.sendQuestionOnly();
      }
    },
    openFilePicker() {
      this.$refs.fileInput.click();
    },
    async uploadFile(event) {
      if (this.isUploading) return;
      if (event) {
        this.file = event.target.files[0];
        event.target.value = ''; 
      }

      if (!this.file) {
        alert('请选择一个文件。');
        return;
      }

      if (!this.newMessage.trim()) {
        alert('请输入问题内容！');
        return;
      }   

      console.log('this.file:', this.file);

      const formData = new FormData();
      formData.append('file', this.file);
      formData.append('question', this.newMessage.trim());

      this.isUploading = true;
      this.$emit("send", { type: 'user', content: this.newMessage.trim() });
      try {
        const response = await axios.post('/api/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        console.log("Response from server:", response.data, response.data.response);
        if (response.data && response.data.response) {
          this.$emit("send",  { type: 'bot', content: response.data.response });
        } else {
          this.$emit("send", {type: 'bot', content: '[问题回复，但未收到有效响应]'});
        }
      } catch (error) {
        console.error('文件上传失败:', error);
        this.$emit("send", {
          type: "bot",
          content: `[文件上传失败]: ${this.file.name}\n错误信息: ${error.message}`,
        });
      } finally {
        this.file = null;
        this.isUploading = false;
      }
    },
    async sendQuestionOnly() {
      this.$emit("send", { type: 'user', content: this.newMessage.trim() });

      try {
        const response = await axios.post('/api/question', {
          question: this.newMessage.trim(),
        });
        console.log("Response from server:", response.data, response.data.response);
        if (response.data && response.data.response) {
          this.$emit("send", { type: 'bot', content: response.data.response });
        } else {
          this.$emit("send", { type: 'bot', content: '[问题回复，但未收到有效响应]' });
        }
      } catch (error) {
        console.error('问题发送失败:', error);
        this.$emit("send", { type: 'bot', content: `[问题发送失败]\n错误信息: ${error.message}` });
      } finally {
        this.newMessage = "";
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
  border: 1px solid rgb(211, 227, 230);
  padding: 10px;
  border-radius: 15px;
  background-color: #f0f8ff;
}

.textarea {
  flex-grow: 1;
  padding: 10px;
  border: none;
  outline: none;
  resize: none; 
  overflow: hidden;
  background-color: aliceblue;
  font-size: 15px;
  border-radius: 5px;
  font-family: Arial, Helvetica, sans-serif;
  line-height: 1.0;
}

.send-btn,
.upload-btn {
  background-color: transparent;
  border: none;
  padding: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 15px;
  transition: background-color 0.2s ease;
}

.send-btn:hover,
.upload-btn:hover {
  background-color: #e3f2fd;
}

.send-btn:disabled,
.upload-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.icon {
  width: 24px;
  height: 24px;
}
</style>