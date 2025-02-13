const alunoBtn = document.getElementById('alunoBtn');
const visitanteBtn = document.getElementById('visitanteBtn');
const alunoForm = document.getElementById('alunoForm');
const visitanteForm = document.getElementById('visitanteForm');

alunoBtn.addEventListener('click', () => {
    alunoForm.classList.add('active');
    visitanteForm.classList.remove('active');
    alunoBtn.classList.add('active');
    visitanteBtn.classList.remove('active');
});

visitanteBtn.addEventListener('click', () => {
    visitanteForm.classList.add('active');
    alunoForm.classList.remove('active');
    visitanteBtn.classList.add('active');
    alunoBtn.classList.remove('active');
});
