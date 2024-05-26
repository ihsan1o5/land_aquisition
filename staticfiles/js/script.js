let map;
let marker;
let autocomplete;
let baseUrl = 'http://localhost:8000'

function initMap() {
    console.log("Initializing map");
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: -34.397, lng: 150.644 },
        zoom: 8
    });

    const input = document.getElementById('pac-input');
    autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.bindTo('bounds', map);

    const infowindow = new google.maps.InfoWindow();
    marker = new google.maps.Marker({
        map: map,
        anchorPoint: new google.maps.Point(0, -29)
    });

    autocomplete.addListener('place_changed', () => {
        infowindow.close();
        marker.setVisible(false);
        const place = autocomplete.getPlace();
        if (!place.geometry) {
            console.log("No details available for input: '" + place.name + "'");
            return;
        }

        if (place.geometry.viewport) {
            map.fitBounds(place.geometry.viewport);
        } else {
            map.setCenter(place.geometry.location);
            map.setZoom(17);
        }

        marker.setPosition(place.geometry.location);
        marker.setVisible(true);

        document.getElementById('location-input').value = `${place.geometry.location.lat()},${place.geometry.location.lng()}`;
    });

    map.addListener('click', (event) => {
        marker.setPosition(event.latLng);
        document.getElementById('location-input').value = `${event.latLng.lat()},${event.latLng.lng()}`;
    });
}

document.getElementById('save-location').addEventListener('click', () => {
    const location = document.getElementById('location-input').value;
    
    if(location) {
        // Fetch the mapModal element and ensure it is instantiated correctly
        const mapModalEl = document.getElementById('mapModal');
        const mapModal = bootstrap.Modal.getInstance(mapModalEl) || new bootstrap.Modal(mapModalEl);
        console.log("location added => ", location)
        // Hide the mapModal if it is correctly instantiated
        if (mapModal) {
            mapModal.hide();
            console.log('mapModal hidden');
        } else {
            console.log('Failed to instantiate mapModal');
        }

        // Show the exampleModal
        const exampleModalEl = document.getElementById('exampleModal');
        const exampleModal = new bootstrap.Modal(exampleModalEl);
        exampleModal.show();
        console.log('exampleModal shown');
    } else {
        console.log('Location input is empty');
    }
});

document.getElementById('mapModal').addEventListener('shown.bs.modal', () => {
    google.maps.event.trigger(map, 'resize');
    if (marker && marker.getPosition()) {
        map.setCenter(marker.getPosition());
    } else {
        map.setCenter({ lat: -34.397, lng: 150.644 });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var deleteIcons = document.querySelectorAll('.delete-property-icon');
    
    deleteIcons.forEach(function(icon) {
        icon.addEventListener('click', function(e) {
            var propertyId = e.target.getAttribute('data-property-id');
            console.log("Property ID:", propertyId);

            var deleteForm = warningAlert.querySelector('#deleteForm');
            deleteForm.action = '/property/delete_property/' + propertyId+'/';
        });
    });
});

function getCSRFToken() {
    let csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    return csrfToken;
}

function editComment(commentId) {
    document.getElementById('comment-' + commentId).classList.add('d-none');
    document.getElementById('edit-comment-' + commentId).classList.remove('d-none');
}

function saveComment(commentId) {
    var newComment = document.getElementById('edit-comment-text-' + commentId).value;
    
    var updateUrl = `${baseUrl}/property/update_comment/${commentId}/`
    
    fetch(updateUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ comment: newComment })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('comment-' + commentId).innerHTML = newComment;
            document.getElementById('comment-' + commentId).classList.remove('d-none');
            document.getElementById('edit-comment-' + commentId).classList.add('d-none');
        } else {
            alert('Error updating comment');
        }
    });
}


document.addEventListener('DOMContentLoaded', function() {
    fetchNotifications();
  
    function fetchNotifications() {
      fetch(`${baseUrl}/property/fetch_notifications/`)
        .then(response => response.json())
        .then(data => {
            console.log('data.....', data);
          const notificationList = document.getElementById('notificationList');
          const notificationCount = document.getElementById('notificationCount');
          notificationList.innerHTML = '';
  
          if (data.notifications.length > 0) {
            notificationCount.textContent = data.notifications.length;
            data.notifications.forEach(notification => {
              const notificationItem = document.createElement('div');
  
              notificationItem.innerHTML = `
                <div class="alert alert-primary" onclick="viewNotificationDetail(${notification.id}, ${notification.property})" role="alert" style="padding: 0; cursor: pointer;">
                    <div class="d-flex justify-content-between notification-top">
                    <span>${notification.title}</span>
                    <a href="#" onclick="markAsRead(${notification.id})">Mark as read</a>
                    </div>
                    <div style="padding: 5px;">
                    <p style="font-size: 10px; margin: 0;">${notification.detail}</p>
                    </div>
                </div>
              `;
              notificationList.appendChild(notificationItem);
            });
          } else {
            notificationCount.textContent = '';
            notificationCount.style.display = 'none';
            notificationList.innerHTML = '<p>No new notifications.</p>';
          }
        });
    }
  
    window.markAsRead = function(notificationId) {
      fetch(`${baseUrl}/property/mark_notification_read/${notificationId}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken()
        }
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          fetchNotifications(); // Refresh notifications after marking as read
        } else {
          alert('Error marking notification as read');
        }
      });
    };

    window.viewNotificationDetail = function(notificationId, propertyId) {
        console.log("noti noti ........ ", propertyId);
        fetch(`${baseUrl}/property/view_notification_detail/${notificationId}/${propertyId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = `${baseUrl}/property/property_detail/${data.propertyId}/`;
            } else {
                alert('Error marking notification as read');
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', (event) => {
    const notificationList = document.getElementById('notificationList');
    const notificationCount = document.getElementById('notificationCount');

    const notificationSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/notifications/'
    );

    notificationSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log("Channel data", data);
        const notificationItem = document.createElement('div');
        notificationItem.innerHTML = `
            <div class="alert alert-primary" role="alert" style="padding: 0; cursor: pointer;">
                <div class="d-flex justify-content-between notification-top">
                    <span>${data.title}</span>
                    <a href="#" onclick="markAsRead(${data.id})">Mark as read</a>
                </div>
                <div style="padding: 5px;">
                    <p style="font-size: 10px; margin: 0;">${data.detail}</p>
                </div>
            </div>
        `;
        notificationList.appendChild(notificationItem);

        // Update the notification count
        const currentCount = parseInt(notificationCount.textContent) || 0;
        notificationCount.textContent = currentCount + 1;
    };

    notificationSocket.onclose = function(e) {
        console.error('WebSocket closed unexpectedly');
    };

    notificationSocket.onerror = function(e) {
        console.error('WebSocket encountered an error:', e);
    };

    notificationSocket.onopen = function(e) {
        console.log('WebSocket connection established');
    };
});


