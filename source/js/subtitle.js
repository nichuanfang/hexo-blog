fetch('https://v2.jinrishici.com/one.json', {
  method: 'GET',
  mode: 'cors', // 设置跨域请求模式
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
    'X-User-Token': 'xNJL0fQDhPz3++IrWZte3QnBlkeSC+J/',
  },
})
  .then((response) => response.json())
  .then((data) => {
    // 处理返回的数据
    console.log(data)
    console.log(data.data.content) // 获取每日一句内容
  })
  .catch((error) => {
    // 处理错误
    console.error('Error:', error)
  })
