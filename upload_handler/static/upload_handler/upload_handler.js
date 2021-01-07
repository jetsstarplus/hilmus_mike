 // Generate 32 char random uuid
 function gen_uuid() {
    var uuid = ""
    for (var i=0; i < 32; i++) {
        uuid += Math.floor(Math.random() * 16).toString(16);
    }
    return uuid
}

// Add upload progress for multipart forms.
$(function() {
    let ferror=false
    let form = $("#form.upload")
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
    
    /*
    This throws a syntax error...
    $('form[@enctype=multipart/form-data]').submit(function(){
    */
    $('form.upload').submit(function(){
        // Prevent multiple submits
        if ($.data(this, 'submitted')) return false;
        // console.log('submitted')
        var freq = 1000; // freqency of update in ms
        var uuid = gen_uuid(); // id for this upload so we can fetch progress info.
        var progress_url = '/account/upload/'; // ajax view serving progress info
        let location=document.getElementById('progress-home')
        // Append X-Progress-ID uuid form action
        this.action += (this.action.indexOf('?') == -1 ? '?' : '&') + 'X-Progress-ID=' + uuid;
        
        var $progress = $('<div id="upload-progress" class="upload-progress"></div>').appendTo(location).append('<div class="progress-container"><span class="progress-info"></span><div class="progress-bar"></div></div>');
        
        // progress bar position
        $progress.css({
            // position: 'absolute',
            // left: '50%', marginLeft: 0-($progress.width()/2), bottom: '20%'
        }).show();
        //alert("test progress")
        // Update progress bar
        function update_progress_info() {
            // alert("test progress")
            $progress.show();
            $.getJSON(progress_url, {'X-Progress-ID': uuid}, function(data, status){
            //   alert(data)
                if (data) {
                    var progress = parseInt(data.uploaded) / parseInt(data.length);
                    // console.log(progress)
                    var width = $progress.find('.progress-container').width()
                    // console.log(width)
                    var progress_width = width * progress;
                    $progress.find('.progress-bar').width(progress_width);
                    $progress.find('.progress-info').text('uploading ' + parseInt(progress*100) + '%');
                    // console.log(progress_width)
                }
                // else{
                //     console.log("No data")
                // }
                window.setTimeout(update_progress_info, freq);
            });
        };
        window.setTimeout(update_progress_info, freq);

        $.data(this, 'submitted', true); // mark form as submitted.
    });
});