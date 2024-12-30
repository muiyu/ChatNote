<template>
  <div class="main-content">
    <!-- 对话标题区域 -->
    <div v-if="currentConversation" class="conversation-header">
      <h2 class="conversation-title">{{ currentConversation.title }}</h2>
    </div>

    <!-- 欢迎信息 -->
    <div class="header" v-if="!currentConversation">
      <div class="title">
        <img src="@/assets/vue.svg" alt="DeepSeek Logo" class="logo" />
        <h2>我是 DeepSeek，很高兴见到你！</h2>
      </div>
      <p class="description">
        我可以帮你写代码、读文件、写作各种创意内容，请把你的任务交给我吧~
      </p>
    </div>

    <!-- 对话窗口 -->
    <div v-if="currentConversation" class="chat-section">
      <div class="chat-window">
        <p
          v-for="(message, index) in currentConversation.messages"
          :key="index"
          class="chat-message"
        >
          {{ message }}
        </p>
      </div>
      <!-- 输入栏 -->
      <InputBar @send="sendMessage" />
    </div>
    <!-- 无选中对话的提示 -->
    <p v-else class="no-conversation">
      请选择一个对话或开启新对话
    </p>
  </div>
</template>

<script>
import InputBar from "@/components/InputBar.vue";

export default {
  props: {
    currentConversation: {
      type: Object,
      required: false,
    },
  },
  components: {
    InputBar,
  },
  methods: {
    sendMessage(message) {
      // 通知父组件发送消息
      this.$emit("send-message", message);
    },
  },
};
</script>

<style scoped>
.main-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  background-color: #fff;
  overflow-y: auto;
  padding: 0;
}

.conversation-header {
  width: 100%;
  padding: 10px;
  background-color: #ffffff;
  box-sizing: border-box;
  text-align: center;
}

.conversation-title {
  font-size: 20px; /* 更大字体 */
  font-weight: bold;
  color: #000000; /* 突出标题 */
  margin: 0;
}

.header {
  text-align: center;
  padding: 20px;
}

.title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.logo {
  width: 50px;
  height: 50px;
}

h2 {
  font-size: 24px;
  color: #444;
  margin: 0;
}

.description {
  font-size: 16px;
  color: #666;
  margin-top: 10px;
}

.chat-section {
  flex-grow: 1;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin-top: 0;
  background: #fff; /* 去掉渐变 */
  padding-top: 20px;
}

.chat-window {
  flex-grow: 1;
  max-height: 400px;
  overflow-y: auto;
  border-radius: 10px;
  padding: 15px;
  background-color: #f9f9f9;
  margin: 20px 0;
}

.chat-message {
  font-size: 14px;
  color: #333;
  margin: 10px 0;
  padding: 8px 12px;
  border-radius: 8px;
  background-color: #ebfaff;
}

.chat-message:nth-child(even) {
  background-color: #d0edff;
}

.no-conversation {
  text-align: center;
  font-size: 16px;
  color: #888;
  margin-top: 50px;
}
</style>
