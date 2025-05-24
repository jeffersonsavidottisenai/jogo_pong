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

# Definições da bola
raio = 30
bola_x = largura // 2
bola_y = altura // 2
velocidade_bola_x = 5 # Velocidade da bora no eixo x (horizontal)
velocidade_bola_y = 0
gravidade = 0.5

# Configuração da plataforma
plataforma_largura = 150
plataforma_altura = 20
plataforma_x = largura // 2 - plataforma_largura // 2
plataforma_y = altura - 50
velocidade_plataforma = 7

# Pontuação
pontuacao = 0
fonte = pygame.font.SysFont(None, 36)

# Clock
clock = pygame.time.Clock()

# Função para desenhar textos
def desenhar_texto(texto, cor, x, y):
    img = fonte.render(texto, True, cor)
    janela.blit(img, (x, y))

#Loop principal
execuntando = True
while execuntando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimento da pçataforma
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
        velocidade_bola_x *= -1 #Inverte a direção horizontal

    # Colisão com a plataforma
    if (plataforma_y <= bola_y + raio <= plataforma_y + plataforma_altura) and \
       (plataforma_x <= bola_x <= plataforma_x + plataforma_largura):
        velocidade_bola_y = -10 # Rebote vertical
        pontuacao += 1

    # Se a bola cair fora da tela
    if bola_y - raio > altura:
        bola_x = largura // 2
        bola_y = altura // 2
        velocidade_bola_x = 5
        velocidade_bola_y = 0
        pontuacao = 0

    # desenha janela
    janela.fill(AZUL_CLARO)

    # Bola
    pygame.draw.circle(janela, AMARELO, (int(bola_x), int(bola_y)), raio)

    # Plataforma
    pygame.draw.rect(janela, VERDE, (plataforma_x, plataforma_y, plataforma_largura, plataforma_altura))

    # Pontuação
    desenhar_texto(f'Pontos: {pontuacao}', BRANCO, 10, 10)

    # Atualiza a tela
    pygame.display.flip()
    clock.tick(60)
