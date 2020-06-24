$(document).ready(function () {
    const $image = $("#user-avatar");
    const $fileInput = $("#id_avatar");
    let $editorImage = $("#editor-image");
    let cropBoxData;
    let canvasData;

    // Clear file so change event can fire if user selects same file again.
    $fileInput.click(function() {
        $(this).prop('value', '');
    });

    // Send file to server and update template img src with new url once saved.
    $fileInput.change(function () {
        if (this.files && this.files[0]) {
            let file = this.files[0];
            let form = new FormData();
            let uploadAvatarUrl = $(this).data('url');
            // set label
            let fileName = $(this).val().split("\\").pop();
            $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
            form.append('file', file);

            $.ajax({
                type: 'POST',
                url: uploadAvatarUrl,
                data: form,
                dataType: 'json',
                contentType: false,
                processData: false,
                success: function (data) {
                    if (data['is_valid']) {
                        $image.attr('src', data['url']);
                    } else {
                        console.log(data['errors']);
                    }
                },
            });
        }
    });

    // Show modal when edit button is clicked.
    $("#open-editor-btn").click(function (e) {
        if ($image.attr('src') !== '') {
            $editorImage.attr('src', $image.attr('src'));
            $("#modal-crop").modal("show");
        }
        e.preventDefault();
    });

    // Initialize image cropper when modal is shown.
    $("#modal-crop").on("shown.bs.modal", function () {
        $editorImage.cropper({
            viewMode: 2,
            aspectRatio: 1 / 1,
            minCropBoxWidth: 200,
            minCropBoxHeight: 200,
            ready: function () {
                $editorImage.cropper("setCanvasData", canvasData);
                $editorImage.cropper("setCropBoxData", cropBoxData);
            }
        });
    }).on("hidden.bs.modal", function () {
        cropBoxData = $editorImage.cropper("getCropBoxData");
        canvasData = $editorImage.cropper("getCanvasData");
        $editorImage.cropper("destroy");
    });

    $(".js-zoom-in").click(function () {
        $editorImage.cropper("zoom", 0.1);
    });

    $(".js-zoom-out").click(function () {
        $editorImage.cropper("zoom", -0.1);
    });
    $(".js-rotate-right").click(function () {
        $editorImage.cropper("rotate", 45);
    });
    $(".js-rotate-left").click(function () {
        $editorImage.cropper("rotate", -45);
    });

    /**
     * Sends image data and url to server to be processed and saved as
     * the user's avatar. Updates template img src with new url when finished.
     */
    $(".js-crop-and-upload").click(function () {
        let cropData = $editorImage.cropper("getData");
        let saveImageUrl = $image.data('url');

        $.ajax({
            url: saveImageUrl,
            type: "POST",
            data: {
                src: $editorImage.attr('src'),
                x: cropData['x'],
                y: cropData['y'],
                height: cropData['height'],
                width: cropData['width'],
                rotate: cropData['rotate'],
            },
            dataType: "json",
            success: function (data, status, jqXHR) {
                $image.attr('src', data.url);
                $('#modal-crop').modal('hide');
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });

    /* CSRF setup for AJAX */
//     function getCookie(name) {
//         let cookieValue = null;
//         if (document.cookie && document.cookie !== '') {
//             let cookies = document.cookie.split(';');
//             for (let i = 0; i < cookies.length; i++) {
//                 let cookie = cookies[i].trim();
//                 // Does this cookie string begin with the name we want?
//                 if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                     break;
//                 }
//             }
//         }
//         return cookieValue;
//     }
//
//     function csrfSafeMethod(method) {
//         // these HTTP methods do not require CSRF protection
//         return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
//     }
//
//     const csrftoken = getCookie('csrftoken');
//
//     $.ajaxSetup({
//         beforeSend: function (xhr, settings) {
//             if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//                 xhr.setRequestHeader("X-CSRFToken", csrftoken);
//             }
//         }
//     });
});