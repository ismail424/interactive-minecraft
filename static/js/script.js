//socket.io is a library that allows us to connect to a server
const socket = io.connect(window.location.origin);
socket.on('connect', function(){
	console.log('connected');
});
socket.on('disconnect', function(){
	console.log('disconnected');
});
socket.on('message', function(message){
	console.log('message: ' + message);
});
socket.on('user', function(user){
	console.log('user: ' + user);
});
socket.on('users', function(users){
	console.log('users: ' + users);
});
//socket.emit('message', message);
