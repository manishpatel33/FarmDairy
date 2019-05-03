// this is for form validation
// u,e is for email and user name
// c is complusory feild
// p is for password validation
// rp is for repeat password
// t is for terms and condtion

function check_form(e) {
  var password = '';
  for (x in e) {
    var inc = 0;
    $('#' + x).removeClass('has-error');
    if (e[x] == 'e' || e[x] == 'u') {
      var re = (e[x] == 'u:') ? /(^|\s)((http(s)?:\/\/)[\w-]+(\.[\w-]+)+\.([a-z]{2,6}(?:\.[a-z]{2})?)(:\d+)?(\/\S*)?)/gi : /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
      if (!re.test($('#' + x).val().trim())) {
        $('#' + x).addClass('has-error');
        warning_msg($('#' + x).attr("data-err-title"), $('#' + x).attr("data-err-title") + " Is Not Proper", $('#' + x).attr("id") + "_err")
        $('#' + x).focus();
        inc++;
      }
    } else if (e[x] == 'c' && $('#' + x).val().trim() == '') {
      $('#' + x).addClass('has-error');
      $('#' + x).focus();
      warning_msg($('#' + x).attr("data-err-title"), $('#' + x).attr("data-err-title") + " Is Empty ", $('#' + x).attr("id") + "_err")
      inc++;
    } else if (e[x] == 't') {
      var checkbox = document.getElementById(x);
      if (!checkbox.checked) {
        //warning_msg("", "Check terms and conditions", "tcagree_war");
        $('#' + x).focus();
        inc++;
      }
    } else if (e[x] == 'p') {
      password = x;
      if ($('#' + x).val().trim().length < 8) {
        warning_msg($('#' + x).attr("data-err-title"), $('#' + x).attr("data-err-title") + " Is less than 8 char Please Enter More Than 8 ", $('#' + x).attr("id") + "_err")
        $('#' + x).addClass('has-error');
        $('#' + x).focus();
        inc++;
      }
    } else if (e[x] == 'rp') {
      if (password != '') {
        if ($('#' + x).val().trim() != $('#' + password).val().trim()) {
          $('#' + x).addClass('has-error');
          $('#' + x).focus();
          warning_msg("Repeat Password", "Both Password Is Not Matched", "repeat_pass_err")
          inc++;
        }
      }
    } else if (e[x] == 'd' && $('#' + x).val().trim() == '') {
      var name = $('#' + x).attr("data-name")
      $('#' + x).focus();
      inc++;
    } else {

    }
    if (inc > 0)
      return false;
  }

  return true;
}

//this function for remove word from input
function removeStringChar(which) {
  if (event.shiftKey == true)
    event.preventDefault();

  var code = event.keyCode;

  if ((code >= 48 && code <= 57) || (code >= 96 && code <= 105) || code == 8 || code == 9 || code == 37 || code == 39 || code == 46 || code == 190 || code == 110) {
    // allowed characters
  } else
    event.preventDefault();

  if ($(which).val().indexOf('.') !== -1 && (code == 190 || code == 110))
    event.preventDefault();
}

function isNumber(which) {
  if (event.shiftKey == true)
    event.preventDefault();

  var code = event.keyCode;

  if ((code >= 48 && code <= 57) || (code >= 96 && code <= 105) || code == 8 || code == 9 || code == 37 || code == 39 || code == 46) {
    // allowed characters
  } else
    event.preventDefault();


}

// to show error msg show this function
//title = msg title
//message = message to be shown
//id =  to give that id to msg 
async function error_msg(title, message, id) {
  $("#" + id).remove();
  iziToast.error({
    title: title,
    message: message,
    timeout: 5000,
    position: 'topRight',
    id: id
  });
}

// to show sucsses msg show this function
async function success_msg(title, message, id) {
  $("#" + id).remove();
  iziToast.success({
    title: title,
    message: message,
    timeout: 5000,
    position: 'topRight',
    id: id
  });
}

// to show info msg show this function
async function info_msg(title, message, id) {
  $("#" + id).remove();
  iziToast.info({
    title: title,
    message: message,
    timeout: 5000,
    position: 'topRight',
    id: id
  });
}

// to show error warining show this function
async function warning_msg(title, message, id) {
  $("#" + id).remove();
  iziToast.warning({
    title: title,
    message: message,
    timeout: 5000,
    position: 'topRight',
    id: id
  });

}