document.addEventListener("DOMContentLoaded", function () {

  var emotionButton = document.getElementById("content");

  if (emotionButton) {
    emotionButton.addEventListener("click", function () {
      chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        chrome.tabs.sendMessage(tabs[0].id, { action: "getSelectionText" });
      });
    });
  } else {
    console.error("Button not found.");
  }
});

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action === "sendSelectionText") {
    var text = request.text;
    console.log("Selected Text: ", text);
    postSelectedText(text);
  }
});

async function postSelectedText(text) {
  if (text.length === 0) {
    console.log("No text selected.");
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/process_emotion", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text }),
    });

    // Check if the response was successful
    if (response.ok) {
      const data = await response.text(); 
      // Display the result on the frontend
      document.getElementById('text z').innerHTML = data;
    } else {
      console.error("Request failed with status code:", response.status);
      const errorText = await response.text();
      console.error("Error response:", errorText);
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

