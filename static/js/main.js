$(document).ready(function () {
    $('*').click(function () {
        let popup = $("#profile-popup");
        if (!popup.hasClass("popup-hidden")) {
            popup.animate({
                height: 1
            }, 100, function () {
                popup.css({ display: "none" }).addClass("popup-hidden");
            });
        }
    });

    $('#profile-btn').click(function () {
        let popup = $("#profile-popup");
        if (popup.hasClass("popup-hidden")) {
            popup.css({ display: "block" }).animate({
                height: popup_height
            }, 100, function () {
                popup.removeClass("popup-hidden")
            });
        }
    });
});