/**
 * Gère une modale de confirmation de suppression créée dynamiquement avec un message et des textes de boutons personnalisables.
 * Utilise Flowbite Modal pour l'affichage et retourne une Promise pour le résultat de la confirmation.
 * Prend en charge l'internationalisation avec window.django.gettext.
 * @class
 */
class DeleteModalManager {
    constructor() {
        this.modal = null;
        this.modalInstance = null;
        this.isClosing = false; // Empêche les appels récursifs
    }

    /**
     * Crée l'élément DOM de la modale de confirmation de suppression dynamiquement.
     * @private
     * @param {string} message - Le message à afficher dans la modale.
     * @param {string} confirmText - Le texte du bouton de confirmation.
     * @param {string} cancelText - Le texte du bouton d'annulation.
     */
    createModal(message, confirmText, cancelText) {
        if (!window.Modal) {
            console.error('Erreur : La bibliothèque Flowbite Modal nest pas chargée.');
            window.notificationManager?.showError(window.django?.gettext ? window.django.gettext('Erreur : La bibliothèque Flowbite nest pas disponible.') : 'Erreur : La bibliothèque Flowbite nest pas disponible.');
            return;
        }

        const modalId = `delete-modal-${Date.now()}`;
        this.modal = document.createElement('div');
        this.modal.id = modalId;
        this.modal.tabIndex = -1;
        this.modal.className = 'hidden overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-[10000001] justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full';
        this.modal.setAttribute('data-modal', 'true');

        this.modal.innerHTML = `
            <div class="relative w-full h-full max-w-md px-4 md:h-auto">
                <div class="relative bg-white rounded-lg shadow">
                    <div class="flex justify-end p-2">
                        <button type="button" class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center" data-modal-hide="${modalId}">
                            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                            </svg>
                            <span class="sr-only">${window.django?.gettext ? window.django.gettext('Fermer la modale') : 'Fermer la modale'}</span>
                        </button>
                    </div>
                    <div class="p-6 pt-0 text-center">
                        <svg class="w-16 h-16 mx-auto text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        <h3 class="mt-5 mb-6 text-lg text-gray-500" id="delete-modal-message">${message || (window.django?.gettext ? window.django.gettext('Êtes-vous sûr de vouloir supprimer cet élément ?') : 'Êtes-vous sûr de vouloir supprimer cet élément ?')}</h3>
                        <button id="delete-modal-confirm" class="text-white bg-red-600 hover:bg-red-800 focus:ring-4 focus:ring-red-300 font-medium rounded-lg text-base inline-flex items-center px-3 py-2.5 text-center mr-2 cursor-pointer">
                            ${confirmText || (window.django?.gettext ? window.django.gettext("Oui, je suis sûr") : "Oui, je suis sûr")}
                        </button>
                        <button id="delete-modal-cancel" class="text-gray-900 bg-white hover:bg-gray-100 focus:ring-4 focus:ring-blue-300 border border-gray-200 font-medium inline-flex items-center rounded-lg text-base px-3 py-2.5 text-center cursor-pointer" data-modal-hide="${modalId}">
                            ${cancelText || (window.django?.gettext ? window.django.gettext('Non, annuler') : 'Non, annuler')}
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(this.modal);
        this.modalInstance = new window.Modal(this.modal, {
            backdrop: 'static',
            backdropClasses: 'bg-gray-900/50 fixed inset-0 z-[10000000]',
            closable: true,
            onHide: () => {
                if (!this.isClosing) {
                    this.isClosing = true;
                    this.closeModal();
                }
            }
        });

        this.initializeEventListeners(modalId);
    }

    /**
     * Initialise les écouteurs d'événements pour les boutons de la modale.
     * @private
     * @param {string} modalId - L'identifiant unique de la modale.
     */
    initializeEventListeners(modalId) {
        const confirmButton = this.modal.querySelector('#delete-modal-confirm');
        const cancelButton = this.modal.querySelector('#delete-modal-cancel');
        const closeButton = this.modal.querySelector(`[data-modal-hide="${modalId}"]`);

        const confirmHandler = () => {
            if (this.resolveCallback) {
                this.resolveCallback(true);
                this.modalInstance.hide();
            }
        };
        const cancelHandler = () => {
            if (this.resolveCallback) {
                this.resolveCallback(false);
                this.modalInstance.hide();
            }
        };

        confirmButton.addEventListener('click', confirmHandler);
        cancelButton.addEventListener('click', cancelHandler);
        closeButton.addEventListener('click', cancelHandler);
    }

    /**
     * Ferme la modale et nettoie les ressources.
     * @private
     */
    closeModal() {
        if (this.modal && this.modalInstance && !this.isClosing) {
            this.isClosing = true;
            this.modal.remove();
            this.modal = null;
            this.modalInstance = null;
            this.resolveCallback = null;
            this.isClosing = false;
        }
    }

    /**
     * Affiche la modale de confirmation de suppression avec un message et des textes de boutons personnalisés.
     * @param {string} message - Le message à afficher dans la modale.
     * @param {string} confirmText - Le texte du bouton de confirmation.
     * @param {string} cancelText - Le texte du bouton d'annulation.
     * @returns {Promise<boolean>} Résout avec true si confirmé, false si annulé ou fermé.
     */
    show(message, confirmText, cancelText) {
        return new Promise((resolve) => {
            this.resolveCallback = resolve;
            this.createModal(message, confirmText, cancelText);
            if (this.modalInstance) {
                this.modalInstance.show();
            }
        });
    }
}

// Exporter une instance singleton
const deleteModalManager = new DeleteModalManager();
window.deleteModalManager = deleteModalManager;