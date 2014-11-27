$("#btnLogin").click(function() {
	var username = $("#inputusername").val();
	var password = $("#inputpassword").val();
	if (username == "" || password == "") {
		alert("Please enter your username and password");
		return;
	}
	$.getJSON("https://chihuahuas.iriscouch.com/user/" + username, function(data){
		if (data.password == password) {
			alert("Welcome " + username);
			location.href = "index";
		} else if(data.password != password) {
			alert("login unsuccessful\n User: " + username);
		}
	}).error(function(){alert("Invalid Login");});
});

$("#btnForgotPassword").click(function() {
	location.href = "forgotpassword.html";
});

$("#btnSignUp").click(function() {
	location.href = "signup.html";
});