// Pegamos as referências dos elementos HTML
const infoMusica = document.getElementById('nome-musica');
const infoArtista = document.getElementById('nome-artista');
const letraTexto = document.getElementById('letra-texto');

// Função que o Python chama para atualizar os dados da música
eel.expose(atualizarInfoMusica);
function atualizarInfoMusica(nome, artista) {
    infoMusica.innerText = nome;
    infoArtista.innerText = artista;
}

// Função principal que o Python chama para atualizar a letra
eel.expose(atualizarLetra);
function atualizarLetra(novaFrase) {
    // 1. Fase de Fade-Out (Apagar a frase anterior)
    letraTexto.classList.remove('visivel');
    
    // 2. Esperamos o tempo da animação de CSS acabar (400ms)
    setTimeout(() => {
        // 3. Trocamos o texto enquanto está invisível
        letraTexto.innerText = novaFrase;
        
        // 4. Fase de Fade-In (Acender a nova frase)
        letraTexto.classList.add('visivel');
    }, 400); // Esse tempo deve ser igual ao 'transition' no CSS
}


// Controle do Visualizador de Áudio
eel.expose(controlarVisualizador);
function controlarVisualizador(estaTocando) {
    const barras = document.querySelectorAll('.bar');
    
    barras.forEach(barra => {
        if (estaTocando) {
            barra.classList.add('tocando');
        } else {
            barra.classList.remove('tocando');
        }
    });
}