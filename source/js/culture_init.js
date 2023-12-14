// 避免打开浏览器时 Culture 页面出现空白，先请求一次数据 建立SSL连接
// 如果SessionStorage中没有init_data，则初始化init_data
if (!sessionStorage.getItem('init_data')) {
  fetch('https://api.jaychou.site/common/init')
    .then(function (data) {
      sessionStorage.setItem('init_data', true)
    })
    .catch(function (error) {
      console.error('Error:', error)
    })
}
