import https from "node:https";

const youtubeVideoExists = (videoId) => new Promise((resolve, reject) => {
    try {
        const req = https.request({
            method: "HEAD",
            host: "img.youtube.com",
            path: `/vi/${videoId}/mqdefault.jpg`,
        }, (res) => resolve(res.statusCode));
        req.on("error", err => reject(err));
        req.end();
    } catch (err) {
        reject(err);
    };
});

const ids = ["8jPfy4wbfaQ", "oFagihfZslU", "FagihfZslUZ", "agihfZslUZH", "gihfZslUZH0", "ihfZslUZH0f", "hfZslUZH0f4", "fZslUZH0f4f", "ZslUZH0f4fP", "slUZH0f4fPb", "lUZH0f4fPbg", "UZH0f4fPbgQ", "ZH0f4fPbgQi", "H0f4fPbgQiz", "0f4fPbgQizH", "f4fPbgQizH9", "4fPbgQizH9n", "fPbgQizH9na", "PbgQizH9naM", "bgQizH9naMl", "gQizH9naMlh", "QizH9naMlh9", "izH9naMlh9y", "zH9naMlh9y9", "H9naMlh9y9f", "9naMlh9y9fZ", "naMlh9y9fZn", "aMlh9y9fZnj", "Mlh9y9fZnjL", "lh9y9fZnjLX", "h9y9fZnjLXk", "9y9fZnjLXkA"];
for (let i = 0; i < ids.length; i++) {
    const id = ids[i];
    console.log(`Checking video ${i + 1} of ${ids.length}: ${id}`);
    try {
        const exists = await youtubeVideoExists(id);
        console.log(`Video ID: ${id} - Exists: ${exists}`);
    } catch (err) {
        console.error(`Error checking video ID: ${id} - ${err}`);
    };
};