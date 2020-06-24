$(document).ready(function () {

    // Toggle project filtering by user skill set.
    $("#js-toggle-my-projects").on('click', function () {
        $("#my-projects").toggle(this.checked);
        $("#all-projects").toggle(!this.checked);
    });


    let positionFilter = 'all';
    let skillFilter = 'all';

    function filterPositions() {
        // Iterate through positions and hide if it doesn't match both filters
        $('.js-position-row').each(function() {
            let filtered = false;

            const position = $(this).data('position');
            const skills = $(this).data('skills');

            if (positionFilter !== 'all') {
                if (position !== positionFilter) {
                    filtered = true;
                }
            }

            if (skillFilter !== 'all') {
                if (!(skills.includes(skillFilter))) {
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

    $('.js-position-filter .nav-link').on('click', function() {
        positionFilter = $(this).data('position');
        filterPositions();
    });

    $('.js-skill-filter .nav-link').on('click', function() {
        skillFilter = $(this).data('skills');
        filterPositions();
    });
});
