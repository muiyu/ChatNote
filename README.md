# 知识库代理项目

该项目是一个基于LangChain的知识库代理应用，包含前端和后端两个部分。

## 项目结构

```
knowledge-agent-project
├── backend
│   ├── src
│   │   ├── app.py                # 后端应用入口点
│   │   ├── agents
│   │   │   └── knowledge_agent.py # 知识库代理类
│   │   ├── services
│   │   │   └── langchain_service.py # LangChain服务类
│   │   └── utils
│   │       └── helpers.py        # 辅助函数
│   ├── requirements.txt           # 后端依赖项
│   └── README.md                  # 后端文档
├── frontend
│   ├── src
│   │   ├── App.js                 # 前端应用入口点
│   │   ├── components
│   │   │   └── KnowledgeAgent.js  # 知识库代理组件
│   │   ├── services
│   │   │   └── api.js             # API交互函数
│   │   └── styles
│   │       └── main.css           # 前端样式
│   ├── package.json                # 前端配置文件
│   └── README.md                   # 前端文档
└── README.md                       # 项目总体文档
```

## 安装与运行

### 后端

1. 进入后端目录：
   ```
   cd backend
   ```

2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

3. 运行后端应用：
   ```
   python src/app.py
   ```

### 前端

1. 进入前端目录：
   ```
   cd frontend
   ```

2. 安装依赖：
   ```
   npm install
   ```

3. 运行前端应用：
   ```
   npm start
   ```

## 使用说明

- 前端应用提供了一个用户界面，用户可以输入查询并与知识库代理进行交互。
- 后端应用处理来自前端的请求，并使用LangChain进行知识库查询。

## 贡献

欢迎任何形式的贡献！请提交问题或拉取请求。