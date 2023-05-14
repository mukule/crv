$(document).ready(function() {
    var date = new Date();
    var currentMonth = date.getMonth();
    var currentYear = date.getFullYear();
  
    // Initialize the calendar
    $('#calendar').fullCalendar({
      // Set options for the calendar
      header: {
        left: 'prev,next',
        center: 'title',
        right: ''
      },
      
      defaultView: 'month',
      defaultDate: date,
      titleFormat: 'MMMM YYYY',
      eventLimit: true,
      events: [],
     
    });
  
    // Set the previous month button click event
    $('#prev-month').click(function() {
      currentMonth--;
      if (currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
      }
      $('#calendar').fullCalendar('gotoDate', currentYear + '-' + (currentMonth + 1) + '-01');
      $('#calendar').fullCalendar('render');
    });
  
    // Set the next month button click event
    $('#next-month').click(function() {
      currentMonth++;
      if (currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
      }
      $('#calendar').fullCalendar('gotoDate', currentYear + '-' + (currentMonth + 1) + '-01');
      $('#calendar').fullCalendar('render');
    });
  });
  