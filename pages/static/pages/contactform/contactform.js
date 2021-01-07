jquery3(document).ready(function($) {
  "use strict";

  //Contact
  jquery3('form#ajaxForm').submit(function(event) {
    event.preventDefault();
    var f = jquery3(this).find('.form-group'),
      ferror = false,
      emailExp = /^[^\s()<>@,;:\/]+@\w[\w\.-]+\.[a-z]{2,}$/i;

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
    f.children('textarea').each(function() { // run all inputs

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
        }
        i.next('.validation').html((ierror ? (i.attr('data-msg') != undefined ? i.attr('data-msg') : 'wrong Input') : '')).show('blind');
      }
    });
    if (ferror) return false;
    else var str = jquery3(this).serialize();
    var action = jquery3(this).attr('action');
    console.log(action)
    // This method gets the csrf token from the cookies
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          let cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
              // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
             }
         }
      }
      return cookieValue;
      }

      let csrftoken = getCookie('csrftoken');  
   
    function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
      }

    jquery3.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
         }
      }
    });
    jquery3.ajax({
      type: "POST",
      url: action,
      data: str,
      dataType:'json',
      statusCode: {
        403: function(responseObject, textStatus) {
          document.getElementById('sendmessage').classList.remove('show');
          document.getElementById('errormessage').innerHTML="Not Permitted!"+' '+textStatus;          
          document.getElementById('errormessage').classList.add('show');
        },
        404:  function(responseObject, textStatus) {
          document.getElementById('sendmessage').classList.remove('show');
          document.getElementById('errormessage').innerHTML="Not Found! 404"+' '+textStatus;          
          document.getElementById('errormessage').classList.add('show');
        },
        500:  function(responseObject, textStatus) {
          document.getElementById('sendmessage').classList.remove('show');
          document.getElementById('errormessage').innerHTML="Internal Server 500!"+' '+textStatus;          
          document.getElementById('errormessage').classList.add('show');
        },
      },
      success: function(data) {
        // console.log(data.message)
        if (data.status === 200) {
          document.getElementById('errormessage').classList.remove('show')
          document.getElementById('sendmessage').innerHTML=data.message
          document.getElementById('sendmessage').classList.add('show')
          $('.contactForm').find( "input, textarea").val("");
        } 
        else {
          document.getElementById('sendmessage').classList.remove('show')
          document.getElementById('errormessage').innerHTML=data.message          
          document.getElementById('errormessage').classList.add('show')
        }

      }
    });
    return false;
  });

});
