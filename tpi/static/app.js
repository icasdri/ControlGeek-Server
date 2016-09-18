setTimeout(function() {
    v = document.createElement("p");
    v.innerHTML = "Javascript is running";
    document.body.appendChild(v);
}, 1000);

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
