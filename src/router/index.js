import { createRouter, createWebHistory } from "vue-router";
import MainContent from "@/components/MainContent.vue";

const routes = [
  {
    path: "/",
    name: "Main",
    component: MainContent, // 指向主页面组件
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
