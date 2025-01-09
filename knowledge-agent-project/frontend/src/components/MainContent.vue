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
          <h2>你好呀，我是 LearnSailor，你的智慧学习伙伴！</h2>
        </div>
        <p class="description">
          我可以基于文档内容进行对话，请把你的问题交给我吧~
        </p>
      </div>
    </div>

    <!-- 对话窗口 -->
    <div v-if="currentConversation" class="chat-section">
      <div ref="chatWindow" class="chat-window">
        <!-- <div v-for="(message, index) in currentConversation.messages" 
             :key="index" 
             class="chat-message">
          <div v-if="message.type === 'user'" class="user-message">
            <strong>User：</strong>{{ message.content }}
          </div>
          <div v-else class="bot-message">
            <strong>LearnSailor：</strong>{{ message.content }}
          </div>
        </div> -->
        <!-- 循环渲染消息 -->
        <div
          v-for="(message, index) in currentConversation.messages"
          :key="index"
          :class="['text-item', { 'text-item-right': message.type === 'user' }]"
        >
          <!-- 机器人头像 -->
          <div v-if="message.type === 'bot'" class="chat-name bot-avatar">
            <img src="@/assets/the-ship-svgrepo-com.svg" alt="Bot Avatar" class="bot-icon" />
          </div>
          <!-- 用户头像 -->
          <div v-else class="chat-name">
            User
          </div>

          <!-- 聊天气泡 -->
          <!-- <div class="chat-box">
            {{ message.content }}
          </div> -->
          <div class="chat-box" v-html="parseMarkdown(message.content)"></div>

        </div>
      </div>
    </div>

    <!-- 输入栏 -->
    <!-- <div class="input-container">
      <InputBar @send="handleSendMessage" />
    </div> -->
    <div v-if="currentConversation" class="input-container">
      <InputBar @send="handleSendMessage" />
    </div>
  </div>
</template>

<script>
import InputBar from "@/components/InputBar.vue";
import { marked } from "marked";

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
    // 控制欢迎信息显示的逻辑
    showConversationHeader() {
      return this.currentConversation && this.currentConversation.messages.length > 0;
    },
  },
  methods: {
    handleSendMessage(message) {
      // 触发父组件的 send-message 事件，将用户发送的消息添加到 currentConversation
      this.$emit('send-message', message);
      console.log('[handleSendMessage] message:', message);
    },
    scrollToBottom() {
      const chatWindow = this.$refs.chatWindow;
      if (chatWindow) {
        chatWindow.scrollTop = chatWindow.scrollHeight;
      }
    },
    parseMarkdown(content) {
      // 解析 Markdown 为 HTML
      return marked(content || "");
    },
  },
  watch: {
    // 自动滚动到底部，监听消息变化
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
.main-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  background-color: #fff;
  overflow-y: hidden;
  padding: 0;
  height: 100%;
}

.input-container {
  width: 100%;
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
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
 
.bot-avatar {
  margin-right: 10px; /* 增加头像与气泡的距离 */
}

.text-item {
  display: flex;
  align-items: flex-start; /* 更好地对齐头像和气泡 */
  margin-bottom: 15px; /* 加大消息之间的间距 */
}


.text-item:last-child {
  margin-bottom: 0;
}

.chat-name {
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  border-radius: 50%; 
  background-color: #3c8aff;
  color: #fff;
  flex-shrink: 0;
  overflow: hidden; 
}

/* 机器人头像容器样式 */
.bot-avatar {
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #ffffff; /* 背景为白色 */
  border: 1px solid #ddd; /* 可选：加一条浅色边框，提升视觉效果 */
  border-radius: 50%; /* 圆形头像 */
  overflow: hidden; /* 防止内容溢出 */
  flex-shrink: 0; /* 防止容器被压缩 */
}

/* 机器人头像图标样式 */
.bot-icon {
  width: 100%; /* 图标占头像容器的比例 */
  height: 100%;
  object-fit: cover; /* 确保图标按比例缩放 */
}

/* 左侧对话气泡的箭头 */
.chat-box:before {
  content: "";
  position: absolute;
  right: 100%;
  top: 50%;
  width: 0;
  height: 0;
  border-top: 9px solid transparent;
  border-right: 8px solid #ffffff;
  border-bottom: 9px solid transparent;
  transform: translateY(-50%);
}

/* 用户消息右对齐 */
.text-item-right {
  justify-content: flex-end;
}

.text-item-right .chat-name {
  order: 2;
}

.text-item-right .chat-box {
  margin-left: 0;
  margin-right: 12px;
  background: #d0edff;
  padding: 10px 15px; /* 添加内边距，增大文字与边框的间距 */
  border-radius: 12px; /* 可选：让气泡更圆润 */
}

/* 右侧对话气泡的箭头 */
.text-item-right .chat-box:before {
  right: -8px;
  border-left: 8px solid #d0edff;
  border-right: none;
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
  width: 70px;
  height: 70px;
}

h2 {
  font-size: 26px;
  font-family: Arial, Helvetica, sans-serif;
  color: #444;
  margin: 0;
}

.description {
  font-size: 15px;
  color: #666;
  margin-top: 10px;
}

.chat-box {
  font-family: Arial, sans-serif;
  line-height: 1.6;
}

.chat-box h1,
.chat-box h2,
.chat-box h3 {
  margin: 10px 0;
}

.chat-box pre {
  background: #f4f4f4;
  padding: 10px;
  border-radius: 5px;
  overflow-x: auto;
}

.chat-box code {
  background: #eee;
  padding: 2px 4px;
  border-radius: 3px;
}
</style>