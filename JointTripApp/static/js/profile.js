$(document).ready(function () {

    $(".myJoinTrip").click(function () {
        $(".myJoinTrip").addClass("active");
        $(".createdTrip").removeClass("active");
        $.get("/profile", {type: "mytrip"})
            .done(function (data) {
                 console.log(data);
            });
    });

    $(".createdTrip").click(function () {
        $(".myJoinTrip").removeClass("active");
        $(".createdTrip").addClass("active");
        $.get("/profile", {type: "createdtrip"})
            .done(function (data) {
                 console.log(data);
            });
    });

});