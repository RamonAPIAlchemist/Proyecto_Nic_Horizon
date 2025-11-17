// static/js/acercade.js

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar animaciones y efectos
    initAboutPage();
    
    // Configurar observadores de intersección para animaciones al hacer scroll
    initScrollAnimations();
    
    // Configurar eventos de hover para las cards
    initCardInteractions();
    
    // Configurar contadores animados para las estadísticas
    initCounterAnimations();
});

function initAboutPage() {
    console.log('Inicializando página Acerca de Nic_Horizon');
    
    // Añadir clase específica al body para estilos específicos de esta página
    document.body.classList.add('acercade-body');
    
    // Preload de recursos si es necesario
    preloadResources();
}

function initScrollAnimations() {
    // Configurar Intersection Observer para animaciones al hacer scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                
                // Si es una card de estadística, iniciar contador
                if (entry.target.classList.contains('stat-item')) {
                    animateCounter(entry.target);
                }
            }
        });
    }, observerOptions);

    // Observar todos los elementos que queremos animar al hacer scroll
    const elementsToAnimate = document.querySelectorAll('.card, .impact-card, .stat-item');
    elementsToAnimate.forEach(el => observer.observe(el));
}

function initCardInteractions() {
    // Efectos especiales para las cards al hacer hover
    const cards = document.querySelectorAll('.card-hover');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transition = 'all 0.3s ease';
        });
    });
}

function initCounterAnimations() {
    // Preparar contadores para animación
    const statNumbers = document.querySelectorAll('.stat-number');
    
    statNumbers.forEach(stat => {
        const target = parseInt(stat.textContent);
        stat.setAttribute('data-target', target);
        stat.textContent = '0';
    });
}

function animateCounter(statItem) {
    const statNumber = statItem.querySelector('.stat-number');
    const target = parseInt(statNumber.getAttribute('data-target'));
    const duration = 2000; // 2 segundos
    const step = target / (duration / 16); // 60fps
    let current = 0;
    
    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        
        // Formatear el número según sea necesario
        if (statNumber.textContent.includes('+')) {
            statNumber.textContent = Math.floor(current) + '+';
        } else if (statNumber.textContent.includes('%')) {
            statNumber.textContent = Math.floor(current) + '%';
        } else {
            statNumber.textContent = Math.floor(current);
        }
    }, 16);
}

function preloadResources() {
    // Preload de imágenes importantes
    const imagesToPreload = [
        '{{ url_for("static", filename="nic_horizon_logo.png") }}'
    ];
    
    imagesToPreload.forEach(src => {
        const img = new Image();
        img.src = src;
    });
}

// Función para manejar errores de carga de imágenes
function handleImageError(imgElement) {
    console.log('Error cargando imagen:', imgElement.src);
    imgElement.style.display = 'none';
    
    const fallback = imgElement.nextElementSibling;
    if (fallback && fallback.classList.contains('logo-icon-fallback')) {
        fallback.style.display = 'flex';
    }
}

// Exportar funciones para uso global si es necesario
window.AboutPage = {
    init: initAboutPage,
    animateCounters: initCounterAnimations
};