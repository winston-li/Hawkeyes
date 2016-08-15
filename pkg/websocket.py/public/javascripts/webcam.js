// Log to html body
var log = function(msg) {
    document.getElementById('log').innerHTML = document.getElementById('log').innerHTML + msg + "<br/>";
};

// Browser compatibility
var video = document.getElementById('sourcevid'), 
    heading = document.getElementsByTagName('h1')[0];

navigator.getMedia = ( navigator.getUserMedia ||
                         navigator.webkitGetUserMedia ||
                         navigator.mozGetUserMedia ||
                         navigator.msGetUserMedia);

// Start webcam playback
navigator.getMedia( {video: true, audio: false}, 
    function(stream) {
        if (navigator.mozGetUserMedia) {
            video.mozSrcObject = stream;
        } else {
            var vendorURL = window.URL || window.webkitURL;
            video.src = vendorURL.createObjectURL(stream);
        }
        video.play();
        heading.textContent = "Web camera streaming started";
    },
    function(err) {
        heading.textContent = "Web camera streaming is not supported, an error occurred: [" + error + "]";
    }
);

// Draw video to output canvas
// var canvas = document.createElement('canvas'); // create a hidden canvas 
var canvas = document.getElementById('output');
var ctx_out = canvas.getContext('2d');
var cw = 320; //video.clientWidth;
var ch = 240; //video.clientHeight;
var drawTimer;
// Render an alpha rectengle on top of video 
var rect;

log('height = ' + ch);
canvas.width = cw;
canvas.height = ch;
extractVideoFrame();

function extractVideoFrame() {
    // First, draw it into the backing canvas
    ctx_out.drawImage(video, 0, 0, cw, ch);
    // Grab the pixel data from the backing canvas
    var stringData=canvas.toDataURL();
    // send it on the wire
    send(stringData);
    // draw rectangle 
    drawVideoRect();
    // draw at next timeout
    drawTimer = setTimeout(extractVideoFrame);
};

function drawVideoRect() {
    if (!rect) {
        return;
    }
    ctx_out.fillStyle = "rgba(150, 50, 50, 0.5)";
    ctx_out.fillRect(rect.x, rect.y, rect.w, rect.h);
};


// frame based websocket communication 
var ws;

if('WebSocket' in window){
    connect('ws://' + location.hostname + (location.port ? ':'+location.port : '') + '/video');
} else {
    log ('web sockets not supported');
}

function connect(host) {
    ws = new WebSocket(host);
    ws.onopen = function () {
        log('connected');
    };

    ws.onclose = function (err) {
        //log('<span style="color: red;">ERROR:</span> ' + evt.data); 
        log('socket closed, error code: ' + err.code);
    };

    ws.onerror = function () { 
        log('There was an error with your websocket'); 
    };

    ws.onmessage = function (message) {
        //console.log(message.data);
        rect = JSON.parse(message.data);
    };
};

function send(msg) {
    if (ws == null || ws.readyState != 1) {
        //log('websocket not ready');
        return;
    }
    ws.send(msg);
};

// DOM object controllers 
function click_canvas() {
    if (video.paused) {
        video.play();
        extractVideoFrame();
    } else {
        video.pause();
        clearTimeout(drawTimer);
    }
};

