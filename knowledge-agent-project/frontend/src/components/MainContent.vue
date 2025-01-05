<template>
  <div class="main-content">
    <!-- 对话标题区域 -->
    <div v-if="currentConversation" class="conversation-header">
      <h2 class="conversation-title">{{ currentConversation.title }}</h2>
    </div>
    
    <!-- 欢迎信息 -->
    <div class="header-container" v-if="!showConversationHeader">
      <div class="header">
        <div class="title">
          <img src="@/assets/the-ship-svgrepo-com.svg" alt="DeepSeek Logo" class="logo" />
          <h2>我是 LearnSailor，你的个性化智能助学伙伴！</h2>
        </div>
        <p class="description">
          我可以基于文档内容进行对话，请把你的任务交给我吧~
        </p>
      </div>
    </div>

    <!-- 对话窗口 -->
    <div v-if="currentConversation" class="chat-section">
      <div ref="chatWindow" class="chat-window">
        <div v-for="(message, index) in currentConversation.messages" 
             :key="index" 
             class="chat-message">
          <div v-if="message.type === 'user'" class="user-message">
            <strong>User：</strong>{{ message.content }}
          </div>
          <div v-else class="bot-message">
            <strong>LearnSailor：</strong>{{ message.content }}
          </div>
        </div>
      </div>
    </div>

    <!-- 输入栏 -->
    <div class="input-container">
      <InputBar @send="handleSendMessage" />
    </div>
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
  computed: {
    showConversationHeader() {
      return this.currentConversation && this.currentConversation.messages.length > 0;
    },
  },
  methods: {
    handleSendMessage(message) {
      // 触发父组件的 send-message 事件
      this.$emit('send-message', message);
    },
    scrollToBottom() {
      const chatWindow = this.$refs.chatWindow;
      if (chatWindow) {
        chatWindow.scrollTop = chatWindow.scrollHeight;
      }
    },
  },
  watch: {
    'currentConversation.messages': {
      handler() {
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      },
      deep: true
    }
  }
};
</script>

<style scoped>
/* 保持原有样式不变 */
.main-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  background-color: #fff;
  overflow-y: auto;
  padding: 0;
  height: 100%;
}

.input-container {
  width: 100%;
  max-width: 700px;
  margin: 20px auto;
  padding: 0 20px;
  box-sizing: border-box;
  position: sticky;
  bottom: 0;
  background: white;
}

.header-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.chat-section {
  flex-grow: 1;
  width: 100%;
  display: flex;
  flex-direction: column;
  margin-top: 0;
  /* background: #fff; */
  padding: 20px;
  box-sizing: border-box;
}

.chat-window {
  flex-grow: 1;
  overflow-y: auto;
  border-radius: 10px;
  padding: 15px;
  /* background-color: #f9f9f9; */
  margin-bottom: 20px;
  max-height: calc(100vh - 200px);
}

.chat-message {
  font-size: 14px;
  color: #333;
  margin: 10px 0;
  padding: 8px 12px;
  border-radius: 8px;
}

.user-message {
  background-color: #ebfaff;
}

.bot-message {
  background-color: #d0edff;
}

.conversation-header {
  width: 100%;
  padding: 10px;
  background-color: #ffffff;
  box-sizing: border-box;
  text-align: center;
}

.conversation-title {
  font-size: 20px;
  font-weight: bold;
  color: #000000;
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
</style>