$("#btnGetSecurityQuestion").click(function() {
	var username = $("#inputusername").val();
	$.getJSON("https://chihuahuas.iriscouch.com/user/" + username, function(data){
		alert("" + data.security_q);
	}).error(function(){alert("Invalid Username");});
});

$("#btnGetPassword").click(function() {
	var username = $("#inputusername").val();
	var security_a = $("#inputsecurityanswer").val();
	$.getJSON("https://chihuahuas.iriscouch.com/user/" + username, function(data){
		if (data.security_a = security_a){
			alert("Your password is: " + data.password);
		} else {
			alert("Invalid Security Answer");
		}
	}).error(function(){alert("Invalid Username");});
});

$("#btnCancel").click(function() {
	location.href = "login.html";
});