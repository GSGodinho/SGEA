
document.querySelectorAll('.cronograma-bloco').forEach(function(cronograma){

    container = cronograma.parentElement;    
    formsetPrefix= container.querySelector('.prefix').value

    buttonRemove=document.createElement('button');
    buttonRemove.innerHTML='Excluir';
    buttonRemove.classList.add('remove-cronograma');

    cronograma.appendChild(buttonRemove);
})

function AdicionarNovo(formsetPrefix,button)
{

    const container = button.parentElement.querySelector('.cronograma-container');
    
    // Verifica se já existe um bloco para clonar, caso contrário cria um novo bloco vazio
  
    // Clona o primeiro bloco de cronograma, se existir
    let newCronograma = container.querySelector('.modelo-form').cloneNode(true);
    newCronograma.setAttribute('class','cronograma-bloco');

    // retorna o total de formularios e utiliza para modificar o prefixo do id e nome
    var totalForms = document.querySelector(`#id_${formsetPrefix}-TOTAL_FORMS`);
    var formCount = parseInt(totalForms.value);
    const regex= new RegExp("__prefix__","g")
    newCronograma.innerHTML = newCronograma.innerHTML.replace(regex, formCount);
    totalForms.value = formCount + 1;
    


    buttonRemove=document.createElement('button');
    buttonRemove.innerHTML='Excluir';
    buttonRemove.classList.add('remove-cronograma');

    buttonRemove.addEventListener('click', function() {
        document.querySelector(`#id_${formsetPrefix}-TOTAL_FORMS`).value-=1
        this.parentElement.remove();
    });
    newCronograma.appendChild(buttonRemove);
    
    container.appendChild(newCronograma);
};



// Função para remover o cronograma (já existente no primeiro bloco)
document.querySelectorAll('.remove-cronograma').forEach(function(button) {
    button.addEventListener('click', function() {
        container= button.parentElement.parentElement
        formsetPrefix= container.querySelector('.prefix').value
        document.querySelector(`#id_${formsetPrefix}-TOTAL_FORMS`).value-=1
        this.parentElement.remove();
    });
});
