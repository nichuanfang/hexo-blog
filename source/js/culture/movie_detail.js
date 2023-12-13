// 电影详情
$(document).ready(function () {
  if (document.querySelector('#movie-detail-container')) {
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
            <span class="star-score">${movieData.rating}<span class="grey-star">☆</span></span>
            <span class="link"><a href="#"><i class="fas fa-external-link-alt"></i>打开</a></span>
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
  }
})
