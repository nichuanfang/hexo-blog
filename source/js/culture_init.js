// 避免打开浏览器时 Culture 页面出现空白，先请求一次数据 建立SSL连接
// 如果SessionStorage中没有init_data且inited不存在，则初始化init_data

// 如果当前是culture/*页面 才执行以下代码
if (
  window.location.pathname.indexOf('/culture/') != -1 &&
  !sessionStorage.getItem('movie_init_data')
) {
  fetch('https://api.jaychou.site/trakt/movie?page=1&page_size=12')
    .then(function (response) {
      return response.json()
    })
    .then(function (data) {
      if (data['data']['data'].length != 0) {
        sessionStorage.setItem('movie_init_data', JSON.stringify(data))
      }
    })
    .catch(function (error) {
      console.error('Error:', error)
    })
}
