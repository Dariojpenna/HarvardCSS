document.addEventListener('DOMContentLoaded', function(){


    function updateNotificationCount() {
        fetch('/get_unread_notifications/')
            .then(response => response.json())
            .then(data => {
                
                const notificationCount = data.count;
                const notificationBadge = document.getElementById('notification-count');
                
                // Counter update
                if (notificationCount > 0) {
                    notificationBadge.innerHTML = notificationCount;
                    notificationBadge.style.display = 'block';
                } else {
                    notificationBadge.style.display = 'none';
                }
            })
            .catch(error => {
                console.error('Error al obtener las notificaciones no leídas:', error);
            });

            
    }
    
    // Call update function
    window.addEventListener('load', updateNotificationCount);

})