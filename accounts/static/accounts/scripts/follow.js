$(document).ready(function () {
    // CSRF protection used by django for POST requests
    let csrf_token = $("input[name=csrfmiddlewaretoken]").val();

    $(".follow-btn").off("click").on("click", function () {
        let $this = $(this);
        let user_id = $this.val();

        $.ajax({
            method: "POST",
            url: "/accounts/follow/",
            data: {
                "user_id": user_id,
                csrfmiddlewaretoken: csrf_token,
            },
            statusCode: {
                200: function (response) {
                    if (response["following"] == true) {
                        $this.html('Following');
                        $this.attr("class", "btn btn-outline-primary follow follow-btn");
                    } else {
                        $this.html('Follow');
                        $this.attr("class", "btn btn-primary follow follow-btn");
                    }
                },
                401: function (response) {
                    window.location.reload();
                }
            }
        })
    });
});