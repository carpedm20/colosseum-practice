
/*
 * CSRF jqeury error solution
 * http://stackoverflow.com/a/5107878
 */

/*
 * Study group search
 */

$('.search_query').keypress(function (e) {
  if (e.which == 13) {
    $('form#study_group_serach_form').submit();
  }
})

$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                 }
             }
         }
         return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});

/*
  $(function() {
    $( ".datepicker" ).datepicker({
      changeMonth: true,
      changeYear: true,
      yearRange: "1900:2012",
      // You can put more options here.

    });
  });
*/

/*
$(document).ready(function() {
  $('#calendar').fullCalendar({
    header: {
      left: 'prev,next today',
      center: 'title',
      right: 'month,agendaWeek,agendaDay'
    },
    editable: true,
    events: '/study/group/event/get_event.json'
  });
});
*/

/*
$(document).ready(function() {
  var date = new Date();
  var d = date.getDate();
  var m = date.getMonth();
  var y = date.getFullYear();
    
  var calendar = $("#calendar").fullCalendar({
    header: {
      left: "prev,next today",
      center: "title",
      right: "month,agendaweek,agendaday"
    },

    titleformat: "ddd, mmm dd, yyyy",
    defaultview: "month",
    selectable: true,
    selecthelper: true,

    select: function(start, end, allday, event, resourceid) {
      var title = prompt("event title:");
      if (title) {
        console.log("@@ adding event " + title + ", start " + start + ", end " + end + ", allday " + allday + ", resource " + resourceid);
        calendar.fullcalendar("renderevent",
        {
          title: title,
          start: start,
          end: end,
          allday: allday,
          resourceid: resourceid
        },
        true // make the event "stick"
        );
     }
      calendar.fullcalendar("unselect");
    },
    editable: true,
    resources: [
      {
        name: "resource 1",
        id: "resource1"
      },
      {
        name: "resource 2",
        id: "resource2"
      },
      {
        name: "resource 3",
        id: "resource3"
      }
    ],
  });
});
*/
