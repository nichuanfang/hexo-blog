hexo.extend.filter.register('theme_inject', function (injects) {
  injects.bodyEnd.raw(
    'menhera',
    `
        <% if (theme.background_image.enable) { %>
            <div id="background-image">
                <img src="<%= theme.background_image.src %>" alt="Background image">
            </div>
        <% } %>
    `
  )
})
