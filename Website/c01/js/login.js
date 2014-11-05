$("#btnLogin").click(function() {
	var username = $("#inputusername").val();
	var password = $("#inputpassword").val();
	$.getJSON("https://chihuahuas.iriscouch.com/user/" + username, function(data){
		if (data[3] = password) {
			alert("login successful " + username);
		} else {
			alert("login unsuccessful " + username);
		}
	});
});

$("#btnForgotPassword").click(function() {
});

$("#btnSignUp").click(function() {
});