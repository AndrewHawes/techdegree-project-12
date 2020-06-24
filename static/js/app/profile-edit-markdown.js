$(document).ready(function () {
    // Editable Select
    $('.js-select').editableSelect();

    $("#js-toggle-markdown").on('click', function () {
        $("#markdown-preview").toggle(this.checked);
        let $label = $('label[for=js-toggle-markdown]');
        $.post('/toggle_markdown/', {status: this.checked}, function(data) {
                if (data.using_markdown) {
                    $label.text('Markdown enabled').addClass('text-info').removeClass('text-muted');
                } else {
                    $label.text('Markdown disabled').addClass('text-muted').removeClass('text-info');
                }
            }
        );
    });

    // Markdown Converter
    const converter = new showdown.Converter();
    converter.setFlavor('github');
    let userText = $('#id_about').val();

    $('#markdown-preview').height($('#id_about').height());
    $('#markdown-output').html(converter.makeHtml(userText));
    $('#id_about').on('change keyup paste', function () {
        let currentVal = $(this).val();
        if (currentVal === userText) {
            return; //check to prevent multiple simultaneous triggers
        }

        userText = currentVal;
        let html = converter.makeHtml(userText);
        $('#markdown-output').html(html);
    });
});