document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek',
        headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'timeGridDay,timeGridWeek,dayGridMonth'
        },
        events: '/property/available_time_slots/',
        selectable: true,
        select: function(info) {
        var dateStr = info.startStr.split('T')[0];
        var timeStr = info.startStr.split('T')[1].slice(0, 5);
        var propertyId = document.getElementById('propertyIdHolder').value;
        if (confirm(`Do you want to book a meeting on ${dateStr} from ${timeStr}?`)) {
            fetch('/property/book_meeting/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                date: dateStr,
                time: timeStr,
                property_id: propertyId
            })
            }).then(response => {
            if (response.ok) {
                calendar.refetchEvents();
            } else {
                alert('Failed to book meeting');
            }
            });
        }
        calendar.unselect();
        },
        eventClick: function(info) {
        var dateStr = info.event.startStr.split('T')[0];
        var timeStr = info.event.startStr.split('T')[1].slice(0, 5);
        var endTimeStr = info.event.endStr.split('T')[1].slice(0, 5);
        var propertyId = document.getElementById('propertyIdHolder').value;
        if (confirm(`Do you want to book a meeting on ${dateStr} from ${timeStr} to ${endTimeStr}?`)) {
            fetch('/property/book_meeting/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                date: dateStr,
                time: timeStr,
                property_id: propertyId
            })
            }).then(response => {
            if (response.ok) {
                calendar.refetchEvents();
                window.location.href = `${baseUrl}/property/home/`;
            } else {
                alert('Failed to book meeting');
            }
            });
        }
        info.jsEvent.preventDefault();
        }
    });
    calendar.render();
});

  
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
}
  
  