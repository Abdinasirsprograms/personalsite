// // Set the date we're counting down to
// var countDownDate = new Date("Dec 25, 2019 04:20:25").getTime();
//
// // Update the count down every 1 second
// var x = setInterval(function() {
//
//   // Get todays date and time
//   var now = new Date().getTime();
//
//   // Find the distance between now and the count down date
//   var distance = countDownDate - now;
//
//   // Time calculations for days, hours, minutes and seconds
//   var days = Math.floor(distance / (1000 * 60 * 60 * 24));
//   var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
//   var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
//   var seconds = Math.floor((distance % (1000 * 60)) / 1000);
//
//   // Output the result in an element with id="demo"
//   document.getElementById("timer").innerHTML =  hours + "hrs: "
//   + minutes + "mins: " + seconds + "secs";
//
//   // If the count down is over, write some text
//   if (distance < 0) {
//     clearInterval(x);
//     document.getElementById("timer").innerHTML = "EXPIRED!";
//   }
// }, 1000);
var DEV = true
var DEVLINK = 'http://localhost:80'
	var formElement = document.querySelectorAll("form");
	for (let i = 0; i < formElement.length; i++) {
		formElement[i].addEventListener('submit', function(event){
				event.preventDefault();
				var request = new XMLHttpRequest();
				request.open("POST", (`${DEV ? DEVLINK:'https://abdinasirnoor.com'}`+ String(this[1].value)), true);
					request.onload = function() {
						if ((this.status === 200)) {
							var cart = document.getElementById('cart_count');
							cart.innerHTML = JSON.parse(this.response).cart_count_update;
							if (formElement[i].querySelector('button.btn-success') != null) {
									var add_Button = formElement[i].querySelector('button.btn-success');
									add_Button.classList.remove('btn-success');
									add_Button.classList.add('btn-secondary')
									add_Button.innerHTML = '&#x2714; Added to cart!';
								};
							console.log(this.response);
						}
						else {
							console.log(this.responseText);
						};
					};
				request.send(new FormData(this));
		});};

$(function() {
var increaseQuantity = $("i.spinnerIncrease");
var decreaseQuantity = $("i.spinnerDecrease");
var inputValue = $("input.quantityInput");
var numberItem = parseInt(inputValue.val());
var arrayItems = [increaseQuantity,decreaseQuantity]
increaseQuantity.click(function() {
	numberItem = numberItem + 1;
	inputValue.attr("value",numberItem);
	$(this).fadeOut(250);
	$(this).fadeIn(250);
	});
decreaseQuantity.click(function() {
	if ((numberItem - 1) >= 0) {
		numberItem = numberItem - 1;
		inputValue.attr("value",numberItem);
		$(this).fadeOut(250);
		$(this).fadeIn(250);
		};
	});
inputValue.keydown(function(event) {
	if (event.which == 38) {
		numberItem = numberItem + 1;
		inputValue.attr("value",numberItem);
		$(increaseQuantity).fadeOut(250);
		$(increaseQuantity).fadeIn(250);
		};
	});
inputValue.keydown(function(event) {
	if (event.which == 40) {
		if ((numberItem - 1) >= 0) {
				numberItem = numberItem-1;
				inputValue.attr("value",numberItem);
				$(decreaseQuantity).fadeOut(250);
				$(decreaseQuantity).fadeIn(250);
			};
		};
	});
});
