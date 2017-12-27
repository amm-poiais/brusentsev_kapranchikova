$(document).ready(function () {
    $('#find').click(function (event) {
        $.get("index.html", {date: $('#datepicker').val(), departure : $('#departure').val(), arrive: $('#arrive').val()})
            .done(function (data) {
            });
    });

});