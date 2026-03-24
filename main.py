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

rodando = True

while rodando:
    # 1. Ler eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_w and no_chao:
                vel_y = -10

    # 2. Atualizar estado
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_a]:
        vel_x = -velocidade
    elif teclas[pygame.K_d]:
        vel_x = velocidade
    else:
        vel_x = 0

    vel_y += gravidade  # gravidade puxando pra baixo

    x += vel_x
    y += vel_y

    # Chão temporário
    if y >= 400:
        y = 400
        vel_y = 0
        no_chao = True
    else:
        no_chao = False

    #Parede Temporária
    if x >= 800 - largura:
        x = 800 - largura
        vel_x = 0
    if x <= 0:
        x = 0
        vel_x = 0

    # 3. Desenhar tela
    tela.fill((30, 30, 30))  # fundo cinza escuro
    pygame.draw.rect(tela, (100, 200, 100), (x, y, largura, altura))
    pygame.display.flip()

    clock.tick(60)  # limita a 60 frames por segundo

pygame.quit()