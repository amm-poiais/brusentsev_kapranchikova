$(document).ready(function () {
    $('#find').click(function (event) {
        $.get("/", {date: $('#datepicker').val(), departure: $('#departure').val(), arrive: $('#arrive').val()})
            .done(function (data) {
                console.log(data);
            });
    });

});