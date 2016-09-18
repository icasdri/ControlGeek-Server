setTimeout(function() {
    v = document.createElement("p");
    v.innerHTML = "Javascript is running";
    document.body.appendChild(v);
}, 100);

var socket = new WebSocket("ws://18.22.7.180:9877/sock");
setInterval(function() {
    socket.send("This is a test!");
}, 1000)

var servo_slider = document.getElementById('servo_slider');
var servo_label = document.getElementById('servo_label');
var led_slider = document.getElementById('led_slider');
var led_label = document.getElementById('led_label');

servo_slider.oninput = function() {
    servo_label.innerHTML = 'Servo: ' + servo_slider.value;
}

led_slider.oninput = function() {
    led_label.innerHTML = 'LED: ' + led_slider.value;
}
