(function ($) {
  "use strict";
        let message_container=document.getElementById('mCSB_1_container')        
        let number=document.getElementById('message-number')
        let comments_number
        // This method gets the time difference for the data
        function timeDifference(current, previous) {
          const milliSecondsPerMinute = 60 * 1000
          const milliSecondsPerHour = milliSecondsPerMinute * 60
          const milliSecondsPerDay = milliSecondsPerHour * 24
          const milliSecondsPerMonth = milliSecondsPerDay * 30
          const milliSecondsPerYear = milliSecondsPerDay * 365
        
          const elapsed = current - previous
        
          if (elapsed < milliSecondsPerMinute / 3) {
            return 'just now'
          }
        
          if (elapsed < milliSecondsPerMinute) {
            return 'less than 1 min ago'
          } else if (elapsed < milliSecondsPerHour) {
            return Math.round(elapsed / milliSecondsPerMinute) + ' min ago'
          } else if (elapsed < milliSecondsPerDay) {
            return Math.round(elapsed / milliSecondsPerHour) + ' h ago'
          } else if (elapsed < milliSecondsPerMonth) {
            let time=Math.round(elapsed/milliSecondsPerDay)
            let data
            if(time===1){
              data=time + ' day ago'
            }
            else{
              data=time + ' days ago'
            }
            return data
          } else if (elapsed < milliSecondsPerYear) {
            return Math.round(elapsed / milliSecondsPerMonth) + ' mo ago'
          } else {
            let time = Math.round(elapsed / milliSecondsPerYear)
            let data
            if(time===1){
              data=time + ' year ago'
            }
            else{
              data=time + ' years ago'
            }
            return data
          }
        }
        
        function timeDifferenceForDate(date) {
          const now = new Date().getTime()
          const updated = new Date(date).getTime()
          return timeDifference(now, updated)
        }
        
        //  console.log(date)
         $.ajax({
          type: "Get",
          url: "/account/messages/",
          dataType: "json",
          success: function (data) {
          //here variable data is in JSON format
          if(data.new_comments.length!=0){
            for(let item=0; item < data.new_comments.length; item++){ 
                let list=document.createElement('li')
                list.setAttribute('id', 'block-displayer')
                let anchor=document.createElement('a')        
                let message=document.createElement('div')
                message.setAttribute('class', 'message-content')
                anchor.setAttribute('href', '#')
                anchor.appendChild(message)
                list.appendChild(anchor)
                message_container.appendChild(list)
                
                //creating a unique id for each form in the scroll bar                
                let date=new Date(data.new_comments[item][3].date)
                // console.log(data.new_comments[item][0].id)
                message.innerHTML=`<h2>${data.new_comments[item][2].name}</h2><span class='message-date'>${timeDifferenceForDate(date)}</span><p>${data.new_comments[item][1].body}</p><hr />`             
                // console.log($(publish_name))
                
            }
        }
        else{
          let list=document.createElement('li')
          list.setAttribute('id', 'block-displayer')
          let anchor=document.createElement('a')        
          let message=document.createElement('div')
          message.setAttribute('class', 'message-content')
          anchor.setAttribute('href', '#')
          anchor.appendChild(message)
          list.appendChild(anchor)
          message_container.appendChild(list)
          message.innerHTML=`<h2>No New Comments </h2>`
        }
          
          comments_number=data.comments
          number.innerHTML= "<a href=''>" + comments_number + "  New Comments</a>"
          console.log(data)
          },
          error: function(jqXHR, textStatus){
            console.log('Error occurred: ' + textStatus);
          },
          })                           
        
})(jQuery);
