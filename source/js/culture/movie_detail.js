// 电影详情
$(document).ready(function () {
  if (document.querySelector('#movie-detail-container')) {
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

    // 验证 URL 是否有效
    function isValidUrl(url) {
      const pattern = /^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$/i
      return pattern.test(url)
    }
    // 获取window.location.search中的tmdb_id
    var tmdb_id = window.location.search.split('=')[1]

    // 从https://api.jaychou.site/trakt/movie/{tmdb_id}获取数据

    var movieData = {}
    $.ajax({
      url: 'https://api.jaychou.site/trakt/movie/' + tmdb_id,
      type: 'GET',
      dataType: 'json',
      async: false,
      success: function (data) {
        movieData = data.data
      },
      error: function (error) {
        console.log(error)
      },
    })

    // 计算评分
    stars = convertToStars(movieData.rating)
    if (movieData.share_link == '') {
      target_placeholder = ''
      open_link = '#'
    } else {
      target_placeholder = 'target="_blank"'
      open_link = movieData.share_link
    }

    // 创建并设置电影详情的 HTML 结构
    var movieDetailHTML = `
        <div class="movie-detail-media">
        <a target="_blank" class="movie-detail-media-cover-link" href="https://www.themoviedb.org/movie/${movieData.movie_id}">
            <div class="movie-detail-media-cover" style="background-image: url('https://www.themoviedb.org/t/p/w300_and_h450_bestv2${movieData.cover_image_url}');"></div>
        </a>
        <div class="movie-detail-media-meta">
            <div class="movie-detail-media-meta-item title">
            <a class="title-link" target="_blank" href="https://www.themoviedb.org/movie/${movieData.movie_id}">${movieData.movie_name}</a>
            </div>
            <div class="movie-detail-media-meta-item">
            <span class="author">${movieData.area} ${movieData.release_year}</span>
            <span class="star-score">${stars[0]}<span class="grey-star">${stars[1]}</span></span>
            <span class="link"><a href="${open_link}" ${target_placeholder}><i class="fas fa-external-link-alt"></i>打开</a></span>
            <span class="copy"><a href="#"><i class="fas fa-copy"></i>复制</a></span>
            <span class="edit"><a href="#"><i class="fas fa-edit"></i>更新</a></span>
            </div>
            <div class="movie-detail-media-meta-item intro-title">剧情简介</div>
            <div class="movie-detail-media-meta-item intro">
            ${movieData.movie_description}
            </div>
        </div>
        </div>
    `
    // 将电影详情添加到页面中
    var movieDetailContainer = document.getElementById('movie-detail-container')
    movieDetailContainer.innerHTML = movieDetailHTML

    // 获取 open_link 元素
    const openLinkElement = document.querySelector('.link a')

    //处理复制
    // 获取复制按钮元素
    var copyButton = document.querySelector(
      '.movie-detail-media-meta-item .copy a'
    )

    // 检查 open_link 是否为空
    if (openLinkElement.getAttribute('href') == '#') {
      // 如果 open_link 为空，则将 .copy 和 .link 元素置灰
      copyButton.classList.add('disabled')
      openLinkElement.classList.add('disabled')
      // 设置样式 灰色
      // TODO  更新链接之后 需要将样式改回来
      copyButton.style.color = '#999'
      openLinkElement.style.color = '#999'
    }

    let isCopyInProgress = false // 标志变量，指示复制操作是否正在进行中
    let copyTimer // 用于存储定时器的变量

    // 添加复制事件监听器
    copyButton.addEventListener('click', async (event) => {
      event.preventDefault() // 阻止超链接的默认跳转行为

      if (open_link != '#') {
        try {
          if (isCopyInProgress) {
            return // 如果复制操作正在进行中，不执行任何操作
          }
          // 使用 Clipboard API 将文本内容复制到剪贴板
          await navigator.clipboard.writeText(open_link)

          // 取消之前的定时器
          clearTimeout(copyTimer)

          // 保存原始的 copyButton 内容
          const originalButtonText = copyButton.innerHTML

          copyButton.innerHTML = '已复制<i class="fas fa-check"></i>'
          copyButton.style.color = 'green'
          // 设置标志变量为 true，表示复制操作正在进行中
          isCopyInProgress = true
          // 1秒后还原 copyButton 的文本和颜色
          copyTimer = setTimeout(() => {
            copyButton.innerHTML = originalButtonText
            copyButton.style.color = '' // 还原 copyButton 文本颜色

            // 设置标志变量为 false，表示复制操作已完成
            isCopyInProgress = false
          }, 1000)
        } catch (err) {
          console.error('复制到剪贴板失败:', err)
        }
      }
    })

    // 获取 editButton 元素
    const editButton = document.querySelector(
      '.movie-detail-media-meta-item .edit a'
    )

    // 添加编辑事件监听器
    editButton.addEventListener('click', (event) => {
      event.preventDefault() // 阻止超链接的默认跳转行为

      // 创建编辑框元素
      const inputBox = document.createElement('div')
      inputBox.className = 'input-box'
      inputBox.style.position = 'fixed'
      inputBox.style.top = '50%'
      inputBox.style.left = '50%'
      inputBox.style.transform = 'translate(-50%, -50%)'
      inputBox.style.backgroundColor = '#607D8B'
      inputBox.style.padding = '20px'
      inputBox.style.border = '1px solid #212529'
      inputBox.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.2)'
      inputBox.style.zIndex = '9999'
      inputBox.style.width = '400px'

      // 创建输入框元素
      const input = document.createElement('input')
      input.type = 'text'
      input.placeholder = '请输入URL'
      input.style.width = '100%'
      input.style.marginBottom = '10px'
      inputBox.appendChild(input)

      // 创建确认按钮元素
      const confirmButton = document.createElement('button')
      confirmButton.textContent = '确认'
      confirmButton.style.float = 'right'
      inputBox.appendChild(confirmButton)

      // 创建取消按钮元素
      const cancelButton = document.createElement('button')
      cancelButton.textContent = '取消'
      cancelButton.style.float = 'right'
      cancelButton.style.marginRight = '10px'
      inputBox.appendChild(cancelButton)

      // 添加编辑框到页面中
      document.body.appendChild(inputBox)

      // 将光标聚焦到输入框
      input.focus()

      // 点击确认按钮的事件处理程序
      confirmButton.addEventListener('click', () => {
        const url = input.value
        if (!isValidUrl(url)) {
          input.placeholder = 'URL无效!'
          input.value = ''
          input.focus()
        } else {
          document.body.removeChild(inputBox)
          // 保存原始的 editButton 内容
          const originalButtonText = editButton.innerHTML

          // 将 editButton 的文本更改为 "√已更新" 和图标
          editButton.innerHTML = '已更新 <i class="fas fa-check"></i>'
          editButton.style.color = 'green' // 设置 editButton 文本颜色为绿色

          // 1秒后还原 editButton 的文本、颜色和图标
          setTimeout(() => {
            editButton.innerHTML = originalButtonText
            editButton.style.color = '' // 还原 editButton 文本颜色
          }, 1000)
          // 检查 inputBox 是否存在，然后再移除
          if (inputBox && inputBox.parentNode) {
            inputBox.parentNode.removeChild(inputBox)
          }
          // 更新打开链接和复制链接的 href 属性 以及还原样式
          openLinkElement.setAttribute('href', url)
          openLinkElement.classList.remove('disabled')
          openLinkElement.style.color = ''
          // openLink设置target="_blank"
          openLinkElement.setAttribute('target', '_blank')
          copyButton.classList.remove('disabled')
          copyButton.style.color = ''
          //  更新open_link
          open_link = url
        }
      })

      // 点击取消按钮的事件处理程序
      cancelButton.addEventListener('click', () => {
        // 移除编辑框
        document.body.removeChild(inputBox)
      })

      // 输入框的键盘事件处理程序
      input.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
          confirmButton.click() // 模拟点击确认按钮
          event.preventDefault() // 阻止回车键的默认行为
        }
      })
    })
  }
})
