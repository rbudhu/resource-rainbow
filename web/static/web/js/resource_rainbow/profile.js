$(document).ready(function() {
    $('#id_skills').select2({
        placeholder: 'Enter a list of skills',
        tags: true,
        tokenSeparators: [',']
    });
});
