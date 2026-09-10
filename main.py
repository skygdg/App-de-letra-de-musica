import eel
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import re
import time
import os

# ================= CONFIGURAÇÕES =================
CLIENT_ID = 'ID DO CLIENTE'
CLIENT_SECRET = 'CHAVE DO CLIENTE'
REDIRECT_URI = 'https://127.0.0.1:8888/callback'


# Inicializa o Eel para ---> 'web'
eel.init('web')

def buscar_letra_sincronizada(nome_musica, nome_artista):
    """Busca a letra no LRCLIB"""
    url = "https://lrclib.net/api/search"
    parametros = {"track_name": nome_musica, "artist_name": nome_artista}
    try:
        resposta = requests.get(url, params=parametros)
        if resposta.status_code == 200:
            dados = resposta.json()
            if len(dados) > 0 and dados[0].get('syncedLyrics'):
                return dados[0]['syncedLyrics']
    except Exception as e: print(f"Erro LRCLIB: {e}")
    return None

def parse_lrc(texto):
    """Transforma o texto .lrc em uma lista [(tempo_ms, 'frase')]"""
    letras_sincronizadas = []
    padrao = re.compile(r'\[(\d{2}):(\d{2})\.(\d{2})\](.*)')
    for linha in texto.strip().split('\n'):
        match = padrao.match(linha)
        if match:
            m, s, xx, texto_letra = match.groups()
            tempo_ms = (int(m) * 60000) + (int(s) * 1000) + (int(xx) * 10)
            letras_sincronizadas.append((tempo_ms, texto_letra.strip()))
    return letras_sincronizadas

class MotorSpotify:
    def __init__(self):
        # Conecta no Spotify
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI, scope="user-read-playback-state"
        ))
        
        # Variáveis de controle
        self.musica_atual_id = ""
        self.letras = []
        self.is_playing = False
        self.frase_anterior = "" # Para evitar atualizações redundantes
        
        # Variáveis para sincronia suave
        self.spotify_progress_ms = 0
        self.ultimo_update_relogio = time.time()

    def loop_principal(self):
        """O motor que roda sem parar num thread separado"""
        # 1. Thread de Sincronia com o Spotify (a cada 2 segundos)
        ultimo_check_spotify = 0

        while True:
            agora = time.time()

            try:
                playback = self.sp.current_playback()

                if playback is not None and playback['is_playing']:
                    self.is_playing = True

                    # LIGA O VISUALIZADOR
                    eel.controlarVisualizador(True)

                    # Checa o Spotify a cada 2 segundos
                    if agora - ultimo_check_spotify > 2:
                        ultimo_check_spotify = agora
                        try:
                            playback = self.sp.current_playback()
                            if playback is not None and playback['is_playing']:
                                self.is_playing = True
                                item = playback['item']
                                nova_musica_id = item['id']

                                if nova_musica_id != self.musica_atual_id:
                                    self.musica_atual_id = nova_musica_id
                                    nome, artista = item['name'], item['artists'][0]['name']

                                    # Envia os dados da música para o JS
                                    eel.atualizarInfoMusica(nome, artista)

                                    texto_lrc = buscar_letra_sincronizada(nome, artista)
                                    self.letras = parse_lrc(texto_lrc) if texto_lrc else []
                                    if not self.letras:
                                        eel.atualizarLetra("(Letra sincronizada não encontrada)")

                                self.spotify_progress_ms = playback['progress_ms']
                                self.ultimo_update_relogio = time.time()
                            else:
                                self.is_playing = False
                                eel.atualizarInfoMusica("Spotify pausado", "...")
                                eel.atualizarLetra("🎵")
                                eel.controlarVisualizador(False)
                        except Exception as e:
                            print(f"Erro Spotify: {e}")

                    # 2. Atualização suave da tela (a cada 50ms)
                    if self.is_playing and self.letras:
                        tempo_passado = (time.time() - self.ultimo_update_relogio) * 1000
                        tempo_estimado_ms = self.spotify_progress_ms + tempo_passado

                        frase_atual = "🎵"
                        for tempo_ms, frase in self.letras:
                            if tempo_estimado_ms >= tempo_ms:
                                frase_atual = frase if frase else "🎵"
                            else:
                                break

                        # SÓ ATUALIZA SE A FRASE MUDOU (evita piscar a tela)
                        if frase_atual != self.frase_anterior:
                            self.frase_anterior = frase_atual
                            # ENVIAMOS A LETRA PARA O JAVASCRIPT ANIMAR
                            eel.atualizarLetra(frase_atual)

                else:
                    self.is_playing = False
                    eel.atualizarInfoMusica("Spotify pausado", "...")
                    eel.atualizarLetra("🎵")
                    eel.controlarVisualizador(False)

            except Exception as e:
                print(f"Erro Spotify: {e}")

            # Pequena pausa para o CPU respirar
            eel.sleep(0.05)

# --- INICIALIZAÇÃO ---
if __name__ == "__main__":
    motor = MotorSpotify()
    
    # Inicia o motor em um thread separado para não travar o Eel
    eel.spawn(motor.loop_principal)
    
    # Abre a janela do navegador (tamanho e posição)
    print("Iniciando interface visual...")
    eel.start('index.html', size=(1000, 500), mode='default')