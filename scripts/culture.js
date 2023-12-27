hexo.extend.filter.register('theme_inject', function (injects) {
  injects.head.raw(
    'culture_init',
    '<script src="/js/culture_init.js"></script>'
  )
  injects.head.raw('movie', '<script src="/js/culture/movie.js"></script>')
  injects.head.raw(
    'movie_detail',
    '<script src="/js/culture/movie_detail.js"></script>'
  )
})