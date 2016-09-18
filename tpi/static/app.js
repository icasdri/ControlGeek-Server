setTimeout(function() {
    v = document.createElement('p');
    v.innerHTML = 'Javascript is running';
    document.body.appendChild(v);
}, 100);

var targets = {};
var socket = new WebSocket('ws://18.22.7.180:9877/sock');
socket.onmessage = function(message) {
    var m = message.data;
    console.log('-- receiving message: ' + m);
    if (m.length >= 2) {
        var p = m[0];
        if (targets.hasOwnProperty(p)) {
            targets[p].updateValue(m.substring(1));
        }
    }
}

var form = document.getElementById('slider_form');

function Target(config_t) {
    var self = this;
    this.prefix = config_t.prefix;
    this.name = config_t.name;
    this.orig_value = config_t.value;

    this.slider = document.createElement('input');
    this.slider.setAttribute('type', 'range');
    this.slider.setAttribute('id', self.prefix + '_slider');
    this.slider.setAttribute('min', 0);
    this.slider.setAttribute('max', 1000);
    this.slider.setAttribute('step', 5);
    this.slider.setAttribute('value', self.orig_value);

    this.label = document.createElement('label');
    this.label.setAttribute('id', self.prefix + '_label');
    this.label.setAttribute('for', self.prefix + '_slider');
    this.label.setAttribute('step', 10);

    this.updateValue = function(val) {
        self.slider.value = val;
        self.label.innerHTML = self.name + ': ' + val;
    }

    this.label.innerHTML = this.name + ': ' + this.slider.value;

    this.slider.oninput = function() {
        self.label.innerHTML = self.name + ': ' + self.slider.value;
        socket.send(self.prefix + self.slider.value);
    }

    form.appendChild(self.label);
    form.appendChild(document.createElement('br'));
    form.appendChild(self.slider);
    form.appendChild(document.createElement('br'));
}

function setupTargets(raw_targets) {
    for (var i=0; i<raw_targets.length; i++) {
        var config_t = raw_targets[i];
        targets[config_t.prefix] = new Target(config_t);
    }
}

var req = new XMLHttpRequest();
req.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        setupTargets(JSON.parse(this.responseText));
    }
}
req.open('GET', 'http://18.22.7.180:9877/static/config.json', true);
req.send()

