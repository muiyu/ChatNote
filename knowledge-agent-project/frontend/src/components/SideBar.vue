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
  width: 200px;
  background-color: #f2fafd;
  padding: 10px;
  transition: width 0.3s;
}

.sidebar.collapsed {
  width: 60px;
}

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.project-name {
  font-size: 25px;
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
  padding: 12px;
  border-radius: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.new-conversation-icon {
  width: 24px;
}

.conversation-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.conversation-list li {
  padding: 10px;
  border-radius: 10px;
  transition: background-color 0.3s;
}

.conversation-list li:hover {
  background-color: #e6f7ff;
}

.conversation-list li.active {
  background-color: #b3e5fc;
}
</style>
