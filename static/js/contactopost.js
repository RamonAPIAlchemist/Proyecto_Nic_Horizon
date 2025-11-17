// static/js/contactopost.js

document.addEventListener('DOMContentLoaded', function() {
    console.log('Nic_Horizon - Página de Equipo cargada correctamente');
    
    // Inicializar la página
    initTeamPage();
    
    // Configurar animaciones al hacer scroll
    initScrollAnimations();
    
    // Configurar interacciones de las cards
    initCardInteractions();
    
    // Configurar contadores animados
    initCounterAnimations();
});

function initTeamPage() {
    console.log('Inicializando página de equipo Nic_Horizon');
    
    // Añadir clase específica al body para estilos específicos
    document.body.classList.add('team-page-body');
    
    // Preload de recursos importantes
    preloadTeamImages();
    
    // Configurar manejo de errores de imágenes
    setupImageErrorHandling();
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
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                
                // Si es una card de estadística, iniciar contador
                if (entry.target.classList.contains('philosophy-card')) {
                    animateStats();
                }
            }
        });
    }, observerOptions);

    // Observar elementos para animaciones
    const elementsToAnimate = document.querySelectorAll(
        '.team-card, .section-header, .specialty-card, .company-logo, .philosophy-card'
    );
    
    elementsToAnimate.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

function initCardInteractions() {
    // Efectos hover mejorados para las cards del equipo
    const teamCards = document.querySelectorAll('.team-card');
    
    teamCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            const roleBadge = this.querySelector('.team-role-badge');
            const photo = this.querySelector('.team-photo');
            
            if (roleBadge) {
                roleBadge.style.transform = 'translateX(-50%) scale(1.1)';
            }
            if (photo) {
                photo.style.transform = 'scale(1.05)';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            const roleBadge = this.querySelector('.team-role-badge');
            const photo = this.querySelector('.team-photo');
            
            if (roleBadge) {
                roleBadge.style.transform = 'translateX(-50%) scale(1)';
            }
            if (photo) {
                photo.style.transform = 'scale(1)';
            }
        });
        
        // Click en card para más información (opcional)
        card.addEventListener('click', function() {
            const memberName = this.querySelector('.team-member-name').textContent;
            console.log(`Clicked on team member: ${memberName}`);
            // Aquí puedes agregar funcionalidad para mostrar más detalles
        });
    });
}

function initCounterAnimations() {
    // Preparar contadores para animación
    const statNumbers = document.querySelectorAll('.stat-number');
    
    statNumbers.forEach(stat => {
        const originalText = stat.textContent;
        const numericValue = originalText.replace(/[^0-9]/g, '');
        const suffix = originalText.replace(numericValue, '');
        
        stat.setAttribute('data-target', numericValue);
        stat.setAttribute('data-suffix', suffix);
        stat.textContent = '0' + suffix;
    });
}

function animateStats() {
    const statNumbers = document.querySelectorAll('.stat-number');
    
    statNumbers.forEach(stat => {
        const target = parseInt(stat.getAttribute('data-target'));
        const suffix = stat.getAttribute('data-suffix');
        let current = 0;
        const duration = 2000; // 2 segundos
        const increment = target / (duration / 16); // 60fps
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            
            // Formatear según el tipo de número
            if (suffix === '+') {
                stat.textContent = Math.floor(current) + suffix;
            } else if (suffix === '%') {
                stat.textContent = Math.floor(current) + suffix;
            } else {
                stat.textContent = Math.floor(current) + suffix;
            }
        }, 16);
    });
}

function preloadTeamImages() {
    // Preload de imágenes del equipo para mejor experiencia
    const imagePaths = [
        '{{ url_for("static", filename="moises.jpg") }}',
        '{{ url_for("static", filename="joao.jpg") }}',
        '{{ url_for("static", filename="arlinton.jpg") }}',
        '{{ url_for("static", filename="heriberto.jpg") }}',
        '{{ url_for("static", filename="ninoska.jpg") }}',
        '{{ url_for("static", filename="nic_horizon_logo.png") }}'
    ];
    
    imagePaths.forEach(src => {
        const img = new Image();
        img.src = src;
    });
}

function setupImageErrorHandling() {
    // Manejo de errores para imágenes que no cargan
    const teamPhotos = document.querySelectorAll('.team-photo, .logo-image');
    
    teamPhotos.forEach(photo => {
        photo.addEventListener('error', function() {
            console.warn(`Error loading image: ${this.src}`);
            this.style.display = 'none';
            const placeholder = this.nextElementSibling;
            if (placeholder && (placeholder.classList.contains('team-img-placeholder') || 
                               placeholder.classList.contains('logo-icon-fallback'))) {
                placeholder.style.display = 'flex';
            }
        });
    });
}

// Función para compartir información del equipo
function shareTeam() {
    const teamInfo = {
        title: 'Nic_Horizon - Especialistas en Flutter',
        text: 'Conoce a nuestro equipo de desarrollo móvil con Flutter - Expertos en aplicaciones multiplataforma',
        url: window.location.href
    };
    
    if (navigator.share) {
        navigator.share(teamInfo)
            .then(() => console.log('Información del equipo compartida exitosamente'))
            .catch((error) => console.log('Error al compartir:', error));
    } else {
        // Fallback para navegadores que no soportan Web Share API
        navigator.clipboard.writeText(window.location.href)
            .then(() => {
                showNotification('Enlace copiado al portapapeles');
            })
            .catch(() => {
                // Fallback más básico
                prompt('Comparte este enlace:', window.location.href);
            });
    }
}

function showNotification(message) {
    // Crear notificación temporal
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--accent-blue);
        color: white;
        padding: 1rem 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        z-index: 1000;
        font-weight: 500;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Exportar funciones para uso global si es necesario
window.TeamPage = {
    init: initTeamPage,
    share: shareTeam,
    animateStats: animateStats
};