const { defineConfig } = require('@vue/cli-service')


module.exports = defineConfig({
  devServer: {
    proxy: {    //配置跨域
      "/api": {         //当检测到url中有/api,则进行跨域处理
        target: "http://127.0.0.1:8000/",    //填写项目请求接口地址
        changeOrigin: true,      //允许跨域
        pathRewrite: {
          "^/api": "",    // 重写路径，将url中的/api，取消（这样，/api起到识别触发作用）
        },
      },
    },
  },
})
