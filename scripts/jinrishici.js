hexo.extend.filter.register('theme_inject', function (injects) {
  injects.bodyBegin.raw(
    'menhera',
    '<span id="jinrishici-sentence">正在加载今日诗词....</span> <script src="https://sdk.jinrishici.com/v2/browser/jinrishici.js" charset="utf-8"></script>'
  )
})
