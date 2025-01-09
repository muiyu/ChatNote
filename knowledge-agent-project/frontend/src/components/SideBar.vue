<template>
  <div :class="['sidebar', { collapsed: isCollapsed }]">
    <div class="header">
      <div class="logo" v-if="!isCollapsed">
        <span class="project-name"> FunnyGo </span>
      </div>
      <button class="toggle-btn" @click="$emit('toggle-sidebar')">
        <img class="toggle-icon" :src="isCollapsed ? openIcon : closeIcon" />
      </button>
    </div>

    <button class="new-conversation" @click="$emit('new-conversation')">
      <img class="new-conversation-icon" :src="addConverIcon" alt="开启新对话" />
      <span v-if="!isCollapsed">开启新对话</span>
    </button>

    <ul class="conversation-list" v-if="!isCollapsed">
      <li
        v-for="(conversation, index) in conversations"
        :key="conversation.id"
        :class="{ active: conversation === currentConversation }"
      >
        <!-- {{ conversation.title }} -->
        <div class="conversation-item">
          <span @click="$emit('select-conversation', conversation)">{{ conversation.title }}</span>
          <!-- 操作按钮 -->
          <div class="dropdown">
            <button class="dropdown-btn" @click.stop="toggleDropdown(index)">
              ...
            </button>
            <!-- 下拉框 -->
            <div v-if="activeDropdown === index" class="dropdown-menu">
              <button @click.stop="$emit('rename-conversation', conversation)">重命名</button>
              <button @click.stop="$emit('deleteConversation', conversation)">删除</button>
            </div>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import openIcon from '@/assets/open.svg';
import closeIcon from '@/assets/close.svg';
import addConverIcon from '@/assets/addconver.svg';

export default {
  props: {
    conversations: Array,
    currentConversation: Object,
    isCollapsed: Boolean,
  },
  data() {
    return {
      openIcon,
      closeIcon,
      addConverIcon,
      activeDropdown: null, // 当前打开下拉框的索引
    };
  },
  methods: {
    toggleDropdown(index) {
      // 切换下拉框的显示状态
      this.activeDropdown = this.activeDropdown === index ? null : index;
      this.$forceUpdate(); // 强制重新渲染，确保更新
    },
    renameConversation(conversation) {
      // 重命名对话
      const newTitle = prompt('请输入新的对话名称：', conversation.title);
      if (newTitle) {
        this.$emit('rename-conversation', { ...conversation, title: newTitle });
      }
      setTimeout(() => {
        this.activeDropdown = null; // 延迟关闭下拉框
      }, 0);
    },
    deleteConversation(conversation) {
      // 删除对话
      if (confirm(`确定要删除对话 "${conversation.title}" 吗？`)) {
        this.$emit('delete-conversation', conversation);
      }
      setTimeout(() => {
        this.activeDropdown = null; // 延迟关闭下拉框
      }, 0);
    },
  },
};
</script>

<style scoped>
.sidebar {
  width: 240px;
  background-color: #f2fafd;
  padding: 10px;
  transition: width 0.3s;
  border-radius: 0 15px 15px 0;
}

.sidebar.collapsed {
  width: 45px;
}

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.project-name {
  font-size: 25px;
  font-family:'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
  font-weight: bold;
}

.toggle-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
}

.toggle-icon {
  width: 24px;
}

.new-conversation {
  background-color: #d0edff;
  color: #6375dd;
  border: none;
  padding: 10px;
  border-radius: 15px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 17px;
  margin-bottom: 20px;
}

.new-conversation:hover {
  background-color: #b3d9ff; /* 鼠标悬停时的背景颜色 */
}

.new-conversation-icon {
  width: 28px;
}

.conversation-list {
  list-style:none;
  padding: 0;
  margin: 0;
}

.conversation-list li {
  padding: 10px;
  border-radius: 12px;
  transition: background-color 0.3s;
  margin-bottom: 8px;
}

.conversation-list li:hover {
  background-color: #e6f7ff;
}

.conversation-list li.active {
  background-color: #c7e9f9;
}

.conversation-item {
  display: flex;
  justify-content: space-between; /* 标题和按钮分隔两侧 */
  align-items: center;
}

/* 下拉按钮样式 */
.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-btn {
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  padding: 5px;
}

.dropdown-btn:hover {
  background-color: #e6f7ff;
  border-radius: 50%;
}

/* 下拉菜单样式 */
.dropdown-menu {
  position: absolute;
  right: 0;
  top: 100%;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  display: flex;
  flex-direction: column; /* 竖向排列 */
}

.dropdown-menu button {
  background: none;
  border: none;
  padding: 10px 15px;
  cursor: pointer;
  white-space: nowrap; /* 禁止换行 */
  width: 100%; /* 宽度占满菜单 */
}

.dropdown-menu button:hover {
  background-color: #f0f8ff;
  border-radius: 8px;
}

</style>