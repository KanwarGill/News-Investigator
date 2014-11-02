          $("#btnAddSource").click(function () {
          //var urlRegex = new RegExp("/^(https?://)?([da-z.-]+).([a-z.]{2,6})([/w .-]*)*/?$/");
	  var urlRegex = new RegExp("^w{3}\.[a-zA-Z0-9]{2,}\.[a-z]{2,3}$");
          var source = $("#inputsource").val();
           if (!urlRegex.test(source)) {
             alert("Please enter a valid url");
	     return;
           }
          var id = source.substring(source.indexOf(".") + 1, source.lastIndexOf("."));
          // console.log(id);
          $.ajax({
              type: "POST",
              url: "http://www.chihuahuas.iriscouch.com/news_source",
              dataType: "json",
              data: '{ "_id" : "' + id + '", "url": "' + source + '" }',
              contentType: "application/json",
              processData: false,
              success: function (data) {
                alert("Successfully added " + source);
              },
              error: function(){
                alert("Cannot add duplicate news source");
              }
          });
        });

        $("#btnGetSources").click(function() {
          $(".getsources").empty();
          // Display the current sources form the DB
          $.getJSON("http://www.chihuahuas.iriscouch.com/news_source/_all_docs?include_docs=true", function(data) {
            var sources = [];
            $.each(data.rows, function(key, val) {
              // console.log(val.doc);
              sources.push("<li id='" + val.doc._id + "'>" + val.doc.url + "</li>");
            });

            $("<ul/>", {
              "class": "listofsources",
              html: sources.join("")
            }).appendTo(".getsources");
          });
        });

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
              },
              error: function(){
                alert("ERROR: Cannot get keyword");
              }
            });
          });
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
              },
              error: function(){
                alert("Cannot add duplicate keyword");
              }
          });
        });

        $("#btnGetKeywords").click(function() {
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
              },
              error: function(){
                alert("ERROR: Cannot get keyword");
              }
            });
          });
        });
