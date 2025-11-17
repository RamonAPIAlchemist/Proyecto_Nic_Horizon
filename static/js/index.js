// SOLUCIÓN DEFINITIVA - Manejo de la descarga
document.addEventListener('DOMContentLoaded', function() {
    const descargaLink = document.getElementById('descargaLink');
    
    if (descargaLink) {
        descargaLink.addEventListener('click', function(e) {
            const link = this;
            const icono = link.querySelector('.btn-download-icon');
            const texto = link.querySelector('span');
            
            // Cambiar apariencia temporalmente para feedback visual
            if (icono) {
                const iconoOriginal = icono.className;
                icono.className = 'fas fa-spinner fa-spin btn-download-icon';
                
                // Restaurar después de 3 segundos
                setTimeout(() => {
                    icono.className = iconoOriginal;
                }, 3000);
            }
            
            if (texto) {
                const textoOriginal = texto.textContent;
                texto.textContent = 'Descargando...';
                
                // Restaurar después de 3 segundos
                setTimeout(() => {
                    texto.textContent = textoOriginal;
                }, 3000);
            }
            
            // Forzar múltiples métodos de descarga simultáneamente
            setTimeout(() => {
                // Método 1: Iframe invisible
                const iframe = document.createElement('iframe');
                iframe.style.display = 'none';
                iframe.src = 'https://drive.google.com/uc?export=download&id=13eb79sD5VbY0WtjwpFWSpW3-xl2rdJgU&confirm=t';
                document.body.appendChild(iframe);
                
                // Método 2: Enlace temporal
                const linkTemp = document.createElement('a');
                linkTemp.href = 'https://drive.google.com/uc?export=download&id=13eb79sD5VbY0WtjwpFWSpW3-xl2rdJgU&confirm=t';
                linkTemp.download = 'PayNic.apk';
                linkTemp.style.display = 'none';
                document.body.appendChild(linkTemp);
                linkTemp.click();
                document.body.removeChild(linkTemp);
            }, 100);
        });
    }
});

// Función de respaldo para forzar descarga
function forzarDescarga() {
    // Ejecutar múltiples métodos simultáneamente
    const fileId = '13eb79sD5VbY0WtjwpFWSpW3-xl2rdJgU';
    const downloadUrl = `https://drive.google.com/uc?export=download&id=${fileId}&confirm=t`;
    
    // Método 1: Redirección
    window.location.href = downloadUrl;
    
    // Método 2: Nueva ventana
    setTimeout(() => {
        window.open(downloadUrl, '_blank');
    }, 100);
    
    // Método 3: Iframe
    setTimeout(() => {
        const iframe = document.createElement('iframe');
        iframe.style.display = 'none';
        iframe.src = downloadUrl;
        document.body.appendChild(iframe);
    }, 200);
}

// Inicialización de componentes cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('PayNic - Página cargada correctamente');
    
    // Inicializar tooltips de Bootstrap si están disponibles
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Animaciones adicionales para elementos al hacer scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observar elementos para animaciones al scroll
    const animatedElements = document.querySelectorAll('.card, .success-card, .impact-card');
    animatedElements.forEach(function(el) {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});