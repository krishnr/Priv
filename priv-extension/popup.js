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
}

// The chrome.storage API is used. This is different
// from the window.localStorage API, which is synchronous and stores data bound
// to a document's origin. Also, using chrome.storage.sync instead of
// chrome.storage.local allows the extension data to be synced across multiple
// user devices.
document.addEventListener('DOMContentLoaded', () => {
  getCurrentTabUrl((url) => {
    var span = document.getElementById('site-title');
    // span.innerHTML = page_title;
    span.innerHTML = getDomain(page_url);
    displayPrivacySummary(page_url);
  });
});

function displayPrivacySummary(page_url) {
  var xhr = new XMLHttpRequest();
  var domain = getDomain(page_url);

  xhr.open("GET", "http://localhost:5000/summarize?hostname=" + domain, true);
  xhr.onload = function (e) {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        var res = JSON.parse(xhr.response);

        formatSummary(res['summary']);
        formatAction(res['action']);
      } else {
        defaultDisplay(domain);
      }
    }
  };
  xhr.onerror = function (e) {
    console.error(xhr.statusText);
    defaultDisplay(domain);
  };
  xhr.send(null);
}

function getDomain(url) {
  var parse = document.createElement('a');
  parse.href = url;
  address = parse.hostname.split(".")
  domain = address[address.length - 2] || address[0];
  return domain;
}

function formatSummary(data) {
  Object.keys(data).forEach(function(key, index) {
    var question = '<span class="question">' + key + '</span>';
    var answer_yes = '<span class="answer yes">Yes</span>';
    var answer_no = '<span class="answer no">No</span>';
    var answer_maybe = '<span class="answer maybe">Maybe</span>';

    paragraph = document.createElement('p');
    paragraph.className = 'clear';
    paragraph.innerHTML = question;

    switch(this[key]) {
      case 'yes':
          paragraph.innerHTML += answer_yes;
          break;
      case 'no':
          paragraph.innerHTML += answer_no;
          break;
      case 'maybe':
          paragraph.innerHTML += answer_maybe;
      default:
          // Unsupported answer
    }

    var items = document.getElementById("items");
    items.appendChild(paragraph);
  }, data);
}

function formatAction(link, type) {
  document.getElementById("action").href=link; 
}

function defaultDisplay(domain) {
  // page title
  var title = document.getElementById("title");
  title.innerHTML = "We don't currently have information about the " + "<span id='site-title'>" + domain + "</span> privacy policy!";
  // remove action button
  var action = document.getElementById("action");
  action.style.display = 'none';
  // make window smaller
  var body = document.getElementById("body");
  body.style.minHeight = '120px';

}