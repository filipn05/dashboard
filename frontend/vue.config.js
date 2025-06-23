const { defineConfig } = require('@vue/cli-service')
// vue.config.js
module.exports = {
  devServer: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
      }
    }
  }
}
