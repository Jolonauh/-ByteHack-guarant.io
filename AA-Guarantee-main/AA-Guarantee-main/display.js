// Send a message to the active tab in the main window
chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    const activeTab = tabs[0];
    chrome.tabs.sendMessage(activeTab.id, { key: 'value' }, function(response) {
      console.log('Received response:', response);
    });
  });