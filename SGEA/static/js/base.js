const list = document.querySelectorAll('.list');

function activeLink() {
   list.forEach((item) => 
    item.classList.remove('ativo'));
   this.classList.add('ativo');
}

    list.forEach((item) => 
    item.addEventListener('mouseover', activeLink));

    list.forEach((item) => 
    item.addEventListener('mouseout', activeLink));