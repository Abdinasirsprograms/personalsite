// form submission handling
document.addEventListener('DOMContentLoaded', () => {
	var form = document.getElementById("contactForm");

	form.addEventListener('submit', function(event){
					event.preventDefault();
					var request = new XMLHttpRequest();
					request.open("POST", '/contacted/', true);
						request.onload = function() {
							var myArr = JSON.parse(this.responseText);
							if ((this.status === 200) && myArr.toString().includes('form_sent: \"true\"') == true) {
							 $("#contactModal").modal('hide'); // remove contactModal
							 $("#successModal").modal('show'); //success message
							 $(".btn-default").replaceWith('<p class="h2">Message has been sent <i class="far fa-thumbs-up fa-2x"></i></p>');
							 var myArr = JSON.parse(this.responseText);
							 console.log(myArr);
							}
							else {
							 $("#contactModal").modal('hide'); // remove contactModal
							$("#successModal").removeClass('alert-success');
							$("#successModal").addClass('alert-danger');
							$(".bodyMessage").replaceWith('<p class="h1 bodyMessage"><strong>Message Was not sent!</strong> bot detected. If you\re human please try again later!</p>');
							$(".btn-default").replaceWith('<p class="h2">Message has was not sent!<i class="far fa-thumbs-down fa-2x"></i></p>');
							console.log(myArr);
							};
						};
					request.send(new FormData(this));
	      });
});
