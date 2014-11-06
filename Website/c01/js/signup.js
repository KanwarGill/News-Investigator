$("#btnCreateAccount").click(function() {
	var username = $("#inputusername").val();
	var password = $("#inputpassword").val();
	var password2 = $("#inputpassword2").val();
	var security_q = $("#inputsecurityquestion").val();
	var security_a = $("#inputsecurityanswer").val();
	
	if (password == password2){
		$.ajax({
			type: "POST",
			url: "http://www.chihuahuas.iriscouch.com/user",
			dataType: "json",
			data: '{ "_id" : "' + username + '", "username" : "' + username + '", "password" : "' + password + '", "security_q" : "' + security_q + '", "security_a" : "' + security_a + '" }',
			contentType: "application/json",
			processData: false,
			success: function (data) {
				alert("Successfully created account: " + username);
			},
			error: function() {
				alert("Could not create account");
			}
		});
	} else {
		alert("Passwords do not match");
	}
});

$("#btnCancel").click(function() {
	location.href = "login.html";
});