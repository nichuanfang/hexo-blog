// // 等待文档加载完成
// $(document).ready(function () {
//   // 获取背景图像元素
//   var backgroundImage = jQuery('#background-image')
//   // 如果背景图像元素不存在，则返回
//   if (backgroundImage.length === 0) {
//     return
//   }
//   // 获取board元素
//   var board = jQuery('#board')
//   // 如果board元素不存在，则返回
//   if (board.length === 0) {
//     return
//   }
//   // 定义posDisplay和scrollDisplay变量，用于控制背景图像的显示
//   var posDisplay = false
//   var scrollDisplay = false
//   // 定义setBackgroundImagePos函数，用于设置背景图像的位置
//   var setBackgroundImagePos = function () {
//     // 获取board元素的左边距
//     var boardLeft = board[0].getClientRects()[0].left
//     // 根据左边距是否大于等于50来决定是否显示背景图像
//     posDisplay = boardLeft >= 50
//     // 设置背景图像的display和left属性
//     backgroundImage.css({
//       display: posDisplay && scrollDisplay ? 'block' : 'none',
//       left: boardLeft - 136 + 'px',
//     })
//   }
//   // 调用setBackgroundImagePos函数
//   setBackgroundImagePos()
//   // 在窗口大小调整时重新调用setBackgroundImagePos函数
//   jQuery(window).resize(setBackgroundImagePos)
//   // 获取board元素的顶部偏移量
//   var headerHeight = board.offset().top
//   // 监听页面滚动事件
//   Fluid.utils.listenScroll(function () {
//     // 获取滚动高度
//     var scrollHeight =
//       document.body.scrollTop + document.documentElement.scrollTop
//     // 根据滚动高度是否大于等于headerHeight来决定是否显示背景图像
//     scrollDisplay = scrollHeight >= headerHeight
//     // 设置背景图像的display属性
//     backgroundImage.css({
//       display: posDisplay && scrollDisplay ? 'block' : 'none',
//     })
//   })
// })
