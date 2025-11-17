// dashboard.js - Funcionalidades para el Dashboard Administrativo

class DashboardManager {
    constructor() {
        this.init();
    }

    init() {
        console.log('✅ Dashboard administrativo cargado correctamente');
        
        this.initTooltips();
        this.initDeleteConfirmations();
        this.initSaveButtons();
        this.initDateInputs();
        this.initFlashMessages();
        this.initFormValidation();
        this.initScrollEffects();
        
        // Verificar formularios después de la carga
        setTimeout(() => this.verifyForms(), 1000);
    }

    // Inicializar tooltips de Bootstrap
    initTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        const tooltipList = tooltipTriggerList.map(tooltipTriggerEl => {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Confirmación para eliminaciones
    initDeleteConfirmations() {
        const deleteButtons = document.querySelectorAll('.btn-outline-danger');
        deleteButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                if (!confirm('¿Está seguro de que desea eliminar este elemento?')) {
                    e.preventDefault();
                }
            });
        });
    }

    // Efectos de carga para botones de guardar
    initSaveButtons() {
        const saveButtons = document.querySelectorAll('.modal-footer .btn-primary, .modal-footer .btn-success, .modal-footer .btn-info');
        saveButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const form = button.closest('form');
                if (form && form.checkValidity()) {
                    this.showLoadingState(button);
                }
            });
        });
    }

    // Mostrar estado de carga en botones
    showLoadingState(button) {
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Guardando...';
        button.disabled = true;
        
        // Restaurar después de 1.5 segundos (simulación)
        setTimeout(() => {
            button.innerHTML = originalText;
            button.disabled = false;
        }, 1500);
    }

    // Formatear fechas para inputs date
    initDateInputs() {
        const dateInputs = document.querySelectorAll('input[type="date"]');
        dateInputs.forEach(input => {
            if (input.value) {
                const date = new Date(input.value);
                if (!isNaN(date)) {
                    input.value = date.toISOString().split('T')[0];
                }
            }
        });
    }

    // Auto-ocultar mensajes flash después de 5 segundos
    initFlashMessages() {
        const flashMessages = document.querySelectorAll('.alert');
        flashMessages.forEach(alert => {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        });
    }

    // Validación de formularios
    initFormValidation() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!this.validateForm(form)) {
                    e.preventDefault();
                    this.showValidationErrors(form);
                }
            });
        });
    }

    // Validar formulario
    validateForm(form) {
        let isValid = true;
        const requiredFields = form.querySelectorAll('[required]');
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                this.highlightInvalidField(field);
            } else {
                this.clearFieldError(field);
            }
        });

        return isValid;
    }

    // Resaltar campo inválido
    highlightInvalidField(field) {
        field.classList.add('is-invalid');
        
        // Crear mensaje de error si no existe
        if (!field.nextElementSibling || !field.nextElementSibling.classList.contains('invalid-feedback')) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'invalid-feedback';
            errorDiv.textContent = 'Este campo es obligatorio';
            field.parentNode.appendChild(errorDiv);
        }
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
        const firstInvalidField = form.querySelector('.is-invalid');
        if (firstInvalidField) {
            firstInvalidField.focus();
        }
        
        // Mostrar alerta general
        this.showAlert('Por favor, complete todos los campos obligatorios marcados con *', 'warning');
    }

    // Mostrar alerta personalizada
    showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            <i class="fas fa-${this.getAlertIcon(type)} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.querySelector('.flash-messages').appendChild(alertDiv);
        
        // Auto-ocultar después de 5 segundos
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 5000);
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
        // Observar elementos para animación al hacer scroll
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

        // Aplicar a tarjetas y tablas
        document.querySelectorAll('.stat-card, .card').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(el);
        });
    }

    // Debug para formularios de ruedas
    debugSubmit(ruedaId) {
        console.log('🔄 Intentando enviar formulario para rueda:', ruedaId);
        
        const form = document.getElementById('formEditarRueda' + ruedaId);
        if (!form) {
            console.error('❌ Formulario no encontrado:', 'formEditarRueda' + ruedaId);
            return false;
        }
        
        const formData = new FormData(form);
        
        console.log('📤 Datos del formulario:');
        for (let [key, value] of formData.entries()) {
            console.log(`  ${key}: ${value}`);
        }
        console.log('📍 URL de destino:', form.action);
        
        // Verificar que todos los campos requeridos estén llenos
        const nombre = form.querySelector('input[name="nombre"]').value;
        const fecha = form.querySelector('input[name="fecha"]').value;
        const descripcion = form.querySelector('textarea[name="descripcion"]').value;
        
        if (!nombre || !fecha || !descripcion) {
            console.log('❌ Campos requeridos vacíos');
            this.showAlert('Por favor, complete todos los campos obligatorios (*)', 'warning');
            return false;
        }
        
        console.log('✅ Formulario válido, enviando...');
        return true;
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
        // Implementar lógica de exportación aquí
        this.showAlert(`Exportando datos de ${tableType}...`, 'info');
    }

    // Método para buscar en tablas
    initTableSearch() {
        const searchInputs = document.querySelectorAll('.table-search');
        searchInputs.forEach(input => {
            input.addEventListener('input', (e) => {
                const searchTerm = e.target.value.toLowerCase();
                const table = input.closest('.card').querySelector('table');
                const rows = table.querySelectorAll('tbody tr');
                
                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    row.style.display = text.includes(searchTerm) ? '' : 'none';
                });
            });
        });
    }
}

// Inicializar dashboard cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new DashboardManager();
});

// Funciones globales para uso en templates
window.debugSubmit = function(ruedaId) {
    return window.dashboard.debugSubmit(ruedaId);
};

window.exportData = function(tableType) {
    return window.dashboard.exportData(tableType);
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