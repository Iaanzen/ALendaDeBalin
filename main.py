import pygame

pygame.init()

tela = pygame.display.set_mode((800, 480))
pygame.display.set_caption("A Lenda de Balin")

clock = pygame.time.Clock()

#Personagem
x, y = 100, 300
largura, altura = 40, 60
vel_x = 0
vel_y = 0
gravidade = 0.5
no_chao = False
velocidade = 5

#mapa
largura_mapa = 3000

#Plataformas
plataformas = [
    (0, 420, largura_mapa, 20),
    (200, 300, 150, 20),
    (500, 200, 150, 20),
]




rodando = True

while rodando:
    # 1. Ler eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP and no_chao:
                vel_y = -12

    # 2. Atualizar estado
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        vel_x = -velocidade
    elif teclas[pygame.K_RIGHT]:
        vel_x = velocidade
    else:
        vel_x = 0

    vel_y += gravidade  # gravidade puxando pra baixo

    x += vel_x
    y_anterior = y
    y += vel_y


    rect_balin = pygame.Rect(x, y, largura, altura)

    no_chao = False

    for plataforma in plataformas:
        rect_plataforma = pygame.Rect(plataforma)
        if rect_balin.colliderect(rect_plataforma):
            if vel_y > 0 and y_anterior + altura <= plataforma[1] + vel_y:
                y = plataforma[1] - altura
                vel_y = 0
                no_chao = True



    #Parede Temporária
    if x >= largura_mapa - largura:
        x = largura_mapa - largura
    if x <= 0:
        x = 0


    # 3. Desenhar tela
    camera_x = x - 400
    tela.fill((30, 30, 30))  # fundo cinza escuro
    pygame.draw.rect(tela, (100, 200, 100), (x - camera_x, y, largura, altura))
    for plataforma in plataformas:
        pygame.draw.rect(tela, (150, 75, 0), (plataforma[0] - camera_x, plataforma[1], plataforma[2], plataforma[3]))
    pygame.display.flip()

    clock.tick(60)  # limita a 60 frames por segundo

pygame.quit()