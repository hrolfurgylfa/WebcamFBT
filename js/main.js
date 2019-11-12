"use strict";

const videoWidth = window.innerWidth;
const videoHeight = window.innerHeight;
const video = document.getElementById('video');
const stopBtn = document.getElementById("stop_btn");

let programSettings = {
    stop: false,
    logging: true
};
const poseSettings = {
    flipHorizontal: true,
    bodyPartConfidenceRequirement: 0.5
}


console.log(video);

async function setupCamera() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      throw new Error(
          'Browser API navigator.mediaDevices.getUserMedia not available');
    }

    video.width = videoWidth;
    video.height = videoHeight;

    const stream = await navigator.mediaDevices.getUserMedia({
        'audio': false,
        'video': {
            facingMode: 'user',
            width: videoWidth,
            height: videoHeight,
        },
    });

    video.srcObject = stream;
  
    return new Promise(resolve => {
        video.onloadedmetadata = () => {
            resolve(video);
        };
    });
}

async function loadVideo() {
    const video = await setupCamera();
    video.play();
  
    return video;
}

async function startDetection() {
    console.log("Byrja detection");
    
    // Gera canvas tilbúinn til þess að sýna smá output
    const canvas = document.getElementById('output');
    canvas.width = videoWidth;
    canvas.height = videoHeight;
    const ctx = canvas.getContext("2d");
    
    const net = await posenet.load({
        architecture: 'ResNet50',
        outputStride: 32,
        inputResolution: { width: 257, height: 200 },
        quantBytes: 2
    });
    console.log("Posenet hlaðið inn:",net);
    
    const video = await loadVideo();
    console.log("Video hlaðið inn:",video);

    async function poseDetectionFrame() {

        if (programSettings.stop) { return null; }

        const pose = await net.estimateSinglePose(video, poseSettings);

        // Filtera gögn til þess að vera ekki með auka punkta sem eru með mjög lága prósentu
        let i = 0;
        while (i < pose.keypoints.length) {
            if (pose.keypoints[i].score < poseSettings.bodyPartConfidenceRequirement) {
                pose.keypoints.splice(i, 1);
            } else {
                i++
            }
        }
        
        // Gera allskonar logging stuff ef það er kveikt á logging í stillingunum
        if (programSettings.logging) {
            console.log(pose);
            
            ctx.clearRect(0, 0, videoWidth, videoHeight);

            ctx.fillStyle = "red";
            pose.keypoints.forEach(bodyPart => {
                ctx.fillRect(bodyPart.position.x, bodyPart.position.y, 10, 10);
            });
        }
        
        // Senda göbgn á Pyton serverinn
        await window.fetch("http://localhost:8080/data", {
            method: 'POST',
            body: JSON.stringify(pose),
        });

        requestAnimationFrame(poseDetectionFrame);
        
    }
    
    poseDetectionFrame();
}

stopBtn.addEventListener("click", () => {
    programSettings.stop = true;
    document.write("<h1 style='text-align: center;'>Program stopped, reload to restart program</h1>");
});

startDetection();