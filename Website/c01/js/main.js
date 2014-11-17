      $("#btnAddSource").click(function () {
         var urlRegex = new RegExp("^w{3}\.[a-zA-Z0-9]{2,}\.[a-z]{2,3}$");
          var source = $("#inputsource").val();
           if (!urlRegex.test(source)) {
             alert("Please enter a valid url");
       return;
           }
          var id = source.substring(source.indexOf(".") + 1, source.lastIndexOf("."));
          $.ajax({
              type: "POST",
              url: "http://www.chihuahuas.iriscouch.com/news_source",
              dataType: "json",
              data: '{ "_id" : "' + id + '", "url": "' + source + '" }',
              contentType: "application/json",
              processData: false,
              success: function (data) {
                alert("Successfully added " + source);
                location.reload();
              },
              error: function(){
                alert("Cannot add duplicate news source");
                location.reload();
              }
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
      getSources();
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
      getKeywords();
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
          getHandles();
          toggle_switch.html('Show Handles');
        }else{
          //change the button label to be 'Hide'
          toggle_switch.html('Hide Handles');
        }
      });
    });

    function getSources(){
      $(".getsources").empty();
      $.getJSON("http://www.chihuahuas.iriscouch.com/news_source/_all_docs?include_docs=true", function(data) {
        var sources = [];
        $.each(data.rows, function(key, val) {
          sources.push("<li class='sources'>" + val.doc.url + "</li>");
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
      $.getJSON("http://www.chihuahuas.iriscouch.com/keywords/_all_docs?include_docs=true", function(data) {
        var keywords = [];
        $.each(data.rows, function(key, val) {
          // console.log(val.doc);
          keywords.push("<li class='keywords'>" + val.doc.keyword + "</li>");
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

        $("#btnDeleteSource").click(function () {
          var source = $("#deletesource").val();
          var id = source.substring(source.indexOf(".") + 1, source.lastIndexOf("."));
          var rev = "";
          $.getJSON("http://www.chihuahuas.iriscouch.com/news_source/" + id, function(data) {
            $.each(data, function(key, val) {
              rev = data._rev;
            });
            $.ajax({
              type: "DELETE",
              url: "http://www.chihuahuas.iriscouch.com/news_source/" + id + "?rev=" + rev,
              dataType: "json",
              contentType: "application/json",
              success: function (data) {
                alert("Successfully deleted " + source);
                location.reload();
              },
              error: function(){
                alert("ERROR: Cannot get Source URL");
                location.reload();
              }
            });
          }).error(function(){alert("ERROR: Source URL not in database");});
        });

        $("#btnAddKeyword").click(function () {
          var key = $("#inputkeyword").val();
           var keyRegex = new RegExp("^[a-zA-Z0-9]+$");
           if (!keyRegex.test(key)) {
             alert("Please enter an alphanumeric keyword");
       return;
           }  
          $.ajax({
              type: "POST",
              url: "http://www.chihuahuas.iriscouch.com/keywords/",
              dataType: "json",
              data: '{ "_id" : "' + key + '", "keyword" : "' + key + '" }',
              contentType: "application/json",
              processData: false,
              success: function (data) {
                alert("Successfully added " + key);
                location.reload();
              },
              error: function(){
                alert("Cannot add duplicate keyword");
                location.reload();
              }
          });
        });

        $("#btnDeleteKeyword").click(function () {
          var key = $("#deletekeyword").val();
          var rev = "";
          $.getJSON("http://www.chihuahuas.iriscouch.com/keywords/" + key, function(data) {
            $.each(data, function(key, val) {
              rev = data._rev;
            });
            $.ajax({
              type: "DELETE",
              url: "http://www.chihuahuas.iriscouch.com/keywords/" + key + "?rev=" + rev,
              dataType: "json",
              contentType: "application/json",
              success: function (data) {
                alert("Successfully deleted " + key);
                location.reload();
              },
              error: function(){
                alert("ERROR: Cannot get keyword");
                location.reload();
              }
            });
          }).error(function(){alert("ERROR: Keyword not in database");});
        });

        $("#btnTableSources").click(function () {
            location.href="table.html";
        });

        $("#btnReturnIndex").click(function () {
            location.href="index.html";
        });

        $("#btnExportTableXML").click(function () {
            $('#SourcesTable').tableExport({type:'xml',escape:'false'});
        });

        $("#btnExportTablePDF").click(function () {
            $('#SourcesTable').tableExport({type:'pdf',escape:'false'});
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
          location.reload();
        },
        error: function(){
          alert("Cannot add twitter handle");
          location.reload();
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
            location.reload();
          },
          error: function(){
            alert("ERROR: cannot get twitter handle");
            location.reload();
          }
        });
      }).error(function(){alert("ERROR: twitter handle not in database");});
    });