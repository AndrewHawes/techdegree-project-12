$(document).ready(function () {
    let filters = {status: 'all', project: 'all', position: 'all'};

    function filterApplications() {
        $('.js-application-row').each(function() {
            let filtered = false;

            for (let filter in filters) {
                if (filters[filter] === 'all') {

                } else if ($(this).data(filter) !== filters[filter]) {
                    filtered = true;
                }
            }
            if (filtered === true) {
                $(this).addClass('d-none');
            } else {
                $(this).removeClass('d-none');
            }
        });
    }

    $('.js-filter .nav-link').on('click', function() {
        let filter = $(this).data('filter');
        filters[filter] = $(this).data(filter);
        filterApplications();
    });
});

$('.js-btn-accept').on('click', function () {
    let applicationId = $(this).data('id');
    $.ajax({
        url: `/applications/accept/${applicationId}/`,
        type: 'post',
        dataType: 'json',
        success: function (data) {
            $(`.js-btn-accept[data-id=${applicationId}]`).addClass("disabled d-block").text('Accepted');
            $(`.js-btn-reject[data-id=${applicationId}]`).hide();
            $(`.js-application-row[data-id=${applicationId}]`).data('status', 'True');
        }
    });
});

$('.js-btn-reject').on('click', function () {
    let applicationId = $(this).data('id');
    $.ajax({
        url: `/applications/reject/${applicationId}/`,
        type: 'post',
        dataType: 'json',
        success: function (data) {
            $(`.js-btn-reject[data-id=${applicationId}]`).addClass("disabled d-block").text('Rejected');
            $(`.js-btn-accept[data-id=${applicationId}]`).hide();
            $(`.js-application-row[data-id=${applicationId}]`).data('status', 'False');
        }
    });
});