function getSites(){
  $(".getsites").empty();

  $.get($SCRIPT_ROOT + '/get_sites').done(function(result){
      console.log(result.data);
      var sources = [];
      $.each(result.data, function(key, val) {
          sources.push("<li class='sites' id='" + val.id + "'>" + val.key + "</li>");
      });            

      $("<ul/>", {
          "class": "listofsites",
          html: sources.join("")
      }).appendTo(".getsites");
  });
};

function getDomains(){
  $(".getdomains").empty();

  $.get($SCRIPT_ROOT + '/get_domains').done(function(result){
      console.log(result.data);
      var sources = [];
      $.each(result.data, function(key, val) {
          sources.push("<li class='domains' id='" + val.id + "'>" + val.key + "</li>");
      });            

      $("<ul/>", {
          "class": "listofdomains",
          html: sources.join("")
      }).appendTo(".getdomains");
  });
};

$("#btnAddSite").click(function() {
    var urlRegex = /^https?:\/\/(\-\.)?([^\s\/?\.#-]+\.?)+(\/[^\s]*)?$/m;
    var source = $("#inputsite").val();
    if (!urlRegex.test(source)) {
        alert("Please enter a valid url");
        return;
    }
    var id = source.substring(source.indexOf(".") + 1, source.lastIndexOf("."));

    $.post($SCRIPT_ROOT + '/add_site', {
        id: id,
        url: source
    }).done(function(result) {
        console.log(result)
        getSites();
        alert("Successfully added " + source);
    }).fail(function(xhr, status, error) {
        console.log(error)
        alert("Cannot add duplicate site");
    });
});

$("#btnAddDomain").click(function() {
    var urlRegex = /^www.(\-\.)?([^\s\/?\.#-]+\.?)+(\/[^\s]*)?$/m;
    var source = $("#inputdomain").val();
    if (!urlRegex.test(source)) {
        alert("Please enter a valid url");
        return;
    }
    var id = source.substring(source.indexOf(".") + 1, source.lastIndexOf("."));

    $.post($SCRIPT_ROOT + '/add_domain', {
        id: id,
        url: source
    }).done(function(result) {
        console.log(result)
        getDomains();
        alert("Successfully added " + source);
    }).fail(function(xhr, status, error) {
        console.log(error)
        alert("Cannot add duplicate domain");
    });
});

$('#show-sites').on('click', function () {
    //get collapse content selector
    var collapse_content_selector = $(this).attr('href');         

    //make the collapse content to be shown or hide
    var toggle_switch = $(this);

    $(collapse_content_selector).toggle(function(){
      if($(this).css('display')=='none'){
      //change the button label to be 'Show'
      toggle_switch.html('Show Sites');
      }else{
      //change the button label to be 'Hide'
      toggle_switch.html('Hide Sites');
      }
    });
});

$('#show-domains').on('click', function () {
    //get collapse content selector
    var collapse_content_selector = $(this).attr('href');         

    //make the collapse content to be shown or hide
    var toggle_switch = $(this);

    $(collapse_content_selector).toggle(function(){
      if($(this).css('display')=='none'){
      //change the button label to be 'Show'
      toggle_switch.html('Show Domains');
      }else{
      //change the button label to be 'Hide'
      toggle_switch.html('Hide Domains');
      }
    });
});

$("#btnDeleteSite").click(function() {
    var source = $("#deletesite").val();
    var id = source.substring(source.indexOf(".") + 1, 
        source.lastIndexOf("."));
        
    $.post($SCRIPT_ROOT + '/delete_site', {
        id: 'site_' + id
    }).done(function(result) {
        console.log(result)
        getSites();
        alert("Successfully deleted " + source);
    }).fail(function(xhr, status, error) {
        console.log(error)
        alert("News source not found.");
    });
});

$("#btnDeleteDomain").click(function() {
    var source = $("#deletedomain").val();
    var id = source.substring(source.indexOf(".") + 1, 
        source.lastIndexOf("."));
        
    $.post($SCRIPT_ROOT + '/delete_domain', {
        id: 'domain_' + id
    }).done(function(result) {
        console.log(result)
        getDomains();
        alert("Successfully deleted " + source);
    }).fail(function(xhr, status, error) {
        console.log(error)
        alert("News source not found.");
    });
});

$("#btnStartArticleCrawl").click(function() {
    alert("This action is not yet implemented until boilerpipe is installed.");
    /*$.post('/crawling', {
        action: "crawl"
    }).done(function(result) {
        console.log(result);
        $("#btnStartCrawl").toggleClass("disabled", true);
        alert("Crawl will be finished shortly. You can view the results in 'View Results");
    }).fail(function() {
        console.log("Error.");
    });*/
});

window.onload = function() {
  getSites();
  getDomains();
};