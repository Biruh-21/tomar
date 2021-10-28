$(document).ready(function () {
    // CSRF protection used by django for POST requests
    var csrf_token = $("input[name=csrfmiddlewaretoken]").val()

    $(".bookmark-icon").off("click").on("click", function () {
        let $this = $(this); // clicked button
        let post_id = $this.val();

        $.ajax({
            method: "POST",
            url: "/bookmark/",
            data: {
                post_id: post_id,
                csrfmiddlewaretoken: csrf_token,
            },
            statusCode: {
                200: function (response) {
                    clicked_btn = $("button[value='" + response["button_val"] + "']")
                    if (response["is_bookmarked"] == true) {
                        $this.html('<i class="fas fa-bookmark fa-lg"></i>');
                    } else {
                        $this.html('<i class="far fa-bookmark fa-lg"></i>');
                    }
                },
                401: function (response) {
                    window.location.reload();
                }
            }
        })
    })

    // AJAX request for post like
    $(".like-btn").off("click").on("click", function () {
        let $this = $(this); // clicked button
        let post_id = $this.val();

        $.ajax({
            method: "POST",
            url: "/likes/",
            data: {
                post_id: post_id,
                csrfmiddlewaretoken: csrf_token,
            },
            statusCode: {
                200: function (response) {
                    if (response["is_liked"] == true) {
                        console.log(response)
                        $this.html('<i class="fas fa-thumbs-up fa-lg"></i>');
                    } else {
                        $this.html('<i class="far fa-thumbs-up fa-lg"></i>');
                    }
                },
                401: function (response) {
                    window.location.reload();
                }
            }
        })
    })
})