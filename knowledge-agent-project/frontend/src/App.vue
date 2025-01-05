<template>
  <div id="app">
    <div class="container">
      <!-- 侧边栏 -->
      <Sidebar
        :conversations="conversations"
        :currentConversation="currentConversation"
        @select-conversation="selectConversation"
        @new-conversation="createNewConversation"
        @toggle-sidebar="toggleSidebar"
        :is-collapsed="isSidebarCollapsed"
      />

      <!-- 主内容区 -->
      <MainContent
        :currentConversation="currentConversation"
        @send-message="sendMessage"
      />
    </div>
  </div>
</template>

<script>
// import axios from 'axios';
import Sidebar from "@/components/SideBar.vue";
import MainContent from "@/components/MainContent.vue";

export default {
  data() {
    return {
      isSidebarCollapsed: false, 
      conversations: [], 
      currentConversation: null, 
    };
  },
  methods: {
    toggleSidebar() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed;
    },
    createNewConversation() {
      const newConversation = {
        id: Date.now(), 
        title: `新对话 ${this.conversations.length + 1}`, 
        messages: [], 
      };
      this.conversations.push(newConversation); 
      this.currentConversation = newConversation; 
    },

    selectConversation(conversation) {
      this.currentConversation = conversation; 
    },

    async sendMessage(message) {
      if (!this.currentConversation) {
        alert('请先新建对话！');
        return;
      }

      this.currentConversation.messages.push(message);
    },
  },
  components: {
    Sidebar,
    MainContent,
  },
};
</script>

<style scoped>
/* 整体容器样式 */
.container {
  display: flex; /* 使用 Flex 布局让 Sidebar 和 MainContent 横向排列 */
  height: 100vh; /* 占满整个视口高度 */
  overflow: hidden; /* 防止内容溢出 */
  padding: 0;
  margin: 0;
}

/* 侧边栏样式 */
.container > Sidebar {
  flex-shrink: 0; /* 保持侧边栏固定宽度，不缩小 */
}

/* 主内容区样式 */
.container > MainContent {
  flex-grow: 1; /* 让主内容区占据剩余空间 */
  background-color: #ffffff; /* 设置主内容区背景色为白色 */
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1); /* 添加左侧阴影，与侧边栏区分 */
  padding: 30px; /* 添加主内容区内部间距 */
  display: flex;
  flex-direction: column;
}
</style>