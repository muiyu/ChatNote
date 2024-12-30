# Vue 3 + Vite

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about IDE Support for Vue in the [Vue Docs Scaling up Guide](https://vuejs.org/guide/scaling-up/tooling.html#ide-support).


src/
├── components/
│   ├── Sidebar.vue        # 可复用的侧边栏组件
│   ├── ChatComponent.vue  # 智能问答组件
│   └── FileUpload.vue     # 文件上传组件
├── views/
│   ├── HomeView.vue       # 首页页面
│   ├── DashboardView.vue  # 仪表盘页面
├── router/
│   └── index.js           # 路由配置文件
├── App.vue                # 根组件，包含全局布局和 <router-view>
└── main.js                # 应用入口文件，挂载 Vue 应用
