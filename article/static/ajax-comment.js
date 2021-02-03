
    // This ajax function submits the comments
    function submit_data(action_status, publish, deleteBtn, form){
        //initialise DOM elements
        
        if ($.data(form, 'submitted')) return false;
          
        var form_data=new FormData(form)

        // This appends whether the comment is to be published or to be deleted
        form_data.append('action', action_status)
        // let str = form.serialize();
        // form_data.append(str)
        let action = form.getAttribute('action');
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
        // console.log(csrftoken)
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
        processData: false,
        contentType: false,
        cache: false,
        url: action,
        data:form_data,
        dataType:'json',               
        success: function(data) {
            // console.log(data.message)
            if (data.status === 200) {
                if(data.message === 'published'){
                   deleteBtn.classList.remove('btn-danger')
                   publish.innerHTML=data.message 
                   publish.classList.remove('btn-primary')        
                   publish.classList.add('btn-success')
                }
                else{
                   publish.classList.remove('btn-primary')
                   deleteBtn.innerHTML=data.message 
                   deleteBtn.classList.remove('btn-danger')        
                   deleteBtn.classList.add('btn-success') 
                }                  
            }                               
        },
        })
        $.data(form, 'submitted', true); // mark form as submitted.
   }

