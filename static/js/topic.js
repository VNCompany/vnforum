$(document).ready(function () {
    $('.btn-vote-user').click(function () {
        let value;
        if ($(this).hasClass("fa-b-up")){
             value = "plus";
        }else {
            value = "minus";
        }
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
                $('#vv-' + id).html(val.value);
            }
            else
                alert(val.message);
        })
    });


    $('.btn-vote-post').click(function () {
        let value;
        if ($(this).hasClass("fa-b-up")){
             value = "plus";
        }else {
            value = "minus";
        }
        let id = $(this).attr("id").toString().split('-')[1];
        $.ajax({
            type: "POST",
            url: "/ajax/vote",
            data: {
                "uid": id,
                "value": value,
                "type": "vote_post"
            }
        }).done(function (msg) {
            let val = JSON.parse(msg);
            if (val.status === "ok") {
                $('#pr-' + id).html(val.value);
            }
            else
                alert(val.message);
        })
    });
});
