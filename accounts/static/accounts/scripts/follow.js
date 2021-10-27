$(document).ready(function () {
    // CSRF protection used by django for POST requests
    var csrf_token = $("input[name=csrfmiddlewaretoken]").val();

    $(".follow-btn").off("click").on("click", function () {
        user_id = $(this).val();

        $.ajax({
            type: "POST",
            url: "/accounts/follow/",
            data: {
                "user_id": user_id,
                csrfmiddlewaretoken: csrf_token,
            },
            success: function (response) {
                console.log(response);
                follow_btn = $(".follow-btn");
                if (response["following"] == true) {
                    follow_btn.html('Following');
                    follow_btn.attr("class", "btn btn-outline-primary follow follow-btn");
                } else {
                    follow_btn.html('Follow');
                    follow_btn.attr("class", "btn btn-primary follow follow-btn");
                }
            }
        })
    });
});