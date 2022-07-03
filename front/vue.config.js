//const { defineConfig } = require('@vue/cli-service')

module.exports = ({
  //transpileDependencies: true,
  lintOnSave:false,
  devServer: {
    proxy: 'http://124.71.169.200:5000'
  },
  configureWebpack: {
    externals: {
      'BMap': 'BMap',
      'BMap_Symbol_SHAPE_POINT': 'BMap_Symbol_SHAPE_POINT'
    }
  }
  // devServer: {
  //   proxy: {
  //       '/pm': {
  //           target: 'http://localhost:5000',
  //           pathRewrite:{'^/pm':''},
  //           // ws: true, //用于支持websocket,默认值为true
  //           // changeOrigin: true //用于控制请求头中的host值,默认值为true
  //       }
  //   }
  // }
})
