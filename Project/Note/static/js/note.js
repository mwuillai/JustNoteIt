$('#panel_button').click(function (e) {
    $('.dashboard-content').addClass('while');
    $('.navbar-brand').addClass('while');
    setTimeout(function() {
        $('.navbar-brand').toggleClass('hide');
    }, 300);
    setTimeout(function() {
        $('.dashboard-content').removeClass('while');
        $('.navbar-brand').removeClass('while');
    }, 1000);
    $('.dashboard-content').toggleClass('open');
    e.preventDefault();
});
