$(document).ready(function () {
    $('.js-btn-apply').on('click', function () {
        let positionId = $(this).data('id');

        $.ajax({
            url: `/positions/apply/${positionId}/`,
            type: 'post',
            dataType: 'json',
            success: function (data) {
                $(`.js-btn-apply[data-id=${positionId}]`).addClass("disabled").text('Applied')
            }
        });
    });
});
