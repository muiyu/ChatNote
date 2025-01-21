# ChatNote
基于 LangChain 框架构建的本地知识库问答程序，包含前端和后端两个部分。

## Tips
**本项目同时作为课程《云计算课程》的结课项目，由本小组成员保留最终解释权。**

## 安装与运行
分别进入前端和后端的目录，跟随 README 文件执行即可。

## 使用说明
- 前端应用提供了一个用户界面，用户可以输入查询并与知识库代理进行交互。
- 后端应用处理来自前端的请求，并使用LangChain进行知识库查询。

前端和后端以镜像形式部署在了GitHub Container Registry，访问yaoximiao成员的Packages可以获取(已处于Public)。

拉取后端
```python
docker pull ghcr.io/myusername/chatnote_backend:latest
```
拉取前端
```python 
docker pull ghcr.io/myusername/chatnote_frontend:latest
```
且在github的仓库的docker分支中yaoximiao分享了docker-compose.yml, （推荐）可以使用它一键启动项目，只需运行以下代码
```python 
docker-compose up
```


## 贡献
欢迎任何形式的贡献！请提交问题或拉取请求。
