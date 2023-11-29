/** @license
 * DHTML Snowstorm! JavaScript-based snow for web pages
 * Making it snow on the internets since 2003. You're welcome.
 * -----------------------------------------------------------
 * Version 1.44.20131215 (Previous rev: 1.44.20131208)
 * Copyright (c) 2007, Scott Schiller. All rights reserved.
 * Code provided under the BSD License
 * http://schillmania.com/projects/snowstorm/license.txt
 */
var snowStorm = (function (e, t) {
  this.autoStart = true
  this.excludeMobile = true
  this.flakesMax = 128
  this.flakesMaxActive = 64
  this.animationInterval = 24
  this.useGPU = true
  this.className = null
  this.flakeBottom = null
  this.followMouse = true
  this.snowColor = '#fff'
  this.snowCharacter = '&bull;'
  this.snowStick = true
  this.targetElement = null
  this.useMeltEffect = true
  this.useTwinkleEffect = false
  this.usePositionFixed = false
  this.usePixelPosition = false
  this.accessibility = true
  this.freezeOnBlur = false
  this.flakeLeftOffset = 0
  this.flakeRightOffset = 0
  this.flakeWidth = 8
  this.flakeHeight = 8
  this.vMaxX = 3
  this.vMaxY = 2
  this.zIndex = 0
  var i = this,
    s,
    l = navigator.userAgent.match(/msie/i),
    n = navigator.userAgent.match(/msie 6/i),
    a = navigator.userAgent.match(/mobile|opera m(ob|in)/i),
    o = l && t.compatMode === 'BackCompat',
    r = o || n,
    f = null,
    m = null,
    h = null,
    u = null,
    c = null,
    d = null,
    v = null,
    y = 1,
    p = 0.6,
    k = 6,
    g = false,
    x = false,
    b = (function () {
      try {
        t.createElement('div').style.opacity = '0.5'
      } catch (e) {
        return false
      }
      return true
    })(),
    w = false,
    F = t.createDocumentFragment()
  s = (function () {
    var s
    function l(t) {
      e.setTimeout(t, 1e3 / (i.animationInterval || 20))
    }
    var n =
      e.requestAnimationFrame ||
      e.webkitRequestAnimationFrame ||
      e.mozRequestAnimationFrame ||
      e.oRequestAnimationFrame ||
      e.msRequestAnimationFrame ||
      l
    s = n
      ? function () {
          return n.apply(e, arguments)
        }
      : null
    var a
    a = t.createElement('div')
    function o(e) {
      var t = a.style[e]
      return t !== undefined ? e : null
    }
    var r = {
      transform: {
        ie: o('-ms-transform'),
        moz: o('MozTransform'),
        opera: o('OTransform'),
        webkit: o('webkitTransform'),
        w3: o('transform'),
        prop: null,
      },
      getAnimationFrame: s,
    }
    r.transform.prop =
      r.transform.w3 ||
      r.transform.moz ||
      r.transform.webkit ||
      r.transform.ie ||
      r.transform.opera
    a = null
    return r
  })()
  this.timer = null
  this.flakes = []
  this.disabled = false
  this.active = false
  this.meltFrameCount = 20
  this.meltFrames = []
  this.setXY = function (e, t, s) {
    if (!e) {
      return false
    }
    if (i.usePixelPosition || x) {
      e.style.left = t - i.flakeWidth + 'px'
      e.style.top = s - i.flakeHeight + 'px'
    } else if (r) {
      e.style.right = 100 - (t / f) * 100 + '%'
      e.style.top = Math.min(s, c - i.flakeHeight) + 'px'
    } else {
      if (!i.flakeBottom) {
        e.style.right = 100 - (t / f) * 100 + '%'
        e.style.bottom = 100 - (s / h) * 100 + '%'
      } else {
        e.style.right = 100 - (t / f) * 100 + '%'
        e.style.top = Math.min(s, c - i.flakeHeight) + 'px'
      }
    }
  }
  this.events = (function () {
    var t = !e.addEventListener && e.attachEvent,
      i = Array.prototype.slice,
      s = {
        add: t ? 'attachEvent' : 'addEventListener',
        remove: t ? 'detachEvent' : 'removeEventListener',
      }
    function l(e) {
      var s = i.call(e),
        l = s.length
      if (t) {
        s[1] = 'on' + s[1]
        if (l > 3) {
          s.pop()
        }
      } else if (l === 3) {
        s.push(false)
      }
      return s
    }
    function n(e, i) {
      var l = e.shift(),
        n = [s[i]]
      if (t) {
        l[n](e[0], e[1])
      } else {
        l[n].apply(l, e)
      }
    }
    function a() {
      n(l(arguments), 'add')
    }
    function o() {
      n(l(arguments), 'remove')
    }
    return { add: a, remove: o }
  })()
  function E(e, t) {
    if (isNaN(t)) {
      t = 0
    }
    return Math.random() * e + t
  }
  function z(e) {
    return parseInt(E(2), 10) === 1 ? e * -1 : e
  }
  this.randomizeWind = function () {
    var e
    d = z(E(i.vMaxX, 0.2))
    v = E(i.vMaxY, 0.2)
    if (this.flakes) {
      for (e = 0; e < this.flakes.length; e++) {
        if (this.flakes[e].active) {
          this.flakes[e].setVelocities()
        }
      }
    }
  }
  this.scrollHandler = function () {
    var s
    u = i.flakeBottom
      ? 0
      : parseInt(
          e.scrollY ||
            t.documentElement.scrollTop ||
            (r ? t.body.scrollTop : 0),
          10
        )
    if (isNaN(u)) {
      u = 0
    }
    if (!g && !i.flakeBottom && i.flakes) {
      for (s = 0; s < i.flakes.length; s++) {
        if (i.flakes[s].active === 0) {
          i.flakes[s].stick()
        }
      }
    }
  }
  this.resizeHandler = function () {
    if (e.innerWidth || e.innerHeight) {
      f = e.innerWidth - 16 - i.flakeRightOffset
      h = i.flakeBottom || e.innerHeight
    } else {
      f =
        (t.documentElement.clientWidth ||
          t.body.clientWidth ||
          t.body.scrollWidth) -
        (!l ? 8 : 0) -
        i.flakeRightOffset
      h =
        i.flakeBottom ||
        t.documentElement.clientHeight ||
        t.body.clientHeight ||
        t.body.scrollHeight
    }
    c = t.body.offsetHeight
    m = parseInt(f / 2, 10)
  }
  this.resizeHandlerAlt = function () {
    f = i.targetElement.offsetWidth - i.flakeRightOffset
    h = i.flakeBottom || i.targetElement.offsetHeight
    m = parseInt(f / 2, 10)
    c = t.body.offsetHeight
  }
  this.freeze = function () {
    if (!i.disabled) {
      i.disabled = 1
    } else {
      return false
    }
    i.timer = null
  }
  this.resume = function () {
    if (i.disabled) {
      i.disabled = 0
    } else {
      return false
    }
    i.timerInit()
  }
  this.toggleSnow = function () {
    if (!i.flakes.length) {
      i.start()
    } else {
      i.active = !i.active
      if (i.active) {
        i.show()
        i.resume()
      } else {
        i.stop()
        i.freeze()
      }
    }
  }
  this.stop = function () {
    var s
    this.freeze()
    for (s = 0; s < this.flakes.length; s++) {
      this.flakes[s].o.style.display = 'none'
    }
    i.events.remove(e, 'scroll', i.scrollHandler)
    i.events.remove(e, 'resize', i.resizeHandler)
    if (i.freezeOnBlur) {
      if (l) {
        i.events.remove(t, 'focusout', i.freeze)
        i.events.remove(t, 'focusin', i.resume)
      } else {
        i.events.remove(e, 'blur', i.freeze)
        i.events.remove(e, 'focus', i.resume)
      }
    }
  }
  this.show = function () {
    var e
    for (e = 0; e < this.flakes.length; e++) {
      this.flakes[e].o.style.display = 'block'
    }
  }
  this.SnowFlake = function (e, l, n) {
    var a = this
    this.type = e
    this.x = l || parseInt(E(f - 20), 10)
    this.y = !isNaN(n) ? n : -E(h) - 12
    this.vX = null
    this.vY = null
    this.vAmpTypes = [1, 1.2, 1.4, 1.6, 1.8]
    this.vAmp = this.vAmpTypes[this.type] || 1
    this.melting = false
    this.meltFrameCount = i.meltFrameCount
    this.meltFrames = i.meltFrames
    this.meltFrame = 0
    this.twinkleFrame = 0
    this.active = 1
    this.fontSize = 10 + (this.type / 5) * 10
    this.o = t.createElement('div')
    this.o.innerHTML = i.snowCharacter
    if (i.className) {
      this.o.setAttribute('class', i.className)
    }
    this.o.style.color = i.snowColor
    this.o.style.position = g ? 'fixed' : 'absolute'
    if (i.useGPU && s.transform.prop) {
      this.o.style[s.transform.prop] = 'translate3d(0px, 0px, 0px)'
    }
    this.o.style.width = i.flakeWidth + 'px'
    this.o.style.height = i.flakeHeight + 'px'
    this.o.style.fontFamily = 'arial,verdana'
    this.o.style.cursor = 'default'
    this.o.style.overflow = 'hidden'
    this.o.style.fontWeight = 'normal'
    this.o.style.zIndex = i.zIndex
    if (i.accessibility) {
      this.o.setAttribute('aria-hidden', i.accessibility)
    }
    F.appendChild(this.o)
    this.refresh = function () {
      if (isNaN(a.x) || isNaN(a.y)) {
        return false
      }
      i.setXY(a.o, a.x, a.y)
    }
    this.stick = function () {
      if (
        r ||
        (i.targetElement !== t.documentElement && i.targetElement !== t.body)
      ) {
        a.o.style.top = h + u - i.flakeHeight + 'px'
      } else if (i.flakeBottom) {
        a.o.style.top = i.flakeBottom + 'px'
      } else {
        a.o.style.display = 'none'
        a.o.style.top = 'auto'
        a.o.style.bottom = '0%'
        a.o.style.position = 'fixed'
        a.o.style.display = 'block'
      }
    }
    this.vCheck = function () {
      if (a.vX >= 0 && a.vX < 0.2) {
        a.vX = 0.2
      } else if (a.vX < 0 && a.vX > -0.2) {
        a.vX = -0.2
      }
      if (a.vY >= 0 && a.vY < 0.2) {
        a.vY = 0.2
      }
    }
    this.move = function () {
      var e = a.vX * y,
        t
      a.x += e
      a.y += a.vY * a.vAmp
      if (a.x >= f || f - a.x < i.flakeWidth) {
        a.x = 0
      } else if (e < 0 && a.x - i.flakeLeftOffset < -i.flakeWidth) {
        a.x = f - i.flakeWidth - 1
      }
      a.refresh()
      t = h + u - a.y + i.flakeHeight
      if (t < i.flakeHeight) {
        a.active = 0
        if (i.snowStick) {
          a.stick()
        } else {
          a.recycle()
        }
      } else {
        if (
          i.useMeltEffect &&
          a.active &&
          a.type < 3 &&
          !a.melting &&
          Math.random() > 0.998
        ) {
          a.melting = true
          a.melt()
        }
        if (i.useTwinkleEffect) {
          if (a.twinkleFrame < 0) {
            if (Math.random() > 0.97) {
              a.twinkleFrame = parseInt(Math.random() * 8, 10)
            }
          } else {
            a.twinkleFrame--
            if (!b) {
              a.o.style.visibility =
                a.twinkleFrame && a.twinkleFrame % 2 === 0
                  ? 'hidden'
                  : 'visible'
            } else {
              a.o.style.opacity =
                a.twinkleFrame && a.twinkleFrame % 2 === 0 ? 0 : 1
            }
          }
        }
      }
    }
    this.animate = function () {
      a.move()
    }
    this.setVelocities = function () {
      a.vX = d + E(i.vMaxX * 0.12, 0.1)
      a.vY = v + E(i.vMaxY * 0.12, 0.1)
    }
    this.setOpacity = function (e, t) {
      if (!b) {
        return false
      }
      e.style.opacity = t
    }
    this.melt = function () {
      if (!i.useMeltEffect || !a.melting) {
        a.recycle()
      } else {
        if (a.meltFrame < a.meltFrameCount) {
          a.setOpacity(a.o, a.meltFrames[a.meltFrame])
          a.o.style.fontSize =
            a.fontSize - a.fontSize * (a.meltFrame / a.meltFrameCount) + 'px'
          a.o.style.lineHeight =
            i.flakeHeight +
            2 +
            i.flakeHeight * 0.75 * (a.meltFrame / a.meltFrameCount) +
            'px'
          a.meltFrame++
        } else {
          a.recycle()
        }
      }
    }
    this.recycle = function () {
      a.o.style.display = 'none'
      a.o.style.position = g ? 'fixed' : 'absolute'
      a.o.style.bottom = 'auto'
      a.setVelocities()
      a.vCheck()
      a.meltFrame = 0
      a.melting = false
      a.setOpacity(a.o, 1)
      a.o.style.padding = '0px'
      a.o.style.margin = '0px'
      a.o.style.fontSize = a.fontSize + 'px'
      a.o.style.lineHeight = i.flakeHeight + 2 + 'px'
      a.o.style.textAlign = 'center'
      a.o.style.verticalAlign = 'baseline'
      a.x = parseInt(E(f - i.flakeWidth - 20), 10)
      a.y = parseInt(E(h) * -1, 10) - i.flakeHeight
      a.refresh()
      a.o.style.display = 'block'
      a.active = 1
    }
    this.recycle()
    this.refresh()
  }
  this.snow = function () {
    var e = 0,
      t = null,
      l,
      n
    for (l = 0, n = i.flakes.length; l < n; l++) {
      if (i.flakes[l].active === 1) {
        i.flakes[l].move()
        e++
      }
      if (i.flakes[l].melting) {
        i.flakes[l].melt()
      }
    }
    if (e < i.flakesMaxActive) {
      t = i.flakes[parseInt(E(i.flakes.length), 10)]
      if (t.active === 0) {
        t.melting = true
      }
    }
    if (i.timer) {
      s.getAnimationFrame(i.snow)
    }
  }
  this.mouseMove = function (e) {
    if (!i.followMouse) {
      return true
    }
    var t = parseInt(e.clientX, 10)
    if (t < m) {
      y = -p + (t / m) * p
    } else {
      t -= m
      y = (t / m) * p
    }
  }
  this.createSnow = function (e, t) {
    var s
    for (s = 0; s < e; s++) {
      i.flakes[i.flakes.length] = new i.SnowFlake(parseInt(E(k), 10))
      if (t || s > i.flakesMaxActive) {
        i.flakes[i.flakes.length - 1].active = -1
      }
    }
    i.targetElement.appendChild(F)
  }
  this.timerInit = function () {
    i.timer = true
    i.snow()
  }
  this.init = function () {
    var s
    for (s = 0; s < i.meltFrameCount; s++) {
      i.meltFrames.push(1 - s / i.meltFrameCount)
    }
    i.randomizeWind()
    i.createSnow(i.flakesMax)
    i.events.add(e, 'resize', i.resizeHandler)
    i.events.add(e, 'scroll', i.scrollHandler)
    if (i.freezeOnBlur) {
      if (l) {
        i.events.add(t, 'focusout', i.freeze)
        i.events.add(t, 'focusin', i.resume)
      } else {
        i.events.add(e, 'blur', i.freeze)
        i.events.add(e, 'focus', i.resume)
      }
    }
    i.resizeHandler()
    i.scrollHandler()
    if (i.followMouse) {
      i.events.add(l ? t : e, 'mousemove', i.mouseMove)
    }
    i.animationInterval = Math.max(20, i.animationInterval)
    i.timerInit()
  }
  this.start = function (s) {
    if (!w) {
      w = true
    } else if (s) {
      return true
    }
    if (typeof i.targetElement === 'string') {
      var l = i.targetElement
      i.targetElement = t.getElementById(l)
      if (!i.targetElement) {
        throw new Error('Snowstorm: Unable to get targetElement "' + l + '"')
      }
    }
    if (!i.targetElement) {
      i.targetElement = t.body || t.documentElement
    }
    if (i.targetElement !== t.documentElement && i.targetElement !== t.body) {
      i.resizeHandler = i.resizeHandlerAlt
      i.usePixelPosition = true
    }
    i.resizeHandler()
    i.usePositionFixed = i.usePositionFixed && !r && !i.flakeBottom
    if (e.getComputedStyle) {
      try {
        x =
          e
            .getComputedStyle(i.targetElement, null)
            .getPropertyValue('position') === 'relative'
      } catch (e) {
        x = false
      }
    }
    g = i.usePositionFixed
    if (f && h && !i.disabled) {
      i.init()
      i.active = true
    }
  }
  function H() {
    e.setTimeout(function () {
      i.start(true)
    }, 20)
    i.events.remove(l ? t : e, 'mousemove', H)
  }
  function M() {
    if (!i.excludeMobile || !a) {
      H()
    }
    i.events.remove(e, 'load', M)
  }
  if (i.autoStart) {
    i.events.add(e, 'load', M, false)
  }
  return this
})(window, document)
