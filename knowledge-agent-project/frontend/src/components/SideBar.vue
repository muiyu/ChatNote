<template>
  <div :class="['sidebar', { collapsed: isCollapsed }]">
    <div class="header">
      <!-- 项目名称 -->
      <div class="logo" v-if="!isCollapsed">
        <span class="project-name">Mentor</span>
      </div>
      <!-- 收起/展开按钮 -->
      <button class="toggle-btn" @click="$emit('toggle-sidebar')">
        <img
          class="toggle-icon"
          :src="isCollapsed ? openIcon : closeIcon"
        />
      </button>
    </div>

    <!-- 开启新对话按钮 -->
    <button class="new-conversation" @click="$emit('new-conversation')">
      <img class="new-conversation-icon" :src="addConverIcon" alt="开启新对话" />
      <!-- 文字只在展开时显示 -->
      <span v-if="!isCollapsed">开启新对话</span>
    </button>

    <!-- 对话列表（仅在展开状态下显示） -->
    <ul class="conversation-list" v-if="!isCollapsed">
      <li
        v-for="conversation in conversations"
        :key="conversation.id"
        :class="{ active: conversation === currentConversation }"
        @click="$emit('select-conversation', conversation)"
      >
        {{ conversation.title }}
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
    conversations: {
      type: Array,
      required: true,
    },
    currentConversation: {
      type: Object,
      required: false,
    },
    isCollapsed: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      openIcon,
      closeIcon,
      addConverIcon,
    };
  },
};
</script>




<style scoped>
.sidebar {
  width: 200px; /* 展开时宽度 */
  background-color: #f2fafd; /* 浅蓝色背景 */
  color: gray; /* 灰色文字 */
  display: flex;
  flex-direction: column;
  padding: 10px;
  border-radius: 10px 0 0 10px;
  transition: width 0.3s ease;
  overflow: hidden; /* 防止内容溢出 */
}

.sidebar.collapsed {
  width: 60px; /* 收起时宽度 */
  align-items: center; /* 内容居中对齐 */
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between; /* 左边项目名称，右边按钮 */
  margin-bottom: 20px;
  width: 100%; /* 确保内容宽度适应侧边栏 */
}

.logo {
  display: flex;
  align-items: center;
}

.project-name {
  font-size: 25px; /* 项目名称字体大小 */
  font-weight: bold;
  color: #444;
  font-family: Georgia, 'Times New Roman', Times, serif;
}

.toggle-btn {
  background-color: transparent; /* 背景透明 */
  border: none; /* 去掉按钮默认边框 */
  cursor: pointer;
  padding: 8px; /* 调整按钮的点击范围 */
  display: flex;
  align-items: center;
  justify-content: center;
}

.toggle-btn:hover {
  background-color: #ececec; /* 悬停时的背景颜色 */
  border-radius: 35%; /* 圆形按钮效果 */
}

.toggle-icon {
  width: 24px; /* 收起/展开图标宽度 */
  height: 24px; /* 收起/展开图标高度 */
}

.new-conversation {
  margin-bottom: 20px;
  background-color: #d0edff; /* 按钮背景 */
  color: #6375dd;
  border: none;
  padding: 12px; /* 内边距 */
  border-radius: 20px; /* 圆角半径 */
  cursor: pointer;
  text-align: left; /* 文字左对齐 */
  font-size: 17px; /* 按钮文字大小 */
  display: flex; /* 图标和文字水平排列 */
  align-items: center; /* 图标和文字垂直居中 */
  gap: 8px; /* 图标和文字之间的间距 */
  width: fit-content; /* 按钮宽度包裹内容 */
}

.new-conversation-icon {
  width: 24px; /* 开启新对话图标宽度 */
  height: 24px; /* 开启新对话图标高度 */
  vertical-align: middle; /* 图标与文字对齐 */
}

.new-conversation:hover {
  background-color: #c4e5f3; /* 按钮悬停效果 */
}

.conversation-list {
  list-style: none;
  padding: 0;
  margin: 0;
  width: 100%; /* 确保宽度对齐侧边栏 */
}

.conversation-list li {
  cursor: pointer;
  padding: 10px;
  border-radius: 10px;
  color: rgb(0, 0, 0); /* 对话列表默认文字颜色 */
  text-align: left; /* 列表文字左对齐 */
  transition: background-color 0.3s ease; /* 平滑过渡效果 */
}

.conversation-list li:hover {
  background-color: #e6f7ff; /* 悬停时更浅的背景 */
}

.conversation-list li.active {
  background-color: #b3e5fc; /* 选中状态的背景颜色 */
}
</style>
