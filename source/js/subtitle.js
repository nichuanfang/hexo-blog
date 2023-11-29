var xhr = new XMLHttpRequest()
xhr.open('GET', 'https://v2.jinrishici.com/one.json', true)
xhr.onreadystatechange = function () {
  if (xhr.readyState === 4 && xhr.status === 200) {
    var data = JSON.parse(xhr.responseText)
    console.log(data)
    console.log(data.data.content) // 获取每日一句内容
  }
}
xhr.send()
