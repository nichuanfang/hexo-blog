// 电影详情
$(document).ready(function () {
  if (document.querySelector('#movie-detail-container')) {
    // 假设获取到的 JSON 结果为 movieData
    var movieData = {
      title: '侏罗纪公园2：失落的世界',
      year: '1997',
      starScore: '★★★☆',
      intro:
        '当年在努布拉岛营建侏罗纪公园时，约翰•哈蒙德（理查德•阿滕伯勒 Richard Attenborough 饰）曾把附近的索纳岛作为恐龙的制造工场。侏罗纪公园沦陷后，索纳岛上的恐龙在完全隔绝且缺少必要合成元素的情况下生存了4年时间。哈蒙德对此颇感好奇，他重新找到马科姆博士（杰夫•高布伦 Jeff Goldblum 饰），邀请他前往小岛考察。4年前经历让马科姆心有余悸，他断然拒绝哈蒙德的提议，但当得知女友莎拉（朱丽安•摩尔 Julianne Moore 饰）已前往小岛之时',
      coverImage:
        'https://www.themoviedb.org/t/p/w300_and_h450_bestv2/uiaXGh35oTmcgPx4EYcLFiR8nfX.jpg',
      movieUrl: 'https://www.themoviedb.org/movie/330',
    }

    // 创建并设置电影详情的 HTML 结构
    var movieDetailHTML = `
        <div class="movie-detail-media">
        <a target="_blank" class="movie-detail-media-cover-link" href="${movieData.movieUrl}">
            <div class="movie-detail-media-cover" style="background-image: url('${movieData.coverImage}');"></div>
        </a>
        <div class="movie-detail-media-meta">
            <div class="movie-detail-media-meta-item title">
            <a class="title-link" target="_blank" href="${movieData.movieUrl}">${movieData.title}</a>
            </div>
            <div class="movie-detail-media-meta-item">
            <span class="author">美国 ${movieData.year}</span>
            <span class="star-score">${movieData.starScore}<span class="grey-star">☆</span></span>
            <span class="link"><a href="#"><i class="fas fa-external-link-alt"></i>打开链接</a></span>
            <span class="copy"><a href="#"><i class="fas fa-copy"></i>复制链接</a></span>
            <span class="edit"><a href="#"><i class="fas fa-edit"></i>更新链接</a></span>
            </div>
            <div class="movie-detail-media-meta-item intro-title">剧情简介</div>
            <div class="movie-detail-media-meta-item intro">
            ${movieData.intro}
            </div>
        </div>
        </div>
    `
    // 将电影详情添加到页面中
    var movieDetailContainer = document.getElementById('movie-detail-container')
    movieDetailContainer.innerHTML = movieDetailHTML
  }
})
