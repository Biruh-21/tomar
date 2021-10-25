$(document).ready(function () {

    // CSRF protection used by django for POST requests
    var csrf_token = $("input[name=csrfmiddlewaretoken]").val()

    $(".bookmark-icon").off("click").on("click", function () {
        var post_id = $(this).val();

        $.ajax({
            type: "POST",
            url: "bookmark/",
            data: {
                post_id: post_id,
                csrfmiddlewaretoken: csrf_token,
            },
            success: function (response) {
                // var clicked_btn = [].filter.call(document.getElementsByTagName("button"), function (button) {
                //     return button.value === response["button_val"];
                // });
                clicked_btn = $("button[value='" + response["button_val"] + "']")
                if (response["is_bookmarked"] == true) {
                    clicked_btn.html('<i class="fas fa-bookmark fa-lg"></i>')
                } else {
                    clicked_btn.html('<i class="far fa-bookmark fa-lg"></i>')
                }
            }
        })
    })
})