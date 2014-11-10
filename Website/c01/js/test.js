$("#btnTest").click(function () {
    console.log("Hello");
    $.getJSON(
        "http://www.chihuahuas.iriscouch.com/user/_design/usertest/_view/usertest",
        function (data) {
            console.log(data.rows[0].value);
        });
});
