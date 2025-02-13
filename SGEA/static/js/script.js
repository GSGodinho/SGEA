let currentStep = 1;
const totalSteps = 4;

function showStep(step) {
    // Esconder todos os passos
    for (let i = 1; i <= totalSteps; i++) {
        document.getElementById('step-' + i).style.display = 'none';
    }

    // Exibir o passo atual
    document.getElementById('step-' + step).style.display = 'block';

    // Gerenciar visibilidade dos botões
    if (step === 1) {
        document.getElementById('prev-btn').style.display = 'none';
    } else {
        document.getElementById('prev-btn').style.display = 'inline-block';
    }

    if (step === totalSteps) {
        document.getElementById('next-btn').style.display = 'none';
        document.getElementById('submit-btn').style.display = 'inline-block';
    } else {
        document.getElementById('next-btn').style.display = 'inline-block';
        document.getElementById('submit-btn').style.display = 'none';
    }
}

function nextStep() {
    if (currentStep < totalSteps) {
        currentStep++;
        showStep(currentStep);
    }
}

function prevStep() {
    if (currentStep > 1) {
        currentStep--;
        showStep(currentStep);
    }
}

// Inicializar mostrando o primeiro passo
showStep(currentStep);
