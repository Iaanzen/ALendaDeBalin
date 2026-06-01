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

princesa = NPC(1500, 360, dialogos=[
    "Espere, cavaleiro! Não me mate!",
    "Eu não sou um monstro, apenas sofro com essa maldição...",
    "O que você vai fazer?"
], escolhas=[
    "Cumprir o contrato (Matar)",
    "Esqueça isso, vamos fugir juntos"
], respostas=[
    ["Não... por favor...", "*Você a derrota* (+1000 XP / +500 Ouro)"],
    ["Sério?!", "Eu aceito! Vamos para longe deste reino..."]
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
estado_jogo = "jogando"
missao_aceita = False
npc_atual = None

while rodando:

    rect_balin = pygame.Rect(x, y, largura, altura)
    # 1. Ler eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            # Pulo (Apenas se NÃO estiver em diálogo)
            if not em_dialogo:
                if evento.key == pygame.K_UP and no_chao:
                    vel_y = -12

            # Movimentação nas escolhas (Apenas se ESTIVER em diálogo)
            if em_dialogo and npc_atual:
                if npc_atual.fala_atual == len(npc_atual.dialogos) - 1:
                    if len(npc_atual.escolhas) > 0:
                        if evento.key == pygame.K_DOWN:
                            npc_atual.escolha_atual = (npc_atual.escolha_atual + 1) % len(npc_atual.escolhas)
                        if evento.key == pygame.K_UP:
                            npc_atual.escolha_atual = (npc_atual.escolha_atual - 1) % len(npc_atual.escolhas)

                # --- AVANÇAR DIÁLOGO / CONFIRMAR (ESPAÇO) ---
                if evento.key == pygame.K_SPACE:
                    if npc_atual.fala_atual < len(npc_atual.dialogos) - 1:
                        npc_atual.fala_atual += 1
                    else:
                        # Se o diálogo tem escolhas na tela
                        if npc_atual.escolhas:
                            # Se for o PAI (npc1), salvamos se a missão foi aceita
                            if npc_atual == npc1:
                                if npc_atual.escolha_atual == 0:
                                    missao_aceita = True
                                else:
                                    missao_aceita = False

                            # Aplica os textos de resposta do NPC correspondente
                            npc_atual.dialogos = npc_atual.respostas[npc_atual.escolha_atual]
                            npc_atual.fala_atual = 0
                            npc_atual.escolhas = []
                        else:
                            # O diálogo de RESPOSTA terminou de verdade aqui!
                            npc_atual.fala_atual = 0
                            em_dialogo = False

                            # --- GATILHOS DOS FINAIS ---
                            if npc_atual == npc1:
                                fim_dialogo = True  # Trava o pai para não falar de novo

                                princesa.fala_atual = 0
                                princesa.escolha_atual = 0

                                if not missao_aceita:
                                    estado_jogo = "fim_recusou"

                            elif npc_atual == princesa:
                                # Se a escolha final guardada na princesa foi a 0 (Matar)
                                if princesa.escolha_atual == 0:
                                    estado_jogo = "fim_matou"
                                else:
                                    estado_jogo = "fim_amor"

                            npc_atual = None

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
    if estado_jogo == "jogando":
        tela.fill((30, 30, 30))  # fundo cinza escuro

        if npc1.ver_interacao(rect_balin) and not fim_dialogo:
            em_dialogo = True
            npc_atual = npc1
        elif missao_aceita and princesa.ver_interacao(rect_balin) and not princesa.resposta_atual == -1:
            em_dialogo = True
            npc_atual = princesa
        else:
            em_dialogo = False
            npc_atual = None
        if em_dialogo and npc_atual is not None:
            desenhar_dialogo(tela, npc_atual.dialogos[npc_atual.fala_atual])
            if npc_atual.fala_atual == len(npc_atual.dialogos) - 1:
                desenhar_escolhas(tela, npc_atual.escolhas, npc_atual.escolha_atual)

        frame = sprite_balin.subsurface((frame_atual * 80, linha_animacao * 65, 65, 65))
        frame = pygame.transform.scale(frame, (tamanho_sprite, tamanho_sprite))
        frame = pygame.transform.flip(frame, True, False)
        tela.blit(frame, (x - camera_x, y - (tamanho_sprite - altura)))
        npc1.desenhar(tela, camera_x, )
        if missao_aceita:
            princesa.desenhar(tela, camera_x)
        for plataforma in plataformas:
            pygame.draw.rect(tela, (150, 75, 0), (plataforma[0] - camera_x, plataforma[1], plataforma[2], plataforma[3]))

    elif estado_jogo == "fim_recusou":
        tela.fill((0,0,0))
        fonte = pygame.font.SysFont(None, 35)
        texto_linha1 = fonte.render("FIM DE JOGO", True, (255, 0, 0))  # Vermelho
        texto_linha2 = fonte.render("Você recusou a missão e seguiu para sua próxima aventura.", True, (255, 255, 255))  # Branco
        tela.blit(texto_linha1, (320, 180))
        tela.blit(texto_linha2, (60, 240))

    elif estado_jogo == "fim_matou":
        tela.fill((0, 0, 0))
        fonte = pygame.font.SysFont(None, 35)
        texto_linha1 = fonte.render("FIM: O MERCENÁRIO", True, (255, 215, 0))  # Dourado
        texto_linha2 = fonte.render("Você derrotou a princesa! Ganhou +1000 XP e +500 Ouro.", True,(255, 255, 255))
        texto_linha3 = fonte.render("Mas e se ela não estivesse amaldiçoada?", True,(255, 255, 255))
        tela.blit(texto_linha1, (280, 180))
        tela.blit(texto_linha2, (70, 240))
        tela.blit(texto_linha3, (160, 280))

    elif estado_jogo == "fim_amor":
        tela.fill((20, 10, 20))  # Um fundo levemente roxo/romântico
        fonte = pygame.font.SysFont(None, 30)
        texto_linha1 = fonte.render("FIM: AMOR PROIBIDO", True, (255, 105, 180))  # Rosa
        texto_linha2 = fonte.render("Você poupou a Princesa. Vocês fugiram juntos para viver uma nova vida.", True,(255, 255, 255))
        tela.blit(texto_linha1, (280, 180))
        tela.blit(texto_linha2, (45, 240))

    pygame.display.flip()
    clock.tick(60)  # limita a 60 frames por segundo

pygame.quit()