# 知识库代理项目前端文档

## 项目概述
该项目是一个基于LangChain的知识库代理应用，包含前端和后端两个部分。前端使用React框架构建，后端使用Flask框架提供API服务。

## 前端结构
- `src/App.js`：前端应用的入口点，设置React应用并配置路由。
- `src/components/KnowledgeAgent.js`：展示知识库代理的界面，并处理用户输入。
- `src/services/api.js`：与后端API交互的函数，发送用户查询并获取代理的响应。
- `src/styles/main.css`：前端应用的样式定义。

## 安装与运行
1. 确保已安装Node.js和npm。
2. 在`frontend`目录下运行以下命令安装依赖：
   ```
   npm install
   ```
3. 启动开发服务器：
   ```
   npm start
   ```
4. 打开浏览器访问 `http://localhost:3000` 查看应用。

## 使用说明
用户可以在知识库代理界面输入查询，系统将通过后端API与知识库代理进行交互，并返回相应的结果。

## 贡献
欢迎提交问题和拉取请求，以帮助改进该项目。请遵循项目的贡献指南。

## 许可证
该项目遵循MIT许可证。