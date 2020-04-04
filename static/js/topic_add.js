$(document).ready(function () {
    $('#submit-form-button').click(function () {
        form = $('#topic_add-form');
        if ($('input[name="title"]').val() !== ""){
            form.submit();
        }else {
            alert("Заголовок не может быть пустым")
        }
    });
});