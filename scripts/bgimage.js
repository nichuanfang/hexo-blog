hexo.extend.filter.register('theme_inject', function (injects) {
  injects.bodyBegin.raw(
    'menhera',
    '<div id="background-image" style="display: none; left: 330.067px;"> <img src="/img/bg/bg01.png" alt="Background image"> </div>'
  )
})