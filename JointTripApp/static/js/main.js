actTrip = function () {};

$(document).ready(function () {
    actTrip = function (id_trip, type) {
        $.post("/", {id_trip: id_trip, type: type})
            .done(function (data) {
                alert("Data Loaded: " + data);
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

                        $(".new-trips .trip .wrap-icons-button").append('<div class="trip__button" onclick="actTrip('+data[i].key[0].pk+','+data[i].value+')"></div>');
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

    });

    $(".createdTrip").click(function () {

    });

});