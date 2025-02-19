"use strict";

const serverUrl = "http://127.0.0.1:8000";

async function uploadImage() {
    let file = document.getElementById("file").files[0];
    
    // Add validation
    if (!file) {
        throw new Error("Please select an image file first");
    }

    let converter = new Promise(function(resolve, reject) {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result
            .toString().replace(/^data:(.*,)?/, ''));
        reader.onerror = (error) => reject(error);
    });
    let encodedString = await converter;

    // Clear file upload input field
    document.getElementById("file").value = "";

    // Make server call to upload image
    // and return the server upload promise
    return fetch(serverUrl + "/images", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({filename: file.name, filebytes: encodedString})
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new HttpError(response);
        }
    })
}

function updateImage(image) {
    document.getElementById("view").style.display = "block";

    let imageElem = document.getElementById("image");
    imageElem.src = image["fileUrl"];
    imageElem.alt = image["fileId"];

    return image;
}

function translateImage(image) {
    // Make server call to translate image and return the server upload promise
    return fetch(serverUrl + "/images/" + image["fileId"] + "/headlines", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({fromLang: "auto", toLang: "en"})
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new HttpError(response);
        }
    })
}

function synthesizeSpeech(text, languageCode = 'en-US') {
    return fetch(serverUrl + "/text/synthesize", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            text: text,
            languageCode: languageCode
        })
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new HttpError(response);
        }
    });
}

function playAudio(audioUrl) {
    const audio = document.getElementById('audioPlayer');
    audio.src = audioUrl;
    audio.play();
}

function getLanguageName(languageCode) {
    const languageNames = {
        'es': 'Spanish',
        'en': 'English',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'zh': 'Chinese',
        'ar': 'Arabic',
        'hi': 'Hindi',
        'auto': 'Auto-detected'
        // Add more languages as needed
    };
    return languageNames[languageCode] || languageCode;
}

function annotateImage(translations) {
    let translationsElem = document.getElementById("translations");
    
    // Update the line count at the beginning
    document.getElementById("lineCount").textContent = `${translations.length} line${translations.length !== 1 ? 's' : ''}`;
    
    // Clear previous translations
    while (translationsElem.firstChild) {
        translationsElem.removeChild(translationsElem.firstChild);
    }
    
    // Iterate over translations
    for (let i = 0; i < translations.length; i++) {
        let translationContainer = document.createElement("div");
        translationContainer.className = "translation-item";

        // Create container for detected language with label
        let languageInfo = document.createElement("span");
        languageInfo.className = "w3-tag w3-small w3-blue-grey";
        languageInfo.style.marginRight = "10px";
        let languageLabel = document.createElement("strong");
        languageLabel.textContent = "Language of the original text: ";
        languageInfo.appendChild(languageLabel);
        
        // Retrieve the language code with fallback logic:
        let detectedLang = translations[i]["translation"]["detectedSourceLanguage"];
        if (!detectedLang && translations[i]["translation"]["sourceLanguage"]) {
            detectedLang = translations[i]["translation"]["sourceLanguage"];
        }
        if (!detectedLang) {
            detectedLang = "auto";
        }
        const languageName = getLanguageName(detectedLang);
        languageInfo.appendChild(document.createTextNode(languageName));

        let translationElem = document.createElement("h6");
        translationElem.appendChild(languageInfo);
        translationElem.appendChild(document.createTextNode(
            translations[i]["text"] + " → " + translations[i]["translation"]["translatedText"]
        ));

        let playButton = document.createElement("button");
        playButton.className = "w3-button w3-circle w3-blue-grey";
        playButton.innerHTML = "🔊";
        playButton.onclick = () => {
            synthesizeSpeech(translations[i]["translation"]["translatedText"])
                .then(audioInfo => playAudio(audioInfo.fileUrl))
                .catch(error => alert("Error: " + error));
        };

        translationContainer.appendChild(translationElem);
        translationContainer.appendChild(playButton);
        translationsElem.appendChild(translationContainer);
        translationsElem.appendChild(document.createElement("hr"));
    }
}

function uploadAndTranslate() {
    // Modify error handling to show friendlier messages
    uploadImage()
        .then(image => updateImage(image))
        .then(image => translateImage(image))
        .then(translations => annotateImage(translations))
        .catch(error => {
            if (error.message === "Please select an image file first") {
                alert(error.message);
            } else {
                alert("Error: " + error);
            }
        });
}

class HttpError extends Error {
    constructor(response) {
        super(`${response.status} for ${response.url}`);
        this.name = "HttpError";
        this.response = response;
    }
}
