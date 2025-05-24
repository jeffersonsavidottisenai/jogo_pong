import pygame
import sys

# Inicializa o pygame
pygame.init()

# Define dimensões da janela
largura, altura = 800, 600
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("MEU JOGO")

# Cores
AZUL_CLARO = (173, 216, 230) # Definindo cor da janela
AMARELO = (255, 255, 0)
VERDE = (0, 255, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
CINZA = (200, 200, 200)
PRETO = (0, 0, 0)
AZUL_ESCURO = (0, 0, 128)

# Definições da bola
raio = 30
bola_x = largura // 2
bola_y = altura // 2
# A velocidade inicial da bola será definida pelo estágio de dificuldade, mas o valor de rebote será fixo para a altura.
velocidade_bola_x = 0 # Será sobrescrito por aplicar_dificuldade
velocidade_bola_y = 0 # Será sobrescrito por aplicar_dificuldade
gravidade = 0 # Será sobrescrito por aplicar_dificuldade

# Constante para a altura do salto (rebote da plataforma)
FORCA_REBOTE_VERTICAL = -15 # Este valor negativo controla a altura do salto da bola após atingir a plataforma.

# Configuração da plataforma
plataforma_largura = 160
plataforma_altura = 20
plataforma_x = largura - plataforma_largura # Plataforma inicia na direita
plataforma_y = altura - 50
velocidade_plataforma = 0 # Será sobrescrito por aplicar_dificuldade

# Pontuação
pontuacao = 0
fonte = pygame.font.SysFont(None, 36)
fonte_grande = pygame.font.SysFont(None, 72)
fonte_media = pygame.font.SysFont(None, 48)

# Vidas
vidas = 3

# Estados do jogo
MENU_INICIAL = 2
JOGANDO = 0
GAME_OVER = 1
PERGUNTA_CONTINUAR = 3
estado_jogo = MENU_INICIAL

# Estágios de Dificuldade
# velocidade_y_bola aqui será apenas o valor inicial quando a bola "nasce" ou reinicia.
# A força do rebote vertical é controlada por FORCA_REBOTE_VERTICAL.
ESTAGIOS_DIFICULDADE = [
    {"pontos_necessarios": 0, "velocidade_x_bola": 5, "velocidade_y_inicial_bola": -10, "gravidade": 0.1, "velocidade_plataforma": 7},
    {"pontos_necessarios": 10, "velocidade_x_bola": 6, "velocidade_y_inicial_bola": -12, "gravidade": 0.3, "velocidade_plataforma": 10},
    {"pontos_necessarios": 25, "velocidade_x_bola": 7, "velocidade_y_inicial_bola": -14, "gravidade": 0.1, "velocidade_plataforma": 13},
    {"pontos_necessarios": 45, "velocidade_x_bola": 8, "velocidade_y_inicial_bola": -16, "gravidade": 0.5, "velocidade_plataforma": 16},
    {"pontos_necessarios": 70, "velocidade_x_bola": 9, "velocidade_y_inicial_bola": -18, "gravidade": 0.2, "velocidade_plataforma": 19},
    {"pontos_necessarios": 100, "velocidade_x_bola": 10, "velocidade_y_inicial_bola": -20, "gravidade": 0.5, "velocidade_plataforma": 22}
]
estagio_atual_dificuldade_indice = 0

# Clock
clock = pygame.time.Clock()

# Função para desenhar textos
def desenhar_texto(texto, cor, x, y, fonte_obj=fonte):
    img = fonte_obj.render(texto, True, cor)
    janela.blit(img, (x, y))

# Função para aplicar as configurações do estágio de dificuldade atual
def aplicar_dificuldade():
    global velocidade_bola_x, velocidade_bola_y, gravidade, velocidade_plataforma
    estagio = ESTAGIOS_DIFICULDADE[estagio_atual_dificuldade_indice]
    velocidade_bola_x = estagio["velocidade_x_bola"]
    velocidade_bola_y = estagio["velocidade_y_inicial_bola"] # Usa a velocidade Y inicial do estágio
    gravidade = estagio["gravidade"]
    velocidade_plataforma = estagio["velocidade_plataforma"]

# Função para reiniciar o jogo completamente
def reiniciar_jogo_completo():
    global bola_x, bola_y, velocidade_bola_x, velocidade_bola_y, pontuacao, vidas, estado_jogo, plataforma_x, estagio_atual_dificuldade_indice
    bola_x = largura // 2
    bola_y = altura // 2
    pontuacao = 0
    vidas = 3
    plataforma_x = largura - plataforma_largura # Plataforma inicia na direita
    estagio_atual_dificuldade_indice = 0 # Reinicia o estágio de dificuldade
    aplicar_dificuldade() # Aplica as configurações do estágio inicial
    estado_jogo = JOGANDO

# Função para reiniciar a posição da bola após perder uma vida ou continuar
def reiniciar_posicao_bola():
    global bola_x, bola_y, velocidade_bola_x, velocidade_bola_y
    bola_x = largura // 2
    bola_y = altura // 2
    # Ao reiniciar, a bola também deve ter sua velocidade Y inicial definida pelo estágio
    estagio = ESTAGIOS_DIFICULDADE[estagio_atual_dificuldade_indice]
    velocidade_bola_x = estagio["velocidade_x_bola"]
    velocidade_bola_y = estagio["velocidade_y_inicial_bola"] # Usa a velocidade Y inicial do estágio

# Função para exibir a tela de Game Over
def tela_game_over():
    global estado_jogo, vidas

    while estado_jogo == GAME_OVER:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = evento.pos

                # Botão Sair
                if 250 <= mouse_pos[0] <= 550 and 350 <= mouse_pos[1] <= 400:
                    pygame.quit()
                    sys.exit()

                # Botão Reiniciar
                if 250 <= mouse_pos[0] <= 550 and 190 <= mouse_pos[1] <= 240:
                    reiniciar_jogo_completo()

        janela.fill(PRETO)
        desenhar_texto("GAME OVER", VERMELHO, largura // 2 - fonte_grande.size("GAME OVER")[0] // 2, altura // 4, fonte_obj=fonte_grande)
        desenhar_texto(f"Pontuação Final: {pontuacao}", BRANCO, largura // 2 - fonte.size(f"Pontuação Final: {pontuacao}")[0] // 2, altura // 2 - 60)
        desenhar_texto(f"Vidas restantes: {vidas}", BRANCO, largura // 2 - fonte.size(f"Vidas restantes: {vidas}")[0] // 2, altura // 2 - 20)

        # Desenha Botões
        # Botão Reiniciar
        pygame.draw.rect(janela, VERDE, (250, 190, 300, 50))
        desenhar_texto("Reiniciar Jogo", BRANCO, 250 + (300 - fonte.size("Reiniciar Jogo")[0]) // 2, 190 + (50 - fonte.size("Reiniciar Jogo")[1]) // 2)

        # Botão Sair
        pygame.draw.rect(janela, VERMELHO, (250, 350, 300, 50))
        desenhar_texto("Sair", BRANCO, 250 + (300 - fonte.size("Sair")[0]) // 2, 350 + (50 - fonte.size("Sair")[1]) // 2)

        pygame.display.flip()
        clock.tick(60)

# Função para exibir o menu inicial
def tela_menu_inicial():
    global estado_jogo

    while estado_jogo == MENU_INICIAL:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = evento.pos
                # Botão Iniciar
                if largura // 2 - 100 <= mouse_pos[0] <= largura // 2 + 100 and \
                   altura // 2 - 25 <= mouse_pos[1] <= altura // 2 + 25:
                    reiniciar_jogo_completo() # Inicia o jogo com estado JOGANDO
                    estado_jogo = JOGANDO

        janela.fill(AZUL_CLARO)
        desenhar_texto("MEU JOGO", AZUL_ESCURO, largura // 2 - fonte_grande.size("MEU JOGO")[0] // 2, altura // 4, fonte_obj=fonte_grande)

        # Desenha o botão Iniciar
        pygame.draw.rect(janela, VERDE, (largura // 2 - 100, altura // 2 - 25, 200, 50))
        desenhar_texto("Iniciar Jogo", BRANCO, largura // 2 - fonte.size("Iniciar Jogo")[0] // 2, altura // 2 - fonte.size("Iniciar Jogo")[1] // 2)

        pygame.display.flip()
        clock.tick(60)

# Função para perguntar ao jogador se quer continuar
def tela_pergunta_continuar():
    global estado_jogo, vidas

    while estado_jogo == PERGUNTA_CONTINUAR:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = evento.pos

                # Botão Continuar
                if 250 <= mouse_pos[0] <= 550 and 270 <= mouse_pos[1] <= 320:
                    vidas -= 1
                    reiniciar_posicao_bola()
                    estado_jogo = JOGANDO

                # Botão Sair / Não Continuar
                if 250 <= mouse_pos[0] <= 550 and 350 <= mouse_pos[1] <= 400:
                    estado_jogo = GAME_OVER # Leva para a tela de Game Over final

        janela.fill(PRETO)
        desenhar_texto("Perdeu uma vida!", AMARELO, largura // 2 - fonte_media.size("Perdeu uma vida!")[0] // 2, altura // 4, fonte_obj=fonte_media)
        desenhar_texto(f"Vidas restantes: {vidas}", BRANCO, largura // 2 - fonte.size(f"Vidas restantes: {vidas}")[0] // 2, altura // 2 - 60)
        desenhar_texto("Deseja continuar?", BRANCO, largura // 2 - fonte_media.size("Deseja continuar?")[0] // 2, altura // 2 - 20, fonte_obj=fonte_media)


        # Desenha Botões
        # Botão Continuar
        pygame.draw.rect(janela, AZUL_CLARO, (250, 270, 300, 50))
        desenhar_texto("Sim (gastar 1 vida)", BRANCO, 250 + (300 - fonte.size("Sim (gastar 1 vida)")[0]) // 2, 270 + (50 - fonte.size("Sim (gastar 1 vida)")[1]) // 2)

        # Botão Não Continuar / Sair
        pygame.draw.rect(janela, VERMELHO, (250, 350, 300, 50))
        desenhar_texto("Não / Sair", BRANCO, 250 + (300 - fonte.size("Não / Sair")[0]) // 2, 350 + (50 - fonte.size("Não / Sair")[1]) // 2)

        pygame.display.flip()
        clock.tick(60)


#Loop principal
execuntando = True
while execuntando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            execuntando = False

    if estado_jogo == MENU_INICIAL:
        tela_menu_inicial()
    elif estado_jogo == JOGANDO:
        # Movimento da plataforma
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and plataforma_x > 0:
            plataforma_x -= velocidade_plataforma
        if teclas[pygame.K_RIGHT] and plataforma_x < largura - plataforma_largura:
            plataforma_x += velocidade_plataforma

        # Atualiza posição da bola
        velocidade_bola_y += gravidade
        bola_x += velocidade_bola_x
        bola_y += velocidade_bola_y

        # Colisão com as laterais da janela
        if bola_x - raio <= 0 or bola_x + raio >= largura:
            velocidade_bola_x *= -1 # Inverte a direção horizontal

        # Colisão com a parte superior da janela
        if bola_y - raio <= 0:
            velocidade_bola_y *= -1 # Inverte a direção vertical

        # Colisão com a parte inferior da janela (perde vida ou game over)
        if bola_y + raio >= altura:
            if vidas > 1:
                estado_jogo = PERGUNTA_CONTINUAR
            else:
                estado_jogo = GAME_OVER

        # Colisão com a plataforma
        if (plataforma_y <= bola_y + raio <= plataforma_y + plataforma_altura) and \
           (plataforma_x <= bola_x <= plataforma_x + plataforma_largura):
            velocidade_bola_y = FORCA_REBOTE_VERTICAL # AQUI é onde a altura do salto é fixa
            pontuacao += 1

            # Verifica e aplica os estágios de dificuldade
            if estagio_atual_dificuldade_indice + 1 < len(ESTAGIOS_DIFICULDADE) and \
               pontuacao >= ESTAGIOS_DIFICULDADE[estagio_atual_dificuldade_indice + 1]["pontos_necessarios"]:
                estagio_atual_dificuldade_indice += 1
                aplicar_dificuldade()

        # desenha janela
        janela.fill(AZUL_CLARO)

        # Bola
        pygame.draw.circle(janela, AMARELO, (int(bola_x), int(bola_y)), raio)

        # Plataforma
        pygame.draw.rect(janela, VERDE, (plataforma_x, plataforma_y, plataforma_largura, plataforma_altura))

        # Pontuação e Vidas
        desenhar_texto(f'Pontos: {pontuacao}', BRANCO, 10, 10)
        desenhar_texto(f'Vidas: {vidas}', BRANCO, 10, 40)
        desenhar_texto(f'Dificuldade: {estagio_atual_dificuldade_indice + 1}', BRANCO, 10, 70)


        # Atualiza a tela
        pygame.display.flip()
        clock.tick(60)
    elif estado_jogo == PERGUNTA_CONTINUAR:
        tela_pergunta_continuar()
    elif estado_jogo == GAME_OVER:
        tela_game_over()

pygame.quit()
sys.exit()