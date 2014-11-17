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
    
    $.get($SCRIPT_ROOT + '/get_sources').done(function(result){
        console.log(result.data);
        var sources = [];
        $.each(result.data, function(key, val) {
            console.log(val.id);
            console.log(val.key);
            sources.push("<li id='" + val.id + "'>" + val.key + "</li>");
        });            

        $("<ul/>", {
            "class": "listofsources",
            html: sources.join("")
        }).appendTo(".getsources");

    });

    $.get($SCRIPT_ROOT + '/get_keywords').done(function(result){
        console.log(result.data);
        var keywords = [];
        $.each(result.data, function(key, val) {
            keywords.push("<li class='keywords'>" + val.key + "</li>");
        });            

        $("<ul/>", {
            "class": "listofkeywords",
            html: keywords.join("")
        }).appendTo(".getkeywords");

    });
};

$("#btnDeleteSource").click(function() {
    var source = $("#deletesource").val();
    var id = source.substring(source.indexOf(".") + 1, 
        source.lastIndexOf("."));
        
    $.post($SCRIPT_ROOT + '/delete_source', {
        id: 'news_source_' + id
    }).done(function(result) {
        console.log(result)
        alert("Successfully deleted " + source);
    }).fail(function(xhr, status, error) {
        console.log(error)
        alert("News source not found.");
    });
});

$("#btnAddKeyword").click(function() {
    var key = $("#inputkeyword").val();
    var keyRegex = new RegExp("^[a-zA-Z0-9]+$");
    if (!keyRegex.test(key)) {
        alert("Please enter an alphanumeric keyword");
        return;
    }

    $.post($SCRIPT_ROOT + '/add_keyword', {
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
    $.post($SCRIPT_ROOT + '/delete_source', {
        id: 'keyword_' + key
    }).done(function(result) {
        console.log(result)
        alert("Successfully deleted " + key);
    }).fail(function(xhr, status, error) {
        console.log(error)
        alert("Keyword not found.");
    });
});

$("#btnTableSources").click(function() {
    location.href = "table.html";
});

$("#btnReturnIndex").click(function() {
    location.href = "index.html";
});