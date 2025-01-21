# 使用官方 Node.js 镜像
FROM node:16-slim

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 package-lock.json
COPY package.json package-lock.json ./

# 安装依赖
RUN npm install

# 复制前端代码
COPY . .

# 构建前端应用
RUN npm run build

# 暴露端口
EXPOSE 8080

# 启动前端应用
CMD ["npm", "run", "serve"]