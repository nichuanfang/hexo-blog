HTMLElement.prototype.wrap = function (e) {
  this.parentNode.insertBefore(e, this)
  this.parentNode.removeChild(this)
  e.appendChild(this)
}
Fluid.plugins = {
  typing: function (e) {
    if (!('Typed' in window)) {
      return
    }
    // 如果是首页 则设置e的内容为通过http请求获取的内容 请求的地址为https://v2.jinrishici.com/one.json
    if (window.location.pathname === '/') {
      fetch('https://v2.jinrishici.com/one.json', {
        method: 'GET',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
        },
      })
        // .then((response) => response.json())
        .then((data) => {
          // 处理返回的数据
          console.log(data)
          // e = data.data.content
        })
        .catch((error) => {
          // 处理错误
          console.error('Error:', error)
        })
    }
    var a = new window.Typed('#subtitle', {
      strings: ['  ', e],
      cursorChar: CONFIG.typing.cursorChar,
      typeSpeed: CONFIG.typing.typeSpeed,
      loop: CONFIG.typing.loop,
    })
    a.stop()
    var t = document.getElementById('subtitle')
    if (t) {
      t.innerText = ''
    }
    jQuery(document).ready(function () {
      a.start()
    })
  },
  fancyBox: function (e) {
    if (!CONFIG.image_zoom.enable || !('fancybox' in jQuery)) {
      return
    }
    jQuery(e || '.markdown-body :not(a) > img, .markdown-body > img').each(
      function () {
        var e = jQuery(this)
        var a = e.attr('data-src') || e.attr('src') || ''
        if (CONFIG.image_zoom.img_url_replace) {
          var t = CONFIG.image_zoom.img_url_replace
          var r = t[0] || ''
          var i = t[1] || ''
          if (r) {
            if (/^re:/.test(r)) {
              r = r.replace(/^re:/, '')
              var n = new RegExp(r, 'gi')
              a = a.replace(n, i)
            } else {
              a = a.replace(r, i)
            }
          }
        }
        var o = e
          .wrap(
            `
        <a class="fancybox fancybox.image" href="${a}"
          itemscope itemtype="http://schema.org/ImageObject" itemprop="url"></a>`
          )
          .parent('a')
        if (o.length !== 0) {
          if (e.is('.group-image-container img')) {
            o.attr('data-fancybox', 'group').attr('rel', 'group')
          } else {
            o.attr('data-fancybox', 'default').attr('rel', 'default')
          }
          var c = e.attr('title') || e.attr('alt')
          if (c) {
            o.attr('title', c).attr('data-caption', c)
          }
        }
      }
    )
    jQuery.fancybox.defaults.hash = false
    jQuery('.fancybox').fancybox({
      loop: true,
      helpers: {
        overlay: {
          locked: false,
        },
      },
    })
  },
  imageCaption: function (e) {
    if (!CONFIG.image_caption.enable) {
      return
    }
    jQuery(
      e ||
        `.markdown-body > p > img, .markdown-body > figure > img,
      .markdown-body > p > a.fancybox, .markdown-body > figure > a.fancybox`
    ).each(function () {
      var e = jQuery(this)
      var a = e.next('figcaption')
      if (a.length !== 0) {
        a.addClass('image-caption')
      } else {
        var t = e.attr('title') || e.attr('alt')
        if (t) {
          e.after(
            `<figcaption aria-hidden="true" class="image-caption">${t}</figcaption>`
          )
        }
      }
    })
  },
  codeWidget() {
    var r = CONFIG.code_language.enable && CONFIG.code_language.default
    var i = CONFIG.copy_btn && 'ClipboardJS' in window
    if (!r && !i) {
      return
    }
    function n(e) {
      return Fluid.utils.getBackgroundLightness(e) >= 0
        ? 'code-widget-light'
        : 'code-widget-dark'
    }
    var o = ''
    o += '<div class="code-widget">'
    o += 'LANG'
    o += '</div>'
    jQuery('.markdown-body pre').each(function () {
      var e = jQuery(this)
      if (e.find('code.mermaid').length > 0) {
        return
      }
      if (e.find('span.line').length > 0) {
        return
      }
      var a = ''
      if (r) {
        a = CONFIG.code_language.default
        if (
          e[0].children.length > 0 &&
          e[0].children[0].classList.length >= 2 &&
          e.children().hasClass('hljs')
        ) {
          a = e[0].children[0].classList[1]
        } else if (e[0].getAttribute('data-language')) {
          a = e[0].getAttribute('data-language')
        } else if (
          e.parent().hasClass('sourceCode') &&
          e[0].children.length > 0 &&
          e[0].children[0].classList.length >= 2
        ) {
          a = e[0].children[0].classList[1]
          e.parent().addClass('code-wrapper')
        } else if (
          e.parent().hasClass('markdown-body') &&
          e[0].classList.length === 0
        ) {
          e.wrap('<div class="code-wrapper"></div>')
        }
        a = a.toUpperCase().replace('NONE', CONFIG.code_language.default)
      }
      e.append(
        o
          .replace('LANG', a)
          .replace(
            'code-widget">',
            n(e[0]) +
              (i
                ? ' code-widget copy-btn" data-clipboard-snippet><i class="iconfont icon-copy"></i>'
                : ' code-widget">')
          )
      )
      if (i) {
        var t = new ClipboardJS('.copy-btn', {
          target: function (e) {
            var a = e.parentNode.childNodes
            for (var t = 0; t < a.length; t++) {
              if (a[t].tagName === 'CODE') {
                return a[t]
              }
            }
          },
        })
        t.on('success', function (e) {
          e.clearSelection()
          e.trigger.innerHTML = e.trigger.innerHTML.replace(
            'icon-copy',
            'icon-success'
          )
          setTimeout(function () {
            e.trigger.innerHTML = e.trigger.innerHTML.replace(
              'icon-success',
              'icon-copy'
            )
          }, 2e3)
        })
      }
    })
  },
}