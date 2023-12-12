let jsonData;
let current;
let next;
let current_tiltify = null;
let current_twitch = null;
let twitchPlayer;
window.current = current;
window.current_tiltify = current_tiltify;
window.current_twitch = current_twitch;

function resizeTwitchEmbed() {
    const container = document.getElementById("main-content");
    const embedElement = document.getElementById("twitch-embed");

    // Calculate the new width and height based on the container size
    const containerWidth = container.clientWidth;
    const viewportHeight = window.innerHeight; // Get the viewport height
    let newWidth, newHeight;

    if (containerWidth <= 800) {
        // If the container width is small, use a 9:16 aspect ratio based on viewport height
        newWidth = containerWidth * 0.8;
        newHeight = viewportHeight * 0.7; // Example: 50% of the viewport height
    } else {
        if (containerWidth * 0.9 > 1000) {
            newWidth = 1000;
            newHeight = newWidth / 2;
        } else {
            newWidth = containerWidth * 0.9;
            newHeight = newWidth / 2;
        }
    }

    // Update the embed dimensions
    embedElement.style.width = newWidth + "px";
    embedElement.style.height = newHeight + "px";
}


// Resize the Twitch embed initially and on window resize
resizeTwitchEmbed();
window.addEventListener("resize", resizeTwitchEmbed);

const sheets =  'https://script.google.com/macros/s/AKfycbyPq8GYC6KiWjbreMVYiPty5B4AQZvJx8Xhmkq1Vp2SkPYht41o4NyrAyQ2qyxNEoVK/exec'



function findActive() {
    return fetch(sheets)
        .then(response => response.json())
        .then(streamers => {
            console.log(streamers)

            for (let i = 0; i < streamers.length; i++) {
                let time = Date.now();

                if (time >= streamers[i].Time && time <= streamers[i + 1].Time) {
                    current = streamers[i].Streamer;
                    next = streamers[i + 1].Streamer;
                    current_tiltify = streamers[i].Tiltify;
                    current_twitch = streamers[i].Twitch;
                    duration = streamers[i + 1].Time - time;
                    window.current = current;
                    window.current_tiltify = current_tiltify;
                    window.current_twitch = current_twitch;
                    console.log("Current:", current);
                    console.log("Next:", next);
                    updateTwitchEmbed(current); // Update the Twitch embed with the current streamer
                    setTimeout(findActive, duration); // Check again after 'duration' milliseconds
                    break;
                }
            }
        });



    }

function initializeTwitchEmbed() {
    twitchPlayer = new Twitch.Embed("twitch-embed", {
        width: "100%",
        height: "100%",
        channel: "Duckisaurus", // Placeholder channel name
        parent: ["embed.example.com", "othersite.example.com"]
    });
}

function updateTwitchEmbed(channelName) {
    if (twitchPlayer) {
        twitchPlayer.setChannel(channelName); // Update the channel
    }
}



initializeTwitchEmbed(); // Initialize the Twitch embed on page load
findActive(); // Start the process to find the active streamer


