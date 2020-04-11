$(document).ready(function () {
    $(".vote-btn").click(function () {
        let value = $(this).hasClass("vote-up") ? "plus" : "minus";
        let id = $(this).attr("id").toString().split('-')[1];
        $.ajax({
            type: "POST",
            url: "/ajax/vote",
            data: {
                "uid": id,
                "value": value,
                "type": "vote_user"
            }
        }).done(function (msg) {
            let val = JSON.parse(msg);
            if (val.status === "ok") {
                $("#rating").html(val.value);
            } else
                alert(val.message);
        })
    });
});