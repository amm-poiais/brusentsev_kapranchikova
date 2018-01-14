actTrip = function () {};

$(document).ready(function () {
    var csrftoken = $.cookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


    actTrip = function (id_trip, type) {
        $.post("", {id_trip: id_trip, type: type})
            .done(function (data) {
                console.log("Data Loaded: " + data);
            });
    }

    $('#find').click(function (event) {
        $.get("/", {date: $('#datepicker').val(), departure: $('#departure').val(), arrive: $('#arrive').val()})
            .done(function (data) {

                data = JSON.parse(data);
                for (var i = 0; i < data.length; i++) {
                    data[i].key = JSON.parse(data[i].key);
                }
                $(".new-trips").empty();
                $(".new-trips").append('<h2>Поездки</h2>');
                for (var i = 0; i < data.length; i++) {

                    $(".new-trips")
                        .append('<div class="trip">' +
                            '<div class="title">' +
                            data[i].key[0].fields.departure + ' - ' + data[i].key[0].fields.arrival +
                            '<div class="time">' + data[i].key[0].fields.start_time + '</div>' +
                            '</div>' +
                            '<div class="wrap-price-comm">' +
                            '<div class="description">' + data[i].key[0].fields.comment + '</div>' +
                            '<div class="duration">' + data[i].key[0].fields.duration + '</div>' +
                            '<div class="price">' + data[i].key[0].fields.price + 'p.</div>' +
                            '</div>' +
                            '<div class="wrap-icons-button">' +
                            '<div class="icon-conditions">' +
                            //'+ data[i].key[0].fields.smoke ? 'allow'+'
                            '<div class="icon talk"></div>' +
                            '<div class="icon pets"></div>' +
                            '<div class="icon smoke"></div>' +
                            '</div>' +


                            '</div>');
                    if (data[i].key[0].fields.smoke) {
                        $(".trip .icon.smoke").addClass("allow");
                    }
                    if (data[i].key[0].fields.pets) {
                        $(".trip .icon.pets").addClass("allow");
                    }
                    if (data[i].key[0].fields.talk) {
                        $(".trip .icon.talk").addClass("allow");
                    }

                    if ($('*').is('.profile')) {
                        $(".new-trips .trip .wrap-icons-button").append('<div class="trip__button" onclick="actTrip('+data[i].key[0].pk+',\''+ data[i].value+'\')"></div>');
                        $(".trip .trip__button").data("id_trip", data[i].key[0].pk);

                        if (data[i].value == "user") {
                            $(".trip .trip__button").append("Отсоединиться");
                            // $(".trip .trip__button").addClass("unJoin");

                        } else if (data[i].value == "owner") {
                            $(".trip .trip__button").append("Удалить");
                            // $(".trip .trip__button").addClass("remove");
                        } else if (data[i].value == "none") {
                            $(".trip .trip__button").append("Присоединиться");
                            // $(".trip .trip__button").addClass("join");
                        }
                    }


                }


            });
    });


    $(".myJoinTrip").click(function () {
        console.log("myjoin");
    });

    $(".createdTrip").click(function () {
        console.log("createed");
    });

});