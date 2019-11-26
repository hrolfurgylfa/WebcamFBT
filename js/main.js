"use strict";

const videoWidth = 1000;
const videoHeight = videoWidth/16*9;
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

let getPartLocationWithName = (name, pose) => {
    let bodyPart = pose.keypoints.find(bodyPart => bodyPart.part = name);

    if (bodyPart != undefined) {
        return bodyPart.position;
    } else {
        return null;
    }
}

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
    
    // const net = await posenet.load({
    //     architecture: 'ResNet50',
    //     outputStride: 32,
    //     inputResolution: { width: 257, height: 200 },
    //     quantBytes: 2
    // });
    const net = await posenet.load({
        architecture: 'MobileNetV1',
        outputStride: 16,
        inputResolution: { width: 640, height: 480 },
        multiplier: 0.75
    });
    console.log("Posenet hlaðið inn:",net);
    
    const video = await loadVideo();
    console.log("Video hlaðið inn:",video);

    async function poseDetectionFrame() {

        if (programSettings.stop) { return null; }

        let pose = await net.estimateSinglePose(video, poseSettings);

        // Filtera gögn til þess að vera ekki með auka punkta sem eru með mjög lága prósentu
        let i = 0;
        while (i < pose.keypoints.length) {
            if (pose.keypoints[i].score < poseSettings.bodyPartConfidenceRequirement) {
                pose.keypoints.splice(i, 1);
            } else {
                i++
            }
        }

        // Reikna hvar hip er
        let hip_points = pose.keypoints.filter(bodyPart => bodyPart.part.slice(-3) === "Hip");
        if (hip_points.length === 2) {
            let hip = {
                position: {
                  y: ( hip_points[0].position.y + hip_points[1].position.y ) / 2,
                  x: ( hip_points[0].position.x + hip_points[1].position.x ) / 2
                },
                part: "Hip",
                score: ( hip_points[0].score + hip_points[1].score ) / 2
            }
            pose.keypoints.push(hip);
        }

        const nececery_locations = {
            "hip": getPartLocationWithName("Hip", pose),
            "left_foot": getPartLocationWithName("leftAnkle", pose),
            "right_foot": getPartLocationWithName("rightAnkle", pose)
        }
        
        // Senda göbgn á Pyton serverinn
        let JSONResopnse = await fetch("http://localhost:8080/data", {
            method: 'POST',
            body: JSON.stringify(nececery_locations),
        });

        // let SteamVR_pose = await fetch(JSONResopnse.url);
        // SteamVR_pose = await SteamVR_pose.json();

        // Gera allskonar logging stuff ef það er kveikt á logging í stillingunum
        // Logga JS pose
        if (programSettings.logging) {
            // console.log(pose);
            
            ctx.clearRect(0, 0, videoWidth, videoHeight);

            ctx.fillStyle = "red";
            pose.keypoints.forEach(bodyPart => {
                ctx.fillRect(bodyPart.position.x, bodyPart.position.y, 10, 10);
            });
        }
        
        // Logga SteamVR pose
        // if (programSettings.logging) {
        //     // console.log(SteamVR_pose);

            
        //     ctx.fillStyle = "blue";
        //     for (i = 0; i < SteamVR_pose.length; i++) {
        //         let device = SteamVR_pose[i]
        //         let translated_x = (device[0]*900) + (videoWidth / 2)
        //         let translated_y = (device[1]*500)

        //         console.log("Device: "+i+
        //             "\nX: "+translated_x+
        //             "\nY: "+translated_y
        //         );

        //         ctx.fillRect(translated_x, translated_y, 10, 10);
        //     }
        // }

        requestAnimationFrame(poseDetectionFrame);
        
    }
    
    poseDetectionFrame();
}

stopBtn.addEventListener("click", () => {
    programSettings.stop = true;
    document.write("<h1 style='text-align: center;'>Program stopped, reload to restart program</h1>");
});

startDetection();