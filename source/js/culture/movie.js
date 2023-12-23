$(document).ready(function () {
  // 如果存在元素.culture-list的div 元素，则执行以下代码
  if (document.querySelector('.movie-culture-list')) {
    // 定义滚动间隔时间和滚动阈值
    var scrollInterval = 300 // 滚动间隔时间，单位为毫秒
    var scrollThreshold = 200 // 滚动阈值，表示距离页面底部的距离，单位为像素
    // 每页加载的电影数量和当前页数
    var currentPage = 1
    // 当前页数
    var itemsPerPage = 12

    var jsonSrc = 'https://api.jaychou.site/trakt/movie'

    var coverSrc = 'https://image.tmdb.org/t/p/w116_and_h174_face'

    var init_data = ''
    // 如果SessionStorage中有init_data，则读取init_data
    if (sessionStorage.getItem('movie_init_data')) {
      init_data = sessionStorage.getItem('movie_init_data')
      sessionStorage.removeItem('movie_init_data')
    }

    // 定义滚动计时器
    var scrollTimer = null
    // 数据是否加载完毕
    data_ended = false
    // 获取元素.culture-list
    var cultureList = document.querySelector('.movie-culture-list')

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
      // 遍历 JSON 数据并生成对应的 <div> 元素
      jsonData.forEach(function (item) {
        // 创建 media 元素
        var media = document.createElement('div')
        media.classList.add('media')

        // 创建超链接 url为电影详情页  电影id为参数

        var url = '/culture/movies/detail/?tmdb_id=' + item.movie_id

        // 创建 media-cover 元素
        var mediaCover = document.createElement('div')
        mediaCover.classList.add('media-cover')
        // 如果share_link为空 则透明度为0.5
        if (item.share_link === '') {
          media.style.opacity = '0.5'
        }

        // mediaCover.style.backgroundImage =
        //   'url(' + coverSrc + item.cover_image_url + ')'

        // 创建图片元素
        var img = document.createElement('img')
        img.setAttribute('src', coverSrc + item.cover_image_url)
        img.setAttribute('data-src', coverSrc + item.cover_image_url)
        img.setAttribute('data-loaded', 'true')
        img.setAttribute('lazyload', '')
        img.setAttribute('srcset', '/img/loading.gif')
        mediaCover.appendChild(img)

        // 创建超链接 包围mediaCover
        var mediaCoverLink = document.createElement('a')
        mediaCoverLink.setAttribute('target', '_blank')
        mediaCoverLink.classList.add('media-cover-link')
        mediaCoverLink.setAttribute('href', url)
        mediaCoverLink.appendChild(mediaCover)

        media.appendChild(mediaCoverLink)

        // 创建 media-meta 元素
        var mediaMeta = document.createElement('div')
        mediaMeta.classList.add('media-meta')

        // 创建 title  元素
        var title = document.createElement('div')
        title.classList.add('media-meta-item', 'title')
        // 创建超链接 包围title
        var titleLink = document.createElement('a')
        titleLink.classList.add('title-link')
        titleLink.setAttribute('target', '_blank')
        titleLink.setAttribute('href', url)
        titleLink.textContent = item.movie_name
        title.appendChild(titleLink)

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
        for (const each of document.querySelectorAll('img[lazyload]')) {
          Fluid.utils.waitElementVisible(
            each,
            function () {
              each.removeAttribute('srcset')
              each.removeAttribute('lazyload')
            },
            CONFIG.lazyload.offset_factor
          )
        }
      })
    }

    //===================================================

    function simulateFetch(url) {
      return new Promise(function (resolve, reject) {
        // 模拟异步请求
        setTimeout(function () {
          // 模拟请求成功，并返回数据
          resolve({ data: '模拟的异步数据' })

          // 模拟请求失败
          // reject('请求失败');
        }, 0) // 模拟请求延迟2秒
      })
    }

    // 初始化加载
    if (init_data !== '') {
      // 使用模拟的异步请求
      simulateFetch('https://api.example.com/data')
        .then(function (response) {
          data = JSON.parse(init_data)
          // 如果数据为空，则返回
          if (data['data']['data'].length === 0) {
            hideLoadingAnimation()
            data_ended = true
          }
          generateMovieElements(data, coverSrc)
        })
        .catch(function (error) {
          // 处理请求失败的错误
          console.error('Error:', error)
        })
    } else {
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
          generateMovieElements(data, coverSrc)
        })
        .catch(function (error) {
          console.error('Error:', error)
        })
    }

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