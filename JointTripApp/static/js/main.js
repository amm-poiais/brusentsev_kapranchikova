$(document).ready(function () {
    $('#find').click(function (event) {
        $.get("/", {date: $('#datepicker').val(), departure : $('#departure').val(), arrive: $('#arrive').val()})
            .done(function (data) {

                data = JSON.parse(data);
                for (var i=0; i<data.length; i++){
                    data[i].key = JSON.parse(data[i].key);
                }
                console.log(data);
                $(".new-trips").empty();
                $(".new-trips").append('<h2>Поездки</h2>');
                 for (var i=0; i<data.length; i++){
                //     <div class="trip">
                //
                //     <div class="wrap-price-comm">
                //         <div class="description">{{ pair.key.comment }}</div>
                //         <div class="duration">{{ pair.key.duration }}</div>
                //         <div class="price">{{ pair.key.price }}p.</div>
                //     </div>
                //     <div class="wrap-icons-button">
                //         <div class="icon-conditions">
                //             {% if pair.key.talk %}
                //                 <div class="icon talk allow"></div>
                //             {% else %}
                //                 <div class="icon talk"></div>
                //             {% endif %}
                //             {% if pair.key.pets %}
                //                 <div class="icon pets allow"></div>
                //             {% else %}
                //                 <div class="icon pets"></div>
                //             {% endif %}
                //             {% if pair.key.smoke %}
                //                 <div class="icon smoke allow"></div>
                //             {% else %}
                //                 <div class="icon smoke"></div>
                //             {% endif %}
                //         </div>
                //         {% if user.is_authenticated %}
                //             {% if pair.value == 'user' %}
                //                 <a class="trip__button" href="/join?id={{ trip.trip_id }}">Отсоединиться</a>
                //             {% elif  pair.value == 'owner' %}
                //                 <a class="trip__button" href="/join?id={{ trip.trip_id }}">Удалить</a>
                //             {% else %}
                //                 <a class="trip__button" href="/join?id={{ trip.trip_id }}">Присоедениться</a>
                //             {% endif %}
                //         {% endif %}
                //     </div>
                //
                // </div>

                    $(".new-trips")
                        .append('<div class="trip">' +
                            '<div class="title">'+
                            data[i].key[0].fields.departure +' - '+data[i].key[0].fields.arrival +
                            '<div class="time">'+ data[i].key[0].fields.start_time +'</div>'+
                            '</div>'+
                            '<div class="wrap-price-comm">'+
                            '<div class="description">' + data[i].key[0].fields.comment +'</div>'+
                            '<div class="duration">' + data[i].key[0].fields.duration +'</div>'+
                            '<div class="price">' + data[i].key[0].fields.price +'p.</div>'+
                            '</div>'+
                            '<div class="wrap-icons-button">'+
                            '<div class="icon-conditions">'+
                            //'+ data[i].key[0].fields.smoke ? 'allow'+'
                            '<div class="icon talk"></div>'+
                            '<div class="icon pets"></div>'+
                            '<div class="icon smoke"></div>'+
                            '</div>'+


                        '</div>');
                    if(data[i].key[0].fields.smoke){
                        $(".trip .icon.smoke").addClass("allow");
                    }
                    if(data[i].key[0].fields.pets){
                        $(".trip .icon.pets").addClass("allow");
                    }
                    if(data[i].key[0].fields.talk){
                        $(".trip .icon.talk").addClass("allow");
                    }

                    //'<a class="trip__button" href="/join?id='+ data[i].key[0].pk+'">Отсоединиться</a>'+
                    if(data[i].value = "user"){
                        $(".trip .trip__button").empty();
                        $(".trip .trip__button").append("Отсоединиться");
                    }else if(data[i].value = "owner"){
                        $(".trip .trip__button").empty();
                        $(".trip .trip__button").append("Удалить");
                    }else if(data[i].value = "none"){
                        $(".trip .trip__button").empty();
                        $(".trip .trip__button").append("Присоединиться");
                    }
                }


            });
    });

});