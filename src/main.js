import { createApp } from 'vue'
import './style.css'; // 引入全局样式文件
import App from './App.vue'
import router from "./router"; // 引入路由配置

// 创建 Vue 应用实例，并挂载插件和路由
const app = createApp(App);

// 使用路由
app.use(router);

// 挂载到 DOM 元素
app.mount('#app');
