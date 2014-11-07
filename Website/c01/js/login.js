$("#btnLogin").click(function() {
	var username = $("#inputusername").val();
	var password = $("#inputpassword").val();
	if (username == "" || password == "") {
		alert("Please enter your username and password");
		return;
	}
	$.getJSON("https://chihuahuas.iriscouch.com/user/" + username, function(data){
		if (data.password == password) {
			alert("login successful\n User: " + username);
			location.href = "index.html";
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