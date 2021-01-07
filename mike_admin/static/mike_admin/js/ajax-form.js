(function ($) {
     "use strict";
            let ferror=false
            let form = $('#ajax-form')
        // Validation for login form
            form.validate(
            {					
                rules:
                {	
                    email:
                    {
                        required: true,
                        email: true
                    },
                    body:
                    {
                        required: true,
                        minlength: 10,
                        maxlength:100
                    },
                    name:{
                        required: true,
                        minlength:4,
                        maxlength:30
                    },
                    phone:{
                        number:true,
                        required: true,
                        minlength:9,
                        maxlength:13,
                      },
                    trans:{
                        required: true,
                        minlength:5
                    },
                    content:{
                        required:true,
                        minlength:20,
                    },
                    username:{
                        required:true,
                    },
                    title:{
                        required:true,
                    }
            },
                messages:
                {	
                    email:
                    {
                        required: 'Please enter your email address!',
                        email: 'Please enter a VALID email address!'
                    },
                    body:
                    {
                        required: 'Please Write Us Something!',
                        minlength:'Your Comment Is Too Short!',
                        maxlength:'Your Comment Is Too Long!'
                    },
                    name:
                    {
                        required:'Enter Your Name!',
                        minlength:'Your Name Should be atleast 4 Characters!',
                        maxlength:'The Name is Too Long!'
                    },                    
                    phone:
                    {                       
                        number:'Phone must be a number!', 
                        required:'Enter Your Safaricom Mobile Phone Number!',
                        minlength:'Your Phone Number Should be atleast 9 characters!',
                        maxlength:'The Phone Number is too Long!',
                    },
                    trans:
                    {
                        required:'Please enter The Transaction Id You Just Received!',
                        minlength:'Please enter a valid Transaction Id!'
                    },
                    content:
                    {
                        required:'Please Write Something Here!',
                        minlength:'Too Short!'
                    },
                    username:
                    {
                        required:'Please Select A User'
                    },
                    title:
                    {
                        required:'The title field is required'
                    }
                },					
                
                errorPlacement: function(error, element)
                {
                    error.insertAfter(element.parent());
                    ferror=true
                }
            });
            
            	
            form.submit((e)=>{		
                e.preventDefault()  
                // if ($.data(form, 'submitted')) return false;
                if(ferror) {
                    ferror=false
                    return false 
                }	
                
                var form_data=new FormData(document.getElementById('ajax-form'))
                		
                // let str = form.serialize();
                // form_data.append(str)
                let action = form.attr('action');
                // console.log(form.serialize())
                // console.log(action)
                // Display the key/value pairs
                // for (var pair of form_data.entries()) {
                //     console.log(pair[0]+ ', ' + pair[1]); 
                // }
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
                statusCode: {
                    403: function(responseObject, textStatus) {
                    document.getElementById('sendmessage').classList.remove('show');
                    document.getElementById('errormessage').innerHTML="Not Permitted!"+' '+textStatus;          
                    document.getElementById('errormessage').classList.add('show');
                    // alert("Not Permitted!"+' '+textStatus)
                    },
                    404:  function(responseObject, textStatus) {
                    document.getElementById('sendmessage').classList.remove('show');
                    document.getElementById('errormessage').innerHTML="Not Found! 404"+' '+textStatus;          
                    document.getElementById('errormessage').classList.add('show');
                    // alert("Not Found! 404"+' '+textStatus)
                    },
                    500:  function(responseObject, textStatus) {
                    document.getElementById('sendmessage').classList.remove('show');
                    document.getElementById('errormessage').innerHTML="Internal Server 500!"+' '+textStatus;          
                    document.getElementById('errormessage').classList.add('show');
                    // alert("Internal Server 500! "+textStatus)
                    },
                },
                success: function(data) {
                    console.log(data.message)
                    if (data.status === 200) {
                        // document.getElementById('message').innerHTML=data.message
                        // alert(data.message)
                        // form.appendChild(document.createElement('p').innerHTML=data.message)
                        document.getElementById('errormessage').classList.remove('show')
                    document.getElementById('sendmessage').innerHTML=data.message          
                    document.getElementById('sendmessage').classList.add('show')
                    
                    // form.find( "textarea").val("");
                    } 
                    else {
                    document.getElementById('sendmessage').classList.remove('show')
                    document.getElementById('errormessage').innerHTML=data.message          
                    document.getElementById('errormessage').classList.add('show')
                    // alert(data.message)
                    }
            
                },
                error: () =>{
                    document.getElementById('sendmessage').classList.remove('show')
                    document.getElementById('errormessage').innerHTML='There Was An Error In Your Submission'         
                    document.getElementById('errormessage').classList.add('show')
                },                                
                
                })
                .fail(function(jqXHR, textStatus){
                    document.getElementById('sendmessage').classList.remove('show')
                    document.getElementById('errormessage').innerHTML="Please Try Again!"         
                    document.getElementById('errormessage').classList.add('show')
                    })

            // $.data(form, 'submitted', true); // mark form as submitted.
            });
            
        
    })(jQuery); 


const resetForm = () =>{
    document.getElementById('sendmessage').classList.remove('show')        
    document.getElementById('errormessage').classList.remove('show')
    // document.getElementById('progress-home').removeChild('progress-container')
}