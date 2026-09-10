#  Spotify Real-Time Lyrics 

Um reprodutor de letras sincronizadas em tempo real que se conecta à sua conta do Spotify e exibe as letras das músicas com uma interface visual moderna, fluida e com efeitos em neon!

Este projeto foi construído usando **Python** para a lógica de backend (comunicação com APIs) e **HTML/CSS/JS** para a interface gráfica, unidos pela biblioteca Eel.

## ✨ Funcionalidades

* **Sincronia Perfeita:** Monitora o que você está ouvindo no Spotify e sincroniza o tempo exato com a letra da música.
* **Busca Automática:** Utiliza a API gratuita LRCLIB para baixar os arquivos de letras sincronizadas (`.lrc`) automaticamente em segundo plano.
* **Interface Web Moderna:** Letras gigantes, centralizadas, com efeito visual de "neon" (verde Spotify) e animações de *fade-in/fade-out*.
* **Visualizador de Áudio (Audio Visualizer):** Barras animadas que simulam a batida da música e pausam automaticamente quando você pausa o Spotify.
* **Otimização de API (Anti-Rate Limit):** Lógica inteligente que faz requisições ao Spotify apenas a cada 2 segundos e calcula os milissegundos restantes usando o relógio interno do sistema, garantindo fluidez extrema sem derrubar ou sobrecarregar os servidores.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Spotipy:** Para autenticação OAuth2 e comunicação com a Web API do Spotify.
* **Requests:** Para consumir a API de letras do LRCLIB.
* **Eel:** Ponte para conectar o backend Python com o frontend web.
* **HTML / CSS / JavaScript:** Para a construção e animação da interface de usuário.
