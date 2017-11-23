var page_url = '';
var page_title = '';

/**
 * Get the current URL.
 *
 * @param {function(string)} callback called when the URL of the current tab
 *   is found.
 */
function getCurrentTabUrl(callback) {
  // Query filter to be passed to chrome.tabs.query - see
  // https://developer.chrome.com/extensions/tabs#method-query
  var queryInfo = {
    active: true,
    currentWindow: true
  };

  chrome.tabs.query(queryInfo, (tabs) => {
    // chrome.tabs.query invokes the callback with a list of tabs that match the
    // query. When the popup is opened, there is certainly a window and at least
    // one tab, so we can safely assume that |tabs| is a non-empty array.
    // A window can only have one active tab at a time, so the array consists of
    // exactly one tab.
    var tab = tabs[0];

    // A tab is a plain object that provides information about the tab.
    // See https://developer.chrome.com/extensions/tabs#type-Tab
    var url = tab.url;
    page_url = url;
    page_title = tab.title;

    // tab.url is only available if the "activeTab" permission is declared.
    // If you want to see the URL of other tabs (e.g. after removing active:true
    // from |queryInfo|), then the "tabs" permission is required to see their
    // "url" properties.
    console.assert(typeof url == 'string', 'tab.url should be a string');

    callback(url);
  });

  // Most methods of the Chrome extension APIs are asynchronous. This means that
  // you CANNOT do something like this:
  //
  // var url;
  // chrome.tabs.query(queryInfo, (tabs) => {
  //   url = tabs[0].url;
  // });
  // alert(url); // Shows "undefined", because chrome.tabs.query is async.
}

/**
 * Change the background color of the current page.
 *
 * @param {string} color The new background color.
 */
function changeBackgroundColor(color) {
  var script = 'document.body.style.backgroundColor="' + color + '";';
  // See https://developer.chrome.com/extensions/tabs#method-executeScript.
  // chrome.tabs.executeScript allows us to programmatically inject JavaScript
  // into a page. Since we omit the optional first argument "tabId", the script
  // is inserted into the active tab of the current window, which serves as the
  // default.
  chrome.tabs.executeScript({
    code: script
  });
}

/**
 * Gets the saved background color for url.
 *
 * @param {string} url URL whose background color is to be retrieved.
 * @param {function(string)} callback called with the saved background color for
 *     the given url on success, or a falsy value if no color is retrieved.
 */
function getSavedBackgroundColor(url, callback) {
  // See https://developer.chrome.com/apps/storage#type-StorageArea. We check
  // for chrome.runtime.lastError to ensure correctness even when the API call
  // fails.
  chrome.storage.sync.get(url, (items) => {
    callback(chrome.runtime.lastError ? null : items[url]);
  });
}

// The chrome.storage API is used. This is different
// from the window.localStorage API, which is synchronous and stores data bound
// to a document's origin. Also, using chrome.storage.sync instead of
// chrome.storage.local allows the extension data to be synced across multiple
// user devices.
document.addEventListener('DOMContentLoaded', () => {
  getCurrentTabUrl((url) => {
    var span = document.getElementById('site-title');
    span.innerHTML = page_title;
    displayPrivacySummary();
  });
});

function displayPrivacySummary() {
  var xhttp = new XMLHttpRequest();
  console.log(page_url);
  // xhttp.open("GET", "http://127.0.0.1:5000/", false);
  // xhttp.setRequestHeader("Content-type", "application/json");
  // xhttp.send();
  // var banana = JSON.parse(xhttp.response)
  
  var response = {
    collection: { // (What information is being collected?) (Notice, Consent)
      score: 1, 
      more_info: {
        label_1: "blah1",
        label_2: "blah2",
        label_3: "blah3"
      }
    },
    use: { // (How is this information being used?) (Purpose)
      score: 2, 
      more_info: {
        label_1: "blah1",
        label_2: "blah2",
        label_3: "blah3"
      }
    }, 
    disclosure: { // Disclosure/Information Sharing (Who has access to this data?) (Disclosure, Security)
      score: 3, 
      more_info: {
        label_1: "blah1",
        label_2: "blah2",
        label_3: "blah3"
      }
    },
    choice: { // Choices (What can you do if policy isn’t followed?) (Accountability)
      score: 4, 
      more_info: {
        label_1: "blah1",
        label_2: "blah2",
        label_3: "blah3"
      }
    }
  };
  formatCollection(response.collection, 'collection');
  formatCollection(response.use, 'use');
  formatCollection(response.disclosure, 'disclosure');
  formatCollection(response.choice, 'choice');
}

function formatCollection(data, type) {
  var text = []
  var labels = [data.more_info.label_1, data.more_info.label_2, data.more_info.label_3];

  for (var i = 0; i < 3; i++) { // no good way to get length of object in JS so hardcore to 3
    text[i] = document.getElementById(type + '_' + i);
    text[i].innerHTML = "<i class='em em-point_right'></i> " + labels[i];
  }
}