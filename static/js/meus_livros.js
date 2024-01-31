function addLivro() {
    $("#addLivro").toggle();
    $("html, body").animate({
        scrollTop: $(document).scrollTop() + 40
    }, "slow");
}

function mostraInput(isbn) {
    document.getElementById("tituloInput" + isbn).removeAttribute("hidden");
    document.getElementById("atualizar" + isbn).style.display = "none";
    document.getElementById("salvar" + isbn).removeAttribute("hidden");
}

document.getElementById('fotos').addEventListener('change', function (e) {
    var fileNames = Array.from(e.target.files).map(file => file.name);
    document.querySelector('#escolher-fotos').innerText = fileNames.join(', ');
    document.querySelector('#escolher-fotos').innerText += " Clique Para Adicionar Mais Fotos";
});

document.getElementById('fotos').addEventListener('change', function (e) {
    var preview = document.getElementById('preview');
    preview.innerHTML = '';

    Array.from(e.target.files).forEach(file => {
        var reader = new FileReader();

        reader.onload = function (e) {
            var img = document.createElement('img');
            img.src = e.target.result;
            img.height = 75;
            img.width = 75;
            preview.appendChild(img);
        };

        reader.readAsDataURL(file);
    });
});