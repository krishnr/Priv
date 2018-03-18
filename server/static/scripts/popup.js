var page_url = '';
var page_title = '';
var policy_header_text = 'Quote from Privacy Policy';

document.addEventListener('DOMContentLoaded', () => {
  displayPrivacySummary(page_url);
});

// Response format:
// "summary": {
//   "question": ["answer", "specific text machine learning algorithm identified"],
//   },
// "action": "clickety click motherfuckers"
// }
function displayPrivacySummary(page_url) {
  formatSummary(res['summary']);
  formatAction(res['action']);
  defaultDisplay(domain);
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