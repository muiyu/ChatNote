<template>
  <div :class="['sidebar', { collapsed: isCollapsed }]">
    <div class="header">
      <div class="logo" v-if="!isCollapsed">
        <span class="project-name"> LearnSailor </span>
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
    conversations: Array,
    currentConversation: Object,
    isCollapsed: Boolean,
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
</style>