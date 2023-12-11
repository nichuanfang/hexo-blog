hexo.extend.filter.register('theme_inject', function (injects) {
  injects.bodyBegin.raw(
    'menhera',
    '<div id="background-image" style="display: none; left: 330.067px;"> <img src="/img/bg/bg01.png" alt="Background image"> </div>'
  )
  injects.head.raw(
    'font-awesome',
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">'
  )
})
