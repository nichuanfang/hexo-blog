$(document).ready(function () {
  // 如果存在元素.culture-list的div 元素，则执行以下代码
  if (document.querySelector('.movie-culture-list')) {
    // 定义每页加载的电影数量和当前页数
    var currentPage = 1
    var itemsPerPage = 12
    // 定义滚动间隔时间和滚动阈值
    var scrollInterval = 300 // 滚动间隔时间，单位为毫秒
    var scrollThreshold = 200 // 滚动阈值，表示距离页面底部的距离，单位为像素

    // 定义滚动计时器
    var scrollTimer = null
    // 数据是否加载完毕
    data_ended = false
    // 获取元素.culture-list
    var cultureList = document.querySelector('.movie-culture-list')
    // 获取元素.culture-list的json-src属性值
    var jsonSrc = cultureList.getAttribute('json-src')
    // 获取元素.culture-list的cover-src属性值
    var coverSrc = cultureList.getAttribute('cover-src')

    //======================函数部分=============================

    // 显示加载动画
    function showLoadingAnimation() {
      document.getElementById('loading').style.display = 'block'
    }

    // 隐藏加载动画
    function hideLoadingAnimation() {
      document.getElementById('loading').style.display = 'none'
    }

    // 将10分制评分(带小数)转换为5分制评分(带小数)  并转换为星星表示
    function convertToStars(rating) {
      var num = parseFloat(rating) / 2
      // 如果4.3分以上 也是五星
      if (num > 4.3) {
        num = 5
      }
      var fullStar = parseInt(num)
      var halfStar = num - fullStar
      var noStar = 5 - fullStar - Math.ceil(halfStar)
      var star = ''
      var grey_star = ''
      for (var i = 0; i < fullStar; i++) {
        star += '★'
      }
      for (var i = 0; i < halfStar; i++) {
        // 半颗星
        star += '☆'
      }
      for (var i = 0; i < noStar; i++) {
        // 空星
        grey_star += '☆'
      }
      return [star, grey_star]
    }

    // 对jsonData进行排序 按照last_watched_at降序排列
    function sortJsonData(jsonData) {
      jsonData.sort(function (a, b) {
        return b.last_watched_at - a.last_watched_at
      })
      return jsonData
    }

    // 发起异步请求获取下一页的 json 数据的函数
    function fetchNextPage(currentPage, itemsPerPage) {
      // 根据实际情况拼接下一页的 json-src
      var nextJsonSrc =
        jsonSrc + '?page=' + currentPage + '&page_size=' + itemsPerPage

      fetch(nextJsonSrc)
        .then(function (response) {
          return response.json()
        })
        .then(function (data) {
          // 如果数据为空，则返回
          if (data['data']['data'].length === 0) {
            hideLoadingAnimation()
            data_ended = true
          }
          // 根据下一页的 json 数据生成子节点
          generateMovieElements(data, coverSrc)
          // 隐藏加载动画
          hideLoadingAnimation()
        })
        .catch(function (error) {
          console.error('Error:', error)
        })
    }

    // 生成子节点的函数
    function generateMovieElements(data, coverSrc) {
      // 假设你的 JSON 数据是一个包含多个电影的数组，每个电影对象都有相应的属性
      var jsonData = data['data']['data']

      // 获取目标容器元素
      var container = document.querySelector('.movie-culture-list')
      jsonData = sortJsonData(jsonData)
      // 遍历 JSON 数据并生成对应的 <div> 元素
      jsonData.forEach(function (item) {
        // 创建 media 元素
        var media = document.createElement('div')
        media.classList.add('media')

        // 创建 media-cover 元素
        var mediaCover = document.createElement('div')
        mediaCover.classList.add('media-cover')
        mediaCover.style.backgroundImage =
          'url(' + coverSrc + item.cover_image_url + ')'
        media.appendChild(mediaCover)

        // 创建 media-meta 元素
        var mediaMeta = document.createElement('div')
        mediaMeta.classList.add('media-meta')

        // 创建 title 元素
        var title = document.createElement('div')
        title.classList.add('media-meta-item', 'title')
        title.textContent = item.movie_name
        mediaMeta.appendChild(title)

        // 创建元信息元素
        var meta = document.createElement('div')
        meta.classList.add('media-meta-item')

        // 创建作者和评分元素
        var authorSpan = document.createElement('span')
        authorSpan.classList.add('author')
        // 地区
        area = item.area
        // 发布时间
        release_year = item.release_year

        authorSpan.textContent = area + ' ' + release_year
        meta.appendChild(authorSpan)

        var starScoreSpan = document.createElement('span')
        starScoreSpan.classList.add('star-score')

        star = convertToStars(item.rating)[0]
        grey_star = convertToStars(item.rating)[1]
        starScoreSpan.textContent = star

        // 创建starScoreSpan的grey_starSpan元素
        var grey_starSpan = document.createElement('span')
        grey_starSpan.classList.add('grey-star')
        grey_starSpan.textContent = grey_star
        starScoreSpan.appendChild(grey_starSpan)

        meta.appendChild(starScoreSpan)

        mediaMeta.appendChild(meta)

        // 创建 intro 元素
        var intro = document.createElement('div')
        intro.classList.add('media-meta-item', 'intro')
        intro.textContent = item.movie_description
        mediaMeta.appendChild(intro)

        // 将生成的子元素添加到 media 元素中
        media.appendChild(mediaMeta)

        // 将 media 元素添加到目标容器中
        container.appendChild(media)
      })
    }

    //===================================================

    // 初始化加载
    // 发起异步请求获取第一页的 json 数据
    fetch(jsonSrc + '?page=' + currentPage + '&page_size=' + itemsPerPage)
      .then(function (response) {
        return response.json()
      })
      .then(function (data) {
        // 如果数据为空，则返回
        if (data['data']['data'].length === 0) {
          hideLoadingAnimation()
          data_ended = true
        }
        // 根据第一页的 json 数据生成子节点
        generateMovieElements(data, coverSrc)
      })
      .catch(function (error) {
        console.error('Error:', error)
      })

    // 监听滚动事件
    window.addEventListener('scroll', function () {
      if (data_ended) {
        hideLoadingAnimation()
        return
      }
      // 清除之前的滚动计时器
      clearTimeout(scrollTimer)

      // 计算滚动到页面底部的距离
      var distanceToBottom =
        document.documentElement.scrollHeight -
        window.innerHeight -
        window.scrollY

      // 检查是否滚动到页面底部
      if (distanceToBottom <= scrollThreshold) {
        // 显示加载动画
        showLoadingAnimation()
        // 设置滚动计时器，延迟一定时间后执行函数
        scrollTimer = setTimeout(function () {
          // 发起异步请求获取下一页的 json 数据
          currentPage++
          // 加载下一页的电影数据
          if (!data_ended) {
            fetchNextPage(currentPage, itemsPerPage)
          }
        }, scrollInterval)
      }
    })
  }
})
