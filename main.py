import pygame

pygame.init()

tela = pygame.display.set_mode((800, 480))
pygame.display.set_caption("A Lenda de Balin")

clock = pygame.time.Clock()

#Personagem
x, y = 100, 300
largura, altura = 40, 50
tamanho_sprite = 160
vel_x = 0
vel_y = 0
gravidade = 0.5
no_chao = False
velocidade = 5

#NPC
class NPC:
    def __init__(self, x, y, w=40, h=60, dialogos=[], escolhas=[], respostas=[]):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.dialogos = dialogos
        self.fala_atual = 0
        self.escolhas = escolhas
        self.escolha_atual = 0
        self.respostas = respostas
        self.resposta_atual = 0


    def desenhar(self, tela, camera_x):
        pygame.draw.rect(tela, (100, 200, 100), (self.x - camera_x, self.y, self.w, self.h ))

    def ver_interacao(self, rect_balin):
        area = pygame.Rect(self.x - 40, self.y, self.w + 40, self.h)
        return area.colliderect(rect_balin)



npc1 = NPC(400, 360, dialogos=[
    "Cavaleiro, preciso da sua ajuda...",
    "Dizem que minha filha está amaldiçoada.",
    "Você toparia resolver isso por mim?"
], escolhas = [
    "Sim, farei o serviço",
    "Não posso fazer isso"
], respostas =[
    ["Graças aos Deuses!", "Minha filha está dentro de casa, cumpra sua missão", "Você será bem recompensado!"],
    ["Entendo...", "Talvez outro cavaleiro seja capaz de tal tarefa..."]
])

#Caixa de diálogo

def desenhar_dialogo(tela, texto):
    pygame.draw.rect(tela, (100, 200, 255), (0, 300, 800, 200))
    fonte = pygame.font.SysFont(None, 32)
    texto_render = fonte.render(texto, True, (255, 255, 255))
    tela.blit(texto_render, (20, 330))

def desenhar_escolhas(tela, escolhas, escolha_atual):
    fonte = pygame.font.SysFont(None, 32)
    for i, escolha in enumerate(escolhas):
        cor = (255, 255, 0) if i == escolha_atual else (255, 255, 255)
        texto_render = fonte.render(escolha, True, (cor))
        tela.blit(texto_render, (20, 370 + i * 35))
def desenhar_resposta(tela, texto):
    pygame.draw.rect(tela, (100, 200, 255), (0, 300, 800, 200))
    fonte = pygame.font.SysFont(None, 32)
    texto_render = fonte.render(texto, True, (255, 255, 255))
    tela.blit(texto_render, (20, 330))

#mapa
largura_mapa = 3000

#Plataformas
plataformas = [
    (0, 420, largura_mapa, 20),
]

#Sprites
sprite_balin = pygame.image.load("sprites/balin/GandalfHardcore Warrior.png").convert_alpha()

#FPS
frame_atual = 0
contador_frames = 0
linha_animacao = 0
frames_por_animacao = {0: 5, 1: 7, 3: 4}

rodando = True
em_dialogo = False
fim_dialogo = False

while rodando:
    # 1. Ler eventos
    rect_balin = pygame.Rect(x, y, largura, altura)
    # 1. Ler eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if not em_dialogo:
                if evento.key == pygame.K_UP and no_chao:
                    vel_y = -12
                    fim_dialogo = False
            if npc1.fala_atual == len(npc1.dialogos) - 1:
                if evento.key == pygame.K_DOWN:
                    npc1.escolha_atual = (npc1.escolha_atual + 1) % len(npc1.escolhas)
                if evento.key == pygame.K_UP:
                    npc1.escolha_atual = (npc1.escolha_atual + 1) % len(npc1.escolhas)
            if evento.key == pygame.K_SPACE:
                if npc1.fala_atual < len(npc1.dialogos) - 1:
                    npc1.fala_atual += 1
                else:
                    if npc1.escolhas:
                        npc1.dialogos = npc1.respostas[npc1.escolha_atual]
                        npc1.fala_atual = 0
                        npc1.escolhas = []

                    else:
                        npc1.fala_atual = 0
                        em_dialogo = False
                        fim_dialogo = True

    # 2. Atualizar estado
    if not em_dialogo:
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            vel_x = -velocidade
        elif teclas[pygame.K_RIGHT]:
            vel_x = velocidade
        else:
            vel_x = 0
    else:
        vel_x = 0

    linha_anterior = linha_animacao

    if vel_y < -2:
        linha_animacao = 3
    elif vel_x != 0:
        linha_animacao = 1
    else:
        linha_animacao = 0

    if linha_animacao != linha_anterior:
        frame_atual = 0
        contador_frames = 0

    if frame_atual >= frames_por_animacao[linha_animacao]:  # ← depois do reset
        frame_atual = 0

    contador_frames += 1
    if contador_frames >= 8:
        contador_frames = 0
        frame_atual += 1
        if frame_atual >= frames_por_animacao[linha_animacao]:
            frame_atual = 0

    vel_y += gravidade
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

    if npc1.ver_interacao(rect_balin) and not fim_dialogo:
        em_dialogo = True
        desenhar_dialogo(tela, npc1.dialogos[npc1.fala_atual])
        if npc1.fala_atual == len(npc1.dialogos) - 1:
            desenhar_escolhas(tela, npc1.escolhas, npc1.escolha_atual)
    else:
        em_dialogo = False
    frame = sprite_balin.subsurface((frame_atual * 80, linha_animacao * 65, 65, 65))
    frame = pygame.transform.scale(frame, (tamanho_sprite, tamanho_sprite))
    frame = pygame.transform.flip(frame, True, False)
    tela.blit(frame, (x - camera_x, y - (tamanho_sprite - altura)))
    npc1.desenhar(tela, camera_x, )
    for plataforma in plataformas:
        pygame.draw.rect(tela, (150, 75, 0), (plataforma[0] - camera_x, plataforma[1], plataforma[2], plataforma[3]))
    pygame.display.flip()

    clock.tick(60)  # limita a 60 frames por segundo

pygame.quit()