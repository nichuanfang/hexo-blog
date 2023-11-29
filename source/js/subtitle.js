// var xhr = new XMLHttpRequest()
// xhr.open('GET', 'https://v2.jinrishici.com/one.json', true)
// // 添加请求头
// // xhr.setRequestHeader('Accept', 'application/json')
// // xhr.setRequestHeader('Content-Type', 'application/json')
// // xhr.setRequestHeader('X-User-Token', 'xNJL0fQDhPz3++IrWZte3QnBlkeSC+J/')
// xhr.onreadystatechange = function () {
//   if (xhr.readyState === 4 && xhr.status === 200) {
//     var data = JSON.parse(xhr.responseText)
//     console.log(data)
//     console.log(data.data.content) // 获取每日一句内容
//   }
// }
// xhr.send()

// fetch('https://v2.jinrishici.com/sentence', {
//   method: 'GET',
//   mode: 'cors', // 设置跨域请求模式
//   headers: {
//     'X-User-Token': 'xNJL0fQDhPz3++IrWZte3QnBlkeSC+J/',
//   },
// })
//   .then((response) => response.json())
//   .then((data) => {
//     // 处理返回的数据
//     console.log(data)
//     console.log(data.data.content) // 获取每日一句内容
//   })
//   .catch((error) => {
//     // 处理错误
//     console.error('Error:', error)
//   })
