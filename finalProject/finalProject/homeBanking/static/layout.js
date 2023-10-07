document.addEventListener('DOMContentLoaded', function(){


    function updateNotificationCount() {
        fetch('/get_unread_notifications/')
            .then(response => response.json())
            .then(data => {
                
                const notificationCount = data.count;
                const notificationBadge = document.getElementById('notification-count');
                
                // Actualiza el contador en la interfaz de usuario
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
    
    // Llama a la función para actualizar el contador al cargar la página
    window.addEventListener('load', updateNotificationCount);

})