$("#btnLogin").click(function() {
	var username = $("#inputusername").val();
	var password = $("#inputpassword").val();
	$.getJSON("https://chihuahuas.iriscouch.com/user/" + username, function(data){
		if (data.password == password) {
			alert("login successful\n User: " + username);
		} else if(data.password != password) {
			alert("login unsuccessful\n User: " + username);
		}
	}).error(function(){alert("Invalid Login");});
});

$("#btnForgotPassword").click(function() {
});

$("#btnSignUp").click(function() {
});