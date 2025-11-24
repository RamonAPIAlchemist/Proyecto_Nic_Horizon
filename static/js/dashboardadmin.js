// dashboard.js - Funcionalidades corregidas para el Dashboard Administrativo

class DashboardManager {
    constructor() {
        this.initialized = false;
        this.firstInvalidField = null;
        this.init();
    }

    

    init() {
        if (this.initialized) {
            console.log('⚠️ Dashboard ya inicializado');
            return;
        }

        console.log('✅ Dashboard administrativo cargado correctamente');
        
        // Esperar a que el DOM esté completamente listo
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.initializeComponents();
            });
        } else {
            this.initializeComponents();
        }
        
        this.initialized = true;
    }

    initializeComponents() {
        this.initModals();
        this.initTooltips();
        this.initDeleteConfirmations();
        this.initSaveButtons();
        this.initDateInputs();
        this.initFlashMessages();
        this.initFormValidation();
        this.initScrollEffects();
        
        this.verifyBootstrap();
        this.verifyForms();

        // Limpieza periódica de backdrops
        this.startBackdropCleanup();
    }

    // Verificar que Bootstrap esté disponible
    verifyBootstrap() {
        if (typeof bootstrap === 'undefined') {
            console.error('❌ Bootstrap no está cargado');
            this.showEmergencyAlert('Bootstrap no está cargado correctamente. Recargue la página.');
            return false;
        }
        console.log('✅ Bootstrap cargado correctamente');
        return true;
    }

    // Inicializar modales corregidos
    initModals() {
        console.log('🔄 Inicializando modales...');
        
        const modalElements = document.querySelectorAll('.modal');
        console.log(`📦 Encontrados ${modalElements.length} modales`);

        modalElements.forEach(modal => {
            try {
                // Configurar modal con opciones específicas
                const bsModal = new bootstrap.Modal(modal, {
                    backdrop: true,
                    keyboard: true,
                    focus: true
                });

                // Limpiar backdrop cuando se cierre el modal
                modal.addEventListener('hidden.bs.modal', () => {
                    this.cleanupBackdrops();
                });

            } catch (error) {
                console.error('Error inicializando modal:', error);
            }
        });

        this.cleanupBackdrops();
    }

    // Limpiar backdrops duplicados
    cleanupBackdrops() {
        const backdrops = document.querySelectorAll('.modal-backdrop');
        if (backdrops.length > 1) {
            console.log(`🧹 Limpiando ${backdrops.length - 1} backdrops duplicados`);
            for (let i = 0; i < backdrops.length - 1; i++) {
                backdrops[i].remove();
            }
        }
    }

    // Limpieza periódica de backdrops
    startBackdropCleanup() {
        setInterval(() => {
            this.cleanupBackdrops();
        }, 2000);
    }

    // Inicializar tooltips de Bootstrap
    initTooltips() {
        if (typeof bootstrap?.Tooltip === 'undefined') {
            console.warn('⚠️ Tooltips de Bootstrap no disponibles');
            return;
        }
        
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        const tooltipList = tooltipTriggerList.map(tooltipTriggerEl => {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
        
        console.log(`🔧 Inicializados ${tooltipList.length} tooltips`);
    }

    // Confirmación para eliminaciones
    initDeleteConfirmations() {
        const deleteButtons = document.querySelectorAll('.btn-outline-danger');
        console.log(`🗑️ Configurando ${deleteButtons.length} botones de eliminación`);
        
        deleteButtons.forEach(button => {
            // Solo agregar confirmación a botones que no abren modales
            if (!button.hasAttribute('data-bs-toggle') || button.getAttribute('data-bs-toggle') !== 'modal') {
                button.addEventListener('click', (e) => {
                    if (!confirm('¿Está seguro de que desea eliminar este elemento?')) {
                        e.preventDefault();
                    }
                });
            }
        });
    }

    // Efectos de carga para botones de guardar - CORREGIDO
    initSaveButtons() {
        const saveButtons = document.querySelectorAll('.modal-footer .btn-primary, .modal-footer .btn-success, .modal-footer .btn-info');
        console.log(`💾 Configurando ${saveButtons.length} botones de guardar`);

        saveButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const form = button.closest('form');
                if (form) {
                    if (this.validateForm(form)) {
                        this.showLoadingState(button);
                        // Permitir que el formulario se envíe normalmente
                    } else {
                        e.preventDefault();
                        this.showValidationErrors(form);
                    }
                }
            });
        });
    }

    // Mostrar estado de carga en botones - MEJORADO
    showLoadingState(button) {
        const originalText = button.innerHTML;
        const originalWidth = button.offsetWidth;
        
        // Mantener el ancho del botón
        button.style.minWidth = originalWidth + 'px';
        
        button.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Procesando...';
        button.disabled = true;
        
        // Restaurar después de 5 segundos máximo (fallback)
        setTimeout(() => {
            if (button.disabled) {
                button.innerHTML = originalText;
                button.disabled = false;
                button.style.minWidth = '';
                this.showAlert('La operación está tomando más tiempo de lo esperado', 'warning');
            }
        }, 5000);
    }

    // Formatear fechas para inputs date
    initDateInputs() {
        const dateInputs = document.querySelectorAll('input[type="date"]');
        dateInputs.forEach(input => {
            if (input.value) {
                try {
                    // Formatear fecha para input date
                    const date = new Date(input.value + 'T00:00:00');
                    if (!isNaN(date.getTime())) {
                        input.value = date.toISOString().split('T')[0];
                    }
                } catch (error) {
                    console.warn('Error formateando fecha:', error);
                }
            }
        });
    }

    // Auto-ocultar mensajes flash después de 5 segundos
    initFlashMessages() {
        const flashMessages = document.querySelectorAll('.alert');
        flashMessages.forEach(alert => {
            setTimeout(() => {
                if (alert.parentNode) {
                    try {
                        const bsAlert = new bootstrap.Alert(alert);
                        bsAlert.close();
                    } catch (error) {
                        // Fallback si Bootstrap Alert no funciona
                        alert.style.opacity = '0';
                        setTimeout(() => {
                            if (alert.parentNode) {
                                alert.parentNode.removeChild(alert);
                            }
                        }, 300);
                    }
                }
            }, 5000);
        });
    }

    // Validación de formularios - MEJORADA
    initFormValidation() {
        const forms = document.querySelectorAll('form');
        console.log(`📝 Configurando validación para ${forms.length} formularios`);

        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!this.validateForm(form)) {
                    e.preventDefault();
                    e.stopPropagation();
                    this.showValidationErrors(form);
                }
            });

            // Validación en tiempo real
            const inputs = form.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                input.addEventListener('blur', () => {
                    this.validateField(input);
                });
            });
        });
    }

    // Validar campo individual
    validateField(field) {
        if (field.hasAttribute('required') && !field.value.trim()) {
            this.highlightInvalidField(field, 'Este campo es obligatorio');
            return false;
        }

        // Validación de email
        if (field.type === 'email' && field.value && !this.isValidEmail(field.value)) {
            this.highlightInvalidField(field, 'Por favor, ingrese un email válido');
            return false;
        }

        // Si pasa validación, limpiar errores
        this.clearFieldError(field);
        return true;
    }

    // Validar formulario - MEJORADA
    validateForm(form) {
        let isValid = true;
        this.firstInvalidField = null;

        const requiredFields = form.querySelectorAll('[required]');
        
        // Limpiar errores previos
        form.querySelectorAll('.is-invalid').forEach(field => {
            field.classList.remove('is-invalid');
        });
        form.querySelectorAll('.invalid-feedback').forEach(feedback => {
            feedback.remove();
        });
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                this.highlightInvalidField(field);
                if (!this.firstInvalidField) {
                    this.firstInvalidField = field;
                }
            }
        });

        // Validación específica para emails
        const emailFields = form.querySelectorAll('input[type="email"]');
        emailFields.forEach(field => {
            if (field.value && !this.isValidEmail(field.value)) {
                isValid = false;
                this.highlightInvalidField(field, 'Por favor, ingrese un email válido');
                if (!this.firstInvalidField) {
                    this.firstInvalidField = field;
                }
            }
        });

        return isValid;
    }

    // Validar email
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Resaltar campo inválido - MEJORADA
    highlightInvalidField(field, message = 'Este campo es obligatorio') {
        field.classList.add('is-invalid');
        
        // Remover feedback anterior si existe
        const existingFeedback = field.parentNode.querySelector('.invalid-feedback');
        if (existingFeedback) {
            existingFeedback.remove();
        }
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        
        field.parentNode.appendChild(errorDiv);
    }

    // Limpiar error del campo
    clearFieldError(field) {
        field.classList.remove('is-invalid');
        const errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.remove();
        }
    }

    // Mostrar errores de validación
    showValidationErrors(form) {
        if (this.firstInvalidField) {
            this.firstInvalidField.focus();
            this.firstInvalidField = null;
        }
        
        this.showAlert('Por favor, complete todos los campos obligatorios correctamente', 'warning');
    }

    // Mostrar alerta personalizada - MEJORADA
    showAlert(message, type = 'info') {
        // Crear contenedor si no existe
        let alertContainer = document.querySelector('.flash-messages');
        if (!alertContainer) {
            alertContainer = document.createElement('div');
            alertContainer.className = 'flash-messages mb-4';
            const container = document.querySelector('.container-fluid');
            const firstChild = container.firstChild;
            container.insertBefore(alertContainer, firstChild);
        }
        
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            <i class="fas fa-${this.getAlertIcon(type)} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        alertContainer.appendChild(alertDiv);
        
        // Auto-ocultar después de 5 segundos
        setTimeout(() => {
            if (alertDiv.parentNode) {
                try {
                    const bsAlert = new bootstrap.Alert(alertDiv);
                    bsAlert.close();
                } catch (error) {
                    alertDiv.remove();
                }
            }
        }, 5000);
    }

    // Alerta de emergencia para errores críticos
    showEmergencyAlert(message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger alert-dismissible fade show system-alert';
        alertDiv.innerHTML = `
            <i class="fas fa-exclamation-triangle me-2"></i>
            <strong>Error del Sistema:</strong> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertDiv);
    }

    // Obtener icono para alerta
    getAlertIcon(type) {
        const icons = {
            'success': 'check-circle',
            'danger': 'exclamation-triangle',
            'warning': 'exclamation-circle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    // Efectos de scroll suave
    initScrollEffects() {
        if (!('IntersectionObserver' in window)) {
            console.warn('⚠️ IntersectionObserver no soportado');
            return;
        }
        
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        const animatedElements = document.querySelectorAll('.stat-card, .card');
        animatedElements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(el);
        });
    }

    // Debug para formularios - MEJORADO
    debugSubmit(formId) {
        console.log('🔄 Verificando formulario:', formId);
        
        const form = document.getElementById(formId);
        if (!form) {
            console.error('❌ Formulario no encontrado:', formId);
            this.showAlert('Error: Formulario no encontrado', 'danger');
            return false;
        }
        
        console.log('✅ Formulario encontrado, procediendo con validación...');
        return this.validateForm(form);
    }

    // Verificar que todos los formularios estén correctamente configurados
    verifyForms() {
        console.log('🔍 Verificando formularios...');
        
        const forms = {
            usuarios: document.querySelectorAll('form[action*="editar_usuario_dashboard"]'),
            publicaciones: document.querySelectorAll('form[action*="editar_publicacion_dashboard"]'),
            ruedas: document.querySelectorAll('form[action*="editar_rueda_dashboard"]')
        };
        
        console.log(`📊 Formularios encontrados:`);
        console.log(`  Usuarios: ${forms.usuarios.length}`);
        console.log(`  Publicaciones: ${forms.publicaciones.length}`);
        console.log(`  Ruedas: ${forms.ruedas.length}`);
        
        // Verificar que todos los formularios tengan IDs únicos
        this.verifyFormIds(forms);
        
        return true;
    }

    

    // Verificar IDs de formularios
    verifyFormIds(forms) {
        const allForms = [...forms.usuarios, ...forms.publicaciones, ...forms.ruedas];
        const formIds = new Set();
        
        allForms.forEach(form => {
            const formId = form.id;
            if (formId) {
                if (formIds.has(formId)) {
                    console.warn(`⚠️ ID duplicado encontrado: ${formId}`);
                } else {
                    formIds.add(formId);
                }
            } else {
                console.warn('⚠️ Formulario sin ID:', form);
            }
        });
    }

    // Método para exportar datos (opcional)
    exportData(tableType) {
        console.log(`📊 Exportando datos de: ${tableType}`);
        this.showAlert(`Exportando datos de ${tableType}...`, 'info');
        
        // Aquí puedes implementar la lógica de exportación real
        // Por ejemplo: generar CSV, Excel, etc.
    }
}

// Inicializar dashboard cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    // Pequeño delay para asegurar que Bootstrap esté completamente cargado
    setTimeout(() => {
        if (typeof bootstrap !== 'undefined') {
            window.dashboard = new DashboardManager();
        } else {
            console.error('❌ Bootstrap no disponible. Recargando página...');
            setTimeout(() => {
                window.location.reload();
            }, 2000);
        }
    }, 100);
});

// Manejar errores no capturados
window.addEventListener('error', (e) => {
    console.error('Error global capturado:', e.error);
    
    if (window.dashboard) {
        window.dashboard.showEmergencyAlert('Ocurrió un error inesperado. Consulte la consola para más detalles.');
    }
});

// Funciones globales para uso en templates
window.debugSubmit = function(formId) {
    if (window.dashboard && typeof window.dashboard.debugSubmit === 'function') {
        return window.dashboard.debugSubmit(formId);
    }
    
    // Fallback si dashboard no está cargado
    console.warn('Dashboard no disponible, usando validación fallback');
    const form = document.getElementById(formId);
    if (!form) {
        alert('Error: Formulario no encontrado');
        return false;
    }
    
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('is-invalid');
            
            if (!field.nextElementSibling || !field.nextElementSibling.classList.contains('invalid-feedback')) {
                const errorDiv = document.createElement('div');
                errorDiv.className = 'invalid-feedback';
                errorDiv.textContent = 'Este campo es obligatorio';
                field.parentNode.appendChild(errorDiv);
            }
        } else {
            field.classList.remove('is-invalid');
            const errorDiv = field.parentNode.querySelector('.invalid-feedback');
            if (errorDiv) {
                errorDiv.remove();
            }
        }
    });
    
    if (!isValid) {
        alert('Por favor, complete todos los campos obligatorios');
        return false;
    }
    
    return true;
};

window.exportData = function(tableType) {
    if (window.dashboard && typeof window.dashboard.exportData === 'function') {
        return window.dashboard.exportData(tableType);
    }
    alert(`Función de exportación para ${tableType} no disponible`);
};

// Polyfill para navegadores antiguos
if (!String.prototype.includes) {
    String.prototype.includes = function(search, start) {
        if (typeof start !== 'number') {
            start = 0;
        }
        if (start + search.length > this.length) {
            return false;
        } else {
            return this.indexOf(search, start) !== -1;
        }
    };
}

// Prevenir envíos dobles de formularios
document.addEventListener('submit', function(e) {
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    
    if (submitBtn && submitBtn.disabled) {
        e.preventDefault();
        return false;
    }
    
    if (submitBtn) {
        submitBtn.disabled = true;
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Procesando...';
        
        // Restaurar después de 10 segundos (fallback)
        setTimeout(() => {
            if (submitBtn.disabled) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
        }, 10000);
    }
});