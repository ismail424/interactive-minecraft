var audio = new Audio(`/static/sounds/success.mp3`);
var fail_audio = new Audio(`/static/sounds/fail.mp3`);
const mc_command = (id, price) => {
	console.log("mc_command", id, price);
	socket.emit('mc-command', {"username": user_info["username"], "command_id": id});
	if (user_info["points"] >= price) {
		success_popup(price);
	}
	else{
		unsuccess_popup();
	}
}

const py_command = (id, price) => {
	console.log("py_command", id, price);
	socket.emit('py-command', {"username": user_info["username"], "command_id": id} );
	if (user_info["points"] >= price) {
		success_popup(price);
	}
	else{
		alert("You don't have enough money!");
	}
}

const success_popup = (price) => {
	let price_text = document.getElementById("price_popup");
	let all_buttons = document.getElementsByClassName("command_button");
	for (let i = 0; i < all_buttons.length; i++) {
		all_buttons[i].disabled = true;
	}

	price_text.classList.remove("price_popup_animation");
	price_text.innerHTML = "";


	function randomInRange(min, max) {
		return Math.random() * (max - min) + min;
	}
	
	confetti({
	spread: 400,
	particleCount: randomInRange(50, 300),
	origin: { y: randomInRange(0.1, 0.9) }
	});

	
	audio.load();
	audio.play();

	price_text.innerHTML = `-${price}¥`;
	// add transform animation to price_text
	price_text.classList.add("price_popup_animation");
	setTimeout(() => {
		price_text.classList.remove("price_popup_animation");
		price_text.innerHTML = "";
		for (let i = 0; i < all_buttons.length; i++) {
			all_buttons[i].disabled = false;
		}
	}, 900);

}

const unsuccess_popup = () => {
	let not_enough_money = document.getElementById("not_enough_popup");
	fail_audio.load();
	fail_audio.play();
	not_enough_money.style.display = "block";
	setTimeout(() => {
		fail_audio.pause();
		not_enough_money.style.display = "none";
	}, 5000);

}