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

      $('#show-sources').on('click', function () {
      //get collapse content selector
      var collapse_content_selector = $(this).attr('href');         
 
      //make the collapse content to be shown or hide
      var toggle_switch = $(this);

        $(collapse_content_selector).toggle(function(){
          if($(this).css('display')=='none'){
          //change the button label to be 'Show'
		toggle_switch.html('Show Sources');
          }else{
          //change the button label to be 'Hide'
      toggle_switch.html('Hide Sources');
          }
        });
      });

      $('#show-keywords').on('click', function () {
      //get collapse content selector
      var collapse_content_selector = $(this).attr('href');         

      //make the collapse content to be shown or hide
      var toggle_switch = $(this);

        $(collapse_content_selector).toggle(function(){
          if($(this).css('display')=='none'){
          //change the button label to be 'Show'
          toggle_switch.html('Show Keywords');
          }else{
          //change the button label to be 'Hide'
          toggle_switch.html('Hide Keywords');
          }
        });
      });
    
    $('#show-handles').click(function () {
      //get collapse content selector
      var collapse_content_selector = $(this).attr('href');         

      //make the collapse content to be shown or hide
      var toggle_switch = $(this);

      $(collapse_content_selector).toggle(function(){
        if($(this).css('display')=='none'){
          //change the button label to be 'Show'
          toggle_switch.html('Show Handles');
        }else{
          //change the button label to be 'Hide'
          toggle_switch.html('Hide Handles');
        }
      });
    });

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

    function getSources(){
      $(".getsources").empty();
    
      $.get($SCRIPT_ROOT + '/get_sources').done(function(result){
          console.log(result.data);
          var sources = [];
          $.each(result.data, function(key, val) {
              sources.push("<li class='sources' id='" + val.id + "'>" + val.key + "</li>");
          });            

          $("<ul/>", {
              "class": "listofsources",
              html: sources.join("")
          }).appendTo(".getsources");
      });
    };
    
    function getKeywords(){
      $(".getkeywords").empty();
        // Display the current keywords form the DB
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
    
    function getHandles(){
      $(".gethandles").empty();
      $.getJSON("http://www.chihuahuas.iriscouch.com/handles/_all_docs?include_docs=true", function(data) {
        var handles = [];
        $.each(data.rows, function(key, val) {
          handles.push("<li class='handles'>" + val.doc.handle + "</li>");
        });
        
        $("<ul/>", {
          "class": "listofhandles",
          html: handles.join("")
        }).appendTo(".gethandles");
      });
    };
    
    window.onload = function() {
      getSources();
      getKeywords();
      getHandles();
    };


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

    $("#btnAddHandle").click(function () {
      var handleRegex = new RegExp("^@{1}[a-zA-Z0-9_]{1,15}$");
      var handle = $("#inputtwitterhandle").val();
      if (!handleRegex.test(handle)) {
        alert("Please enter a valid twitter handle");
        return;
      }
      var id = handle.substring(handle.indexOf("@") + 1);
      $.ajax({
        type: "POST",
        url: "http://www.chihuahuas.iriscouch.com/handles",
        dataType: "json",
        data: '{ "_id" : "' + id + '", "handle": "' + handle + '" }',
        contentType: "application/json",
        processData: false,
        success: function (data) {
          alert("Successfully added " + handle);
		  getHandles();
        },
        error: function(){
          alert("Cannot add twitter handle");
        }
      });
    });
    
    $("#btnDeleteHandle").click(function () {
      var handle = $("#deletetwitterhandle").val();
      var rev = "";
      var id = handle.substring(handle.indexOf("@") + 1);
      $.getJSON("http://www.chihuahuas.iriscouch.com/handles/" + id, function(data) {
        $.each(data, function(key, val) {
          rev = data._rev;
        });
        $.ajax({
          type: "DELETE",
          url: "http://www.chihuahuas.iriscouch.com/handles/" + id + "?rev=" + rev,
          dataType: "json",
          contentType: "application/json",
          success: function (data) {
            alert("Successfully deleted " + handle);
			getHandles();
          },
          error: function(){
            alert("ERROR: cannot get twitter handle");
          }
        });
      }).error(function(){alert("ERROR: twitter handle not in database");});
    });

$("#btnTableSources").click(function() {
    location.href = "table.html";
});

$("#btnReturnIndex").click(function() {
    location.href = "index.html";
});