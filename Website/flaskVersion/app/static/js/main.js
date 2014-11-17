$("#btnAddSource").click(function() {
    var urlRegex = new RegExp("^w{3}.[a-zA-Z0-9]{2,}.[a-z]{2,3}$");
    var source = $("#inputsource").val();
    if (!urlRegex.test(source)) {
        alert("Please enter a valid url");
        return;
    }
    var id = source.substring(source.indexOf(".") + 1, source.lastIndexOf("."));
    $.post($SCRIPT_ROOT + '/add_source', {
        id: id,
        url: source
    }).done(function(result) {
        console.log(result)
        alert("Successfully added " + source);
    }).fail(function(xhr, status, error) {
        console.log(error)
        alert("Cannot add duplicate news source");
    });
});

$('#show-sources').on('click', function() {
    console.log("Hello");
    //get collapse content selector
    var collapse_content_selector = $(this).attr('href');

    //make the collapse content to be shown or hide
    var toggle_switch = $(this);

    $(collapse_content_selector).toggle(function() {
        if ($(this).css('display') == 'none') {
            //change the button label to be 'Show'
            toggle_switch.html('Show Sources');
        }
        else {
            //change the button label to be 'Hide'
            toggle_switch.html('Hide Sources');
        }
    });
});

$('#show-keywords').on('click', function() {
    //get collapse content selector
    var collapse_content_selector = $(this).attr('href');

    //make the collapse content to be shown or hide
    var toggle_switch = $(this);

    $(collapse_content_selector).toggle(function() {
        if ($(this).css('display') == 'none') {
            //change the button label to be 'Show'
            toggle_switch.html('Show Keywords');
        }
        else {
            //change the button label to be 'Hide'
            toggle_switch.html('Hide Keywords');
        }
    });
});

window.onload = function() {
    $(".getsources").empty();
    $.getJSON(
        "http://www.chihuahuas.iriscouch.com/news_source/_all_docs?include_docs=true",
        function(data) {
            var sources = [];
            $.each(data.rows, function(key, val) {
                sources.push("<li id='" + val.doc._id +
                    "'>" + val.doc.url + "</li>");
            });

            $("<ul/>", {
                "class": "listofsources",
                html: sources.join("")
            }).appendTo(".getsources");
        });

    $(".getkeywords").empty();
    // Display the current keywords form the DB
    $.getJSON(
        "http://www.chihuahuas.iriscouch.com/keywords/_all_docs?include_docs=true",
        function(data) {
            var keywords = [];
            $.each(data.rows, function(key, val) {
                // console.log(val.doc);
                keywords.push("<li class='keywords'>" +
                    val.doc.keyword + "</li>");
            });

            $("<ul/>", {
                "class": "listofkeywords",
                html: keywords.join("")
            }).appendTo(".getkeywords");
        });
};

$("#btnDeleteSource").click(function() {
    var source = $("#deletesource").val();
    var id = source.substring(source.indexOf(".") + 1, source.lastIndexOf(
        "."));
    var rev = "";
    $.getJSON("http://www.chihuahuas.iriscouch.com/news_source/" +
        id, function(data) {
            $.each(data, function(key, val) {
                rev = data._rev;
            });
            $.ajax({
                type: "DELETE",
                url: "http://www.chihuahuas.iriscouch.com/news_source/" +
                    id + "?rev=" + rev,
                dataType: "json",
                contentType: "application/json",
                success: function(data) {
                    alert("Successfully deleted " +
                        source);
                },
                error: function(xhr, status, error) {
                    alert(
                        "ERROR: Cannot get keyword"
                    );
                }
            });
        });
});

$("#btnAddKeyword").click(function() {
    var key = $("#inputkeyword").val();
    var keyRegex = new RegExp("^[a-zA-Z0-9]+$");
    if (!keyRegex.test(key)) {
        alert("Please enter an alphanumeric keyword");
        return;
    }

    $.post($SCRIPT_ROOT + '/add_keywords', {
        id: key,
        keyword: key
    }).done(function(result) {
        console.log(result)
        alert("Successfully added " + key);
    }).fail(function(xhr, status, error) {
        console.log(xhr.responseText + ': ' + error)
        alert("Cannot add duplicate keyword");
    });
});

$("#btnDeleteKeyword").click(function() {
    var key = $("#deletekeyword").val();
    var rev = "";
    $.getJSON("http://www.chihuahuas.iriscouch.com/keywords/" +
        key, function(data) {
            $.each(data, function(key, val) {
                rev = data._rev;
            });
            $.ajax({
                type: "DELETE",
                url: "http://www.chihuahuas.iriscouch.com/keywords/" +
                    key + "?rev=" + rev,
                dataType: "json",
                contentType: "application/json",
                success: function(data) {
                    alert("Successfully deleted " +
                        key);
                },
                error: function(xhr, status, error) {
                    alert(
                        "ERROR: Cannot get keyword"
                    );
                }
            });
        });
});

$("#btnTableSources").click(function() {
    location.href = "table.html";
});

$("#btnReturnIndex").click(function() {
    location.href = "index.html";
});