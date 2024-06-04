const mic_btn = document.querySelector('#mic');
const playback = document.querySelector('.playback');

mic_btn.addEventListener('click', ToggleMic);

let can_record = false;
let is_recording = false;

let recorder = null;

let chunks = [];

function SetupAudio(){
    console.log("SetupAudio Start")
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia){
        navigator.mediaDevices
            .getUserMedia({
                audio: true
                })
            .then(SetupStream)
            .catch(err=>{
                console.error(err)
            });
    }
    console.log("SetupAudio End")
}

SetupAudio();

function SetupStream(stream){
    console.log("SetupStream Start")
    recorder = new MediaRecorder(stream);

    recorder.ondataavailable = e => {
        chunks.push(e.data);
    }

    recorder.onstop = e => {
        const blob = new Blob(chunks, { type: "audio/wav; codecs=opus" });
        chunks = [];
        const audioURL = window.URL.createObjectURL(blob);
        playback.src = audioURL;

        // Create a FormData object and append the file
        let formData = new FormData();
        formData.append('audioFile', blob, 'recording.wav');

        // Send the FormData object to the server via AJAX
        fetch('/upload_audio', { // The URL of your Flask endpoint
            method: 'POST',
            body: formData
        }).then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error(error));
    }

    can_record = true;
    console.log("SetupStream End")
}

function ToggleMic(){
    console.log("ToggleMic Start")
    if(!can_record) return;
    is_recording = !is_recording;

    if(is_recording){
        console.log("ToggleMic > if start")
        recorder.start();
        mic_btn.classList.add("is-recording");
        console.log("ToggleMic > if end")
    }
    else{
        console.log("ToggleMic > else start")
        recorder.stop();
        mic_btn.classList.remove("is-recording");
        console.log("ToggleMic > else end")
    }
    console.log("ToggleMic End")
}
