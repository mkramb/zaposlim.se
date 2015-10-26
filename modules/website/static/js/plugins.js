$.mustache = function(template, view, partials) {
  return Mustache.to_html(template, view, partials);
};

// custom X-CSRFToken header
$(document).ajaxSend(function(event, xhr, settings) {
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type)) {
        xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
    }
});

$.ajaxSetup({
	crossDomain: false,
	cache: 		 false
});

function reloadBanners() {
  var time = (new Date()).getTime();

  for (var i=0;  $('#banner_' + i).length > 0; i++) {
    var banner = $('#banner_' + i);

    banner.get(0).src =
   banner.get(0).src.split('?')[0] + '?' + time;
  }
}

$.fn.clearForm = function() {
  return this.each(function() {
    var type = this.type,
      tag = this.tagName.toLowerCase(),
      css = this.className;

      if (tag == 'form') {
        $('label.error').remove();
        return $(':input',this).clearForm();
      }

      if (css.indexOf('dont-clear') < 0) {
          if (type == 'text' || type == 'password') {
              this.value = '';
          }
          else if (tag == 'textarea') {
              this.value = '';
          }
          else if (type == 'checkbox' || type == 'radio') {
              this.checked = false;
          }
          else if (tag == 'select') {
              $(this).val('').change();
          }
      }
  });
};

function getBaseURL() {
    var url = location.href;  // entire url including querystring - also: window.location.href;
    var baseURL = url.substring(0, url.indexOf('/', 14));

    if (baseURL.indexOf('http://localhost') != -1) {
        // Base Url for localhost
        var url = location.href;  // window.location.href;
        var pathname = location.pathname;  // window.location.pathname;
        var index1 = url.indexOf(pathname);
        var index2 = url.indexOf("/", index1 + 1);
        var baseLocalUrl = url.substr(0, index2);

        return baseLocalUrl + "/";
    }
    else {
        // Root Url for domain name
        return baseURL + "/";
    }
}

window.special = {
  '%20' : new RegExp(' ', 'g'),
  '%3F' : new RegExp('\\?', 'g'),
  '%26' : new RegExp('&', 'g'),
  '%3D' : new RegExp('=', 'g')
}

function escapeRE(s) {
  s = s.toString();

  _.each(window.special, function(from, to) {
    s = s.replace(from, to);
  });

  return s;
}
