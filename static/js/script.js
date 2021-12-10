const socket = io.connect(window.location.origin);

var all_active_users = [];

socket.on('connect', function(){
	console.log('Connected');
});

socket.on("all_users", function(data){
	let users_list = document.getElementById('users_list');
	users_list.innerHTML = '';
	all_active_users = data;
	for(let i = 0; i < data.length; i++) {
		users_list.innerHTML += `<li>${data[i]}</li>`;
	}
});

socket.on("points", function(data){
	if (data.username == user_info["username"]) {
		document.getElementById('points_int').innerHTML = data.points;
	}
});	



const get_all_users = () => {
	socket.emit('get_all_users');
}

document.addEventListener("DOMContentLoaded", function(){
	get_all_users();
});

const mc_list = () => {
	socket.emit('mc-list');
}


const do_command = (command) => {
	socket.emit('do-command', {"username": user_info["username"], "command": command} );
}