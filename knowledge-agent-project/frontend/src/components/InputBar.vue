<template>
  <div class="input-bar">
    <textarea
      v-model="newMessage"
      placeholder="给 LearnSailor 发送消息"
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

    <!-- 图问引擎按钮 -->
    <button class="engine-btn" :class="{ active: engineOn }" @click="toggleEngine">
      图问引擎
      <img
        class="engine-icon"
        :src="engineOn ? onIcon : offIcon"
        alt="图问引擎状态"
      />
    </button>
  </div>
</template>

<script>
import axios from 'axios';
import onIcon from '@/assets/on.svg'; // 引入 on.svg 图标
import offIcon from '@/assets/off.svg'; // 引入 off.svg 图标

export default {
  data() {
    return {
      newMessage: "",
      engineOn: false, // 图问引擎开关状态
      // 图标资源
      onIcon,
      offIcon,
      file: null, // 选中的文件
      isUploading: false, // 上传状态
    };
  },
  methods: {
    autoResize(event) {
      const textarea = event.target;
      textarea.style.height = "auto"; // 重置高度
      textarea.style.height = `${textarea.scrollHeight}px`; // 动态调整高度
    },
    sendMessage() {
      if (!this.newMessage.trim()&& !this.file) {
        alert('请输入问题内容！');
        return;
      }
      
      // 缓存消息内容
      const message = this.newMessage.trim();
      
      // 清空输入框内容
      this.newMessage = "";

      // 发送消息
      if (this.file) {
        this.uploadFile(message);
      } else {
        this.sendQuestionOnly(message);
      }
    },
    openFilePicker() {
      this.$refs.fileInput.click();
    },
    toggleEngine() {
      this.engineOn = !this.engineOn; // 切换图问引擎状态
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
      formData.append("file", this.file);
      formData.append("question", this.newMessage.trim());

      this.isUploading = true;
      this.$emit("send", { type: "user", content: this.newMessage.trim() });

      try {
        const response = await axios.post(this.getApiUrl('upload'), formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        console.log("Response from server:", response.data, response.data.response);
        if (response.data && response.data.response) {
          this.$emit("send", { type: "bot", content: response.data.response });
        } else {
          this.$emit("send", { type: "bot", content: "[问题回复，但未收到有效响应]" });
        }
      } catch (error) {
        console.error("文件上传失败:", error);
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
      this.$emit("send", { type: "user", content: this.newMessage.trim() });
      try {
        const response = await axios.post(this.getApiUrl('question'), {
          question: this.newMessage.trim(),
        });
        console.log("Response from server:", response.data, response.data.response);
        if (response.data && response.data.response) {
          this.$emit("send", { type: "bot", content: response.data.response });
        } else {
          this.$emit("send", { type: "bot", content: "[问题回复，但未收到有效响应]" });
        }
      } catch (error) {
        console.error("问题发送失败:", error);
        this.$emit("send", { type: "bot", content: `[问题发送失败]\n错误信息: ${error.message}` });
      }
    },
    getApiUrl(endpoint) {
        const baseUrls = {
          upload: this.engineOn ? '/api/upload_with_graph' : '/api/upload',
          question: this.engineOn ? '/api/question_with_graph' : '/api/question',
        };
        return baseUrls[endpoint];
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
  border-radius: 20px;
  background-color: #f0f8ff;
}

.textarea {
  flex-grow: 1;
  padding: 10px 10px 0 10px;
  border: none;
  outline: none;
  resize: none; 
  overflow: auto;
  background-color: aliceblue;
  font-size: 18px;
  border-radius: 10px;
  font-family: Arial, Helvetica, sans-serif;
  line-height: 1.5;
  min-height: 40px; /* 设置输入框最小高度 */
  max-height: 200px; /* 可选：限制最大高度 */
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

.engine-btn {
  display: flex;
  align-items: center;
  gap: 1px;
  background-color: #f0f8ff;
  border: 1px solid #f0f8ff;
  color: #333; /* 默认文字颜色 */
  font-size: 16px;
  padding: 8px 12px;
  border-radius: 15px;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.engine-btn:hover {
  background-color: #e3f2fd;
}

.engine-btn.active {
  color: #1296db; /* 激活状态的文字颜色 */
  background-color: #e3f2fd; /* 激活状态的背景颜色 */
}


/* 图标大小调整 */
.engine-icon {
  width: 40px; /* 调整图标宽度 */
  height: 40px; /* 调整图标高度 */
}
</style>