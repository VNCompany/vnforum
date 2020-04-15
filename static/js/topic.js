$(document).ready(function () {
    $('.btn-vote-user').click(function () {
        let vote_btn = $(this);
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
                let parent = vote_btn.parent().children(".prop-v");
                parent.html(val.value);
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

    $('.post_send-btn').click(function () {
        let topic_id = $('#d-topic_id').attr("data-tid");
        $.ajax({
            type: "post",
            url: "/ajax/topic/" + topic_id + "/add_post",
            data: {
                "content": $("#editor").val()
            }
        }).done(function (msg) {
            if (msg !== "ok")
                alert(msg);
            else{
                document.location.reload();
                let pos = $("#editor-block").offset().top;
                $(document).scrollTop(pos);
            }
        })
    });
});
