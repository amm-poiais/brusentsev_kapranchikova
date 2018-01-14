var OWNER = 'owner';
var USER = 'user';
var NONE = 'none';


actTrip = function () {
};

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
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    actTrip = function (id_trip, type, button) {
        var res = true;
        if (type == OWNER) {
            res = prompt("Предупреждение", "Вы действительно хотите удалить поездку?");

        }
        if (res)
            $.post("", {id_trip: id_trip, type: type})
                .done(function (data) {
                    var newBut = document.createElement("div");
                    newBut.classList.add("trip__button");
                    newBut.onclick = function () {
                        actTrip(id_trip, data, this);
                    };
                    var newBut_content;
                    switch (data) {
                        case "user":
                            newBut_content = document.createTextNode("Отсоединиться");
                            break;
                        case "none":
                            newBut_content = document.createTextNode("Присоединиться");
                            break;
                        case "deleted":
                            button.parentNode.parentNode.remove();
                            break
                    }
                    newBut.appendChild(newBut_content);
                    button.parentNode.replaceChild(newBut, button);
                });
    };

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
                        $(".new-trips .trip .wrap-icons-button").append('<div class="trip__button" onclick="actTrip(' + data[i].key[0].pk + ',\'' + data[i].value + '\', this)"></div>');
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

});