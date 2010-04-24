if (typeof console == "undefined" || typeof console.log == "undefined") var console = { log: function() {} };

$(document).ready(function(){
	$('#layoutImg').click(function() {
		var url = $('a.titel')[0].href;
		console.log("redirecting to: " + url);
		document.location = url;
	});
});