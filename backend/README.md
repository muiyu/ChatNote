# 后端知识库代理项目

该项目是一个基于LangChain的知识库代理，包含前后端应用。后端使用Flask框架，前端使用React框架。

## 目录结构

```
knowledge-agent-project
├── backend
│   ├── app.py                # 后端应用入口
│   ├── agents
│   │   ├── knowledge_agent.py # 知识库代理实现
│   │   └── agent_with_graph.py # 使用图数据库
│   ├── services
│   │   ├── deepseek_v2_langchain.py # LangChain服务实现
│   │   └── graph_rag.py # 使用图增强搜索
│   ├── requirements.txt           # Python依赖项
│   └── README.md                  # 后端文档
├── frontend
│   ├── node_modules
│   ├── public
│   ├── src
│   │   ├── assets # 一些图标素材
│   │   ├── components # 主要功能组件
│   │   │   ├── ChatBox.vue
│   │   │   ├── InputBar.vue
│   │   │   ├── KnowledgeAgent.vue
│   │   │   ├── MainContent.vue
│   │   │   ├── SideBar.vue
│   │   │   └── App.vue
│   │   ├── main.js
│   │   ├── style.css
│   │   └── .gitignore
│   ├── .npmrc
│   ├── babel.config.js
│   ├── jsconfig.json
│   ├── package-lock.json
│   ├── package.json
│   └── README.md
└── README.md                       # 项目总体文档
```

## 安装依赖

在后端目录下运行以下命令安装依赖：

```
pip install -r requirements.txt
```

## 导入服务 API KEY
```
source ~/api-key.src
```
格式应该类似于
```
export OPENAI_API_KEY=xxx
export OPENAI_BASE_URL=xxx
export NEO4J_URI=xxx
export NEO4J_USERNAME=xxx
export NEO4J_PASSWORD=xxx
```

## 运行后端服务

在后端目录下，运行以下命令启动Flask应用：

```
python app.py
```

## 使用说明

后端服务启动后，可以通过指定的API端点与知识库代理进行交互。

## 贡献

欢迎任何形式的贡献！请提交问题或拉取请求。