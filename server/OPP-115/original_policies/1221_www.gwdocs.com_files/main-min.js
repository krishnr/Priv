function formInputClasses(){jQuery('input[type="text"]').addClass("text");jQuery('input[type="password"]').addClass("text");jQuery('input[type="checkbox"]').addClass("checkbox");jQuery('input[type="radio"]').addClass("radiobutton");jQuery('input[type="submit"]').addClass("submit");jQuery('input[type="image"]').addClass("buttonImage")}function placeholderPolyfill(){jQuery("input, textarea").placeholder()}jQuery.noConflict();jQuery(document).ready(function(){formInputClasses();placeholderPolyfill();Modernizr&&!Modernizr.borderradius&&function(e){e(".round-icon").each(function(){var t=e(this),n=t.attr("class");t.append('<span class="'+n+'"/>')})}(jQuery)});