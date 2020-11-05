
jQuery(document).ready(function($) {
  "use strict";

  //Contact
  $('form.contactForm').submit(function(event) {
    event.preventDefault();
    var f = $(this).find('.form-group'),
      ferror = false,
      emailExp = /^(0*100{1,1}\.?((?<=\.)0*)?%?$)|(^0*\d{0,2}\.?((?<=\.)\d*)?%?)$/g;

    f.children('input').each(function() { // run all inputs

      var i = $(this); // current input
      var rule = i.attr('data-rule');

      if (rule !== undefined) {
        var ierror = false; // error flag for current input
        var pos = rule.indexOf(':', 0);
        if (pos >= 0) {
          var exp = rule.substr(pos + 1, rule.length);
          rule = rule.substr(0, pos);
        } else {
          rule = rule.substr(pos + 1, rule.length);
        }

        switch (rule) {
          case 'required':
            if (i.val() === '') {
              ferror = ierror = true;
            }
            break;

          case 'minlen':
            if (i.val().length < parseInt(exp)) {
              ferror = ierror = true;
            }
            break;

          case 'email':
            if (!emailExp.test(i.val())) {
              ferror = ierror = true;
            }
            break;

          case 'checked':
            if (! i.is(':checked')) {
              ferror = ierror = true;
            }
            break;

          case 'regexp':
            exp = new RegExp(exp);
            if (!exp.test(i.val())) {
              ferror = ierror = true;
            }
            break;
        }
        i.next('.validation').html((ierror ? (i.attr('data-msg') !== undefined ? i.attr('data-msg') : 'wrong Input') : '')).show('blind');
      }
    });
    f.children('option').each(function() { // run all inputs

      var i = $(this); // current input
      var rule = i.attr('data-rule');

      if (rule !== undefined) {
        var ierror = false; // error flag for current input
        var pos = rule.indexOf(':', 0);
        if (pos >= 0) {
          var exp = rule.substr(pos + 1, rule.length);
          rule = rule.substr(0, pos);
        } else {
          rule = rule.substr(pos + 1, rule.length);
        }

        switch (rule) {
          case 'required':
            if (i.val() === '') {
              ferror = ierror = true;
            }
            break;

          case 'select':
            if (i.val() === "1") {
              ferror = ierror = true;
            }
            break;
        }
        i.next('.validation').html((ierror ? (i.attr('data-msg') != undefined ? i.attr('data-msg') : 'wrong Input') : '')).show('blind');
      }
    });
    if (ferror) return false;
    else var str = $(this).serialize();

   
    var action = $(this).attr('action');
    
    

  //var csrftoken = Cookies.get('csrftoken');
    if( ! action ) {
      action = ' https://thawing-spire-41307.herokuapp.com/hilmus/ajax/submit-contacts/'
    }
    $.ajax({
      type: "POST",
      url: action,
      data: str,
      dataType:'json',
      success: function(data) {
        
        if (data.message == 'OK') {
          $("#sendmessage").addClass("show");
          $("#errormessage").removeClass("show");
          $("#successmessage").addClass("show");
          $("#successmessage").html(data.text);
          $('.contactForm').find("input, textarea").val("");
        } else {
          $("#sendmessage").removeClass("show");
          $("#errormessage").addClass("show");
          $('#errormessage').html(data.message);
        }

      }
    });
    return false;
  });

});
