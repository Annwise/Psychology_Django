document.addEventListener('DOMContentLoaded', function() {
    const bookingForm = document.getElementById('booking-form');
    
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            fetch('/booking/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                }
            })
            .then(response => response.json())
            .then(data => {
                const messageDiv = document.getElementById('booking-message');
                if (data.success) {
                    messageDiv.innerHTML = '<p style="color: #ffd700;">Спасибо за запись! Мы свяжемся с вами в ближайшее время.</p>';
                    messageDiv.style.display = 'block';
                    document.getElementById('booking-form').reset();
                } else {
                    messageDiv.innerHTML = '<p style="color: #ff6b6b;">Ошибка: ' + data.error + '</p>';
                    messageDiv.style.display = 'block';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('booking-message').innerHTML = '<p style="color: #ff6b6b;">Произошла ошибка при отправке формы</p>';
                document.getElementById('booking-message').style.display = 'block';
            });
        });
    }
});
