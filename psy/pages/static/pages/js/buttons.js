// Обработчик кнопки консультации
document.addEventListener('DOMContentLoaded', function() {
    const consultationBtn = document.querySelector('.js-consultation-btn');
    
    if (consultationBtn) {
        consultationBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            // 1. Плавный скролл к разделу контактов
            const target = document.getElementById('contacts');
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }

            // 2. Анимация нажатия (опционально)
            this.classList.add('button-pressed');
            setTimeout(() => {
                this.classList.remove('button-pressed');
            }, 300);
            
            // 3. Для будущей формы (заглушка)
            console.log('Инициация записи...');
        });
    }
});