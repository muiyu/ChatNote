// vue.config.js
const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  // 配置 Webpack
  configureWebpack: {
    resolve: {
      alias: {
        vue$: 'vue/dist/vue.esm-bundler.js', // 设置 Vue 的别名
      },
    },
  },

  // 使用 chainWebpack 自定义配置
  chainWebpack: (config) => {
    config.plugin('define').tap((definitions) => {
      Object.assign(definitions[0], {
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: 'false', // 设置 Vue 的特性标志
      });
      return definitions;
    });
  },

  // 开发服务器配置
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // 后端服务地址
        changeOrigin: true, // 允许跨域
        pathRewrite: { '^/api': '' }, // 重写路径，去掉 /api 前缀
      },
    },
  },
});