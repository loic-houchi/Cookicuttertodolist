const Auth = {
    initMultiStepForm() {
        const nextBtn = document.getElementById('nextToStep2');
        const backBtn = document.getElementById('backToStep1');
        let currentStep = 1;

        nextBtn.addEventListener('click', () => {
            document.getElementById('step1').classList.remove('active');
            document.getElementById('step2').classList.add('active');
            document.getElementById('step1-indicator').classList.remove('active');
            document.getElementById('step1-indicator').classList.add('completed');
            document.getElementById('step2-indicator').classList.add('active');
            document.getElementById('connector1').classList.add('active');
            currentStep = 2;
        });

        backBtn.addEventListener('click', () => {
            document.getElementById('step2').classList.remove('active');
            document.getElementById('step1').classList.add('active');
            document.getElementById('step2-indicator').classList.remove('active');
            document.getElementById('step1-indicator').classList.remove('completed');
            document.getElementById('step1-indicator').classList.add('active');
            document.getElementById('connector1').classList.remove('active');
            currentStep = 1;
        });
    },

    togglePassword(inputId, toggleId) {
        const input = document.getElementById(inputId);
        const toggle = document.getElementById(toggleId);
        if (input.type === 'password') {
            input.type = 'text';
            toggle.classList.remove('fa-eye');
            toggle.classList.add('fa-eye-slash');
        } else {
            input.type = 'password';
            toggle.classList.remove('fa-eye-slash');
            toggle.classList.add('fa-eye');
        }
    }
};