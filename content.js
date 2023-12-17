chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    //listens to the messsage sent from the script.js 
    if (request.action === "getSelectionText") { //checks whether the message has the property "action" that is equal to "getSelectionText"
      var selection = window.getSelection(); //retrieves the selected text from the webpage
      var text = selection.toString().trim(); //converts the selection object to String and then trim it
      chrome.runtime.sendMessage({ action: "sendSelectionText", text: text }); //messages back an object with property 'action' set to "sendSelectionText" and "text" containing the final trimmed text
    }
  });
  