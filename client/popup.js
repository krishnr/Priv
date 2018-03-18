var page_url = '';
var page_title = '';
var policy_header_text = 'Quote from Privacy Policy';

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

// Response format:
// "summary": {
//   "question": ["answer", "specific text machine learning algorithm identified"],
//   },
// "action": "clickety click motherfuckers"
// }
function displayPrivacySummary(page_url) {
  var xhr = new XMLHttpRequest();
  var domain = getDomain(page_url);

  // Change to localhost below in order to run on development server
  //xhr.open("GET", "http:localhost:80/summarize?hostname=" + domain, true);
  xhr.open("GET", "http://ec2-18-219-251-103.us-east-2.compute.amazonaws.com:80/summarize?hostname=" + domain, true);
  xhr.onload = function (e) {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        var res = JSON.parse(xhr.response); // comment back in when backend returns this format of response
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
  var answer_yes = '<span class="answer yes">Yes</span>';
  var answer_no = '<span class="answer no">No</span>';
  var answer_maybe = '<span class="answer maybe">Maybe</span>';

  Object.keys(data).slice(0, 7).forEach(function(key, index) {
    var question = '<span class="question"><a href="#">' + key + '</a></span>';

    paragraph = document.createElement('p');
    paragraph.className = 'clear';
    paragraph.innerHTML = question;

    switch(this[key][0]) {
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

    // adjust heights for two-line sentences
    if (key.length > 45) {
      paragraph.lastChild.className += ' double-line-height';
    }

    createDropdown(paragraph, this[key][1], this[key][2], index);

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
  var question_prompt = document.getElementById("question-prompt");
  question_prompt.style.display = 'none';
  // remove action button
  var action = document.getElementById("action");
  action.style.display = 'none';
  // hide summary space
  var cta = document.getElementsByClassName("parent")[0];
  cta.style.margin = '0px';
  // hide container
  var cta = document.getElementsByClassName("cta")[0];
  cta.style.height = '14px';
  // make window smaller
  var body = document.getElementById("body");
  body.style.minHeight = '120px';
}

function createDropdown(paragraph, question_content, content, index) {
  q_desc_class = "question-description";
  dropdown_class = "dropdown";
  policy_header_class = "policy_header";
  policy_class ="policy";

  dropdown = document.createElement('div');
  dropdown.id = dropdown_class + '-' + index;
  dropdown.className = dropdown_class;
  dropdown.style.display = 'none';

  question_description = document.createElement('div');
  question_description.id = q_desc_class + "-" + index;
  question_description.className = q_desc_class;
  question_description.innerHTML = question_content;

  policy_header = document.createElement('div');
  policy_header.id = policy_header_class + '-' + index;
  policy_header.className = policy_header_class;
  policy_header.innerHTML = policy_header_text;

  policy = document.createElement('div');
  policy.id = policy_class + '-' + index;
  policy.className = policy_class;
  policy.innerHTML = content;

  dropdown.appendChild(question_description);
  dropdown.appendChild(policy_header);
  dropdown.appendChild(policy);
  paragraph.appendChild(dropdown);
  // toggle display on click, ugh I wish I used react now
  paragraph.addEventListener('click', function(e) {
    // Stop redirect to top of page
    e.preventDefault();
    dropdown_click = document.getElementById(dropdown_class + '-' +index);
    if (dropdown_click.style.display === 'none') {
      dropdown_click.style.display = 'block';
    } else {
      dropdown_click.style.display = 'none';
    }
  });
}