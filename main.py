import pygame

pygame.init()

tela = pygame.display.set_mode((800, 480))
pygame.display.set_caption("A Lenda de Balin")

clock = pygame.time.Clock()

# Personagem
x, y = 100, 300
largura, altura = 40, 50
tamanho_sprite = 160
vel_x = 0
vel_y = 0
gravidade = 0.5
no_chao = False
velocidade = 5


# NPC
# NPC Animado Automatizado
class NPC:
    def __init__(self, x, y, caminho_sprite=None, frames_animacao=1, tamanho_frame=65, tamanho_render=160, h_ajuste=0,
                 dialogos=[], escolhas=[], respostas=[]):
        self.x = x
        self.y = y
        self.w = 40  # Largura da colisão lógica
        self.h = 50  # Altura da colisão lógica
        self.dialogos = dialogos
        self.fala_atual = 0
        self.escolhas = escolhas
        self.escolha_atual = 0
        self.respostas = respostas
        self.resposta_atual = 0

        # Parâmetros de tamanho do Sprite
        self.tamanho_frame = tamanho_frame
        self.tamanho_render = tamanho_render
        self.h_ajuste = h_ajuste

        # Controle de Animação
        self.frame_atual = 0
        self.contador_frames = 0
        self.frames_animacao = frames_animacao

        self.spritesheet = None
        if caminho_sprite:
            try:
                self.spritesheet = pygame.image.load(caminho_sprite).convert_alpha()

                passo_horizontal = 80 if self.tamanho_frame == 65 else self.tamanho_frame
                largura_total = self.spritesheet.get_width()

                # Calcula o máximo de frames possíveis antes de estourar a borda
                max_frames_possiveis = largura_total // passo_horizontal

                # Se o que você colocou for maior do que existe na imagem, ele corrige sozinho
                if self.frames_animacao > max_frames_possiveis:
                    self.frames_animacao = max_frames_possiveis

            except pygame.error:
                print(f"Erro: Não foi possível carregar caminho {caminho_sprite}")

    def atualizar_animacao(self):
        self.contador_frames += 1
        if self.contador_frames >= 8:  # Velocidade da animação
            self.contador_frames = 0
            self.frame_atual += 1
            # Evita passar do limite total definido na inicialização
            if self.frame_atual >= self.frames_animacao:
                self.frame_atual = 0

    def desenhar(self, tela, camera_x):
        if self.spritesheet:
            self.atualizar_animacao()

            passo_horizontal = 80 if self.tamanho_frame in [64, 65] else self.tamanho_frame
            pos_x_corte = self.frame_atual * passo_horizontal

            # 🛡️ TRAVA ANTICRASH ADICIONAL: Garante que o retângulo nunca saia da imagem
            if pos_x_corte + self.tamanho_frame > self.spritesheet.get_width():
                self.frame_atual = 0
                pos_x_corte = 0

            # Corta o pedaço da imagem
            frame = self.spritesheet.subsurface((pos_x_corte, 0, self.tamanho_frame, self.tamanho_frame))

            # Redimensiona para a tela
            frame_render = pygame.transform.scale(frame, (self.tamanho_render, self.tamanho_render))

            # Inverte o lado para a princesa olhar para a esquerda
            if self.tamanho_frame == 65:
                frame_render = pygame.transform.flip(frame_render, True, False)

            # Desenha na tela
            tela.blit(frame_render, (self.x - camera_x, self.y - (self.tamanho_render - self.h) + self.h_ajuste))
        else:
            pygame.draw.rect(tela, (100, 200, 100), (self.x - camera_x, self.y, self.w, self.h))

    def ver_interacao(self, rect_balin):
        area = pygame.Rect(self.x - 40, self.y, self.w + 40, self.h)
        return area.colliderect(rect_balin)


npc1 = NPC(400, 370, "sprites/fazendeiros/ORANGE FARMER2.png",
           frames_animacao=4, tamanho_frame=32, tamanho_render=120, h_ajuste=0, dialogos=[
        "Cavaleiro, preciso da sua ajuda...",
        "Dizem que minha filha está amaldiçoada.",
        "Você toparia resolver isso por mim?"
    ], escolhas=[
        "Sim, farei o serviço",
        "Não posso fazer isso"
    ], respostas=[
        ["Graças aos Deuses!", "Minha filha está dentro de casa, cumpra sua missão", "Você será bem recompensado!"],
        ["Entendo...", "Talvez outro cavaleiro seja capaz de tal tarefa..."]
    ])

princesa = NPC(1500, 370, "sprites/princesa/GandalfHardcore Goddess NPC.png",
               frames_animacao=1, tamanho_frame=64, tamanho_render=160, h_ajuste=-20, dialogos=[
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


# Caixa de diálogo centralizada
def desenhar_dialogo(tela, texto):
    largura_caixa = 800
    altura_caixa = 160
    pos_x_caixa = (800 - largura_caixa) // 2
    pos_y_caixa = 60

    # Desenha a caixa de fundo
    pygame.draw.rect(tela, (100, 200, 255), (pos_x_caixa, pos_y_caixa, largura_caixa, altura_caixa))

    fonte = pygame.font.SysFont(None, 32)
    texto_render = fonte.render(texto, True, (255, 255, 255))

    # Centraliza o texto horizontalmente com base no tamanho dele
    pos_x_texto = (800 - texto_render.get_width()) // 2
    tela.blit(texto_render, (pos_x_texto, pos_y_caixa + 25))


def desenhar_escolhas(tela, escolhas, escolha_atual):
    fonte = pygame.font.SysFont(None, 32)
    pos_y_inicial = 150

    for i, escolha in enumerate(escolhas):
        cor = (255, 255, 0) if i == escolha_atual else (255, 255, 255)
        texto_render = fonte.render(escolha, True, cor)

        # Centraliza cada opção de escolha horizontalmente
        pos_x_opcao = (800 - texto_render.get_width()) // 2
        tela.blit(texto_render, (pos_x_opcao, pos_y_inicial + i * 35))


def desenhar_botao_reiniciar(tela):
    # Define posição e tamanho do botão (Centralizado na parte inferior da tela)
    largura_btn, altura_btn = 200, 50
    x_btn = (800 - largura_btn) // 2
    y_btn = 360

    rect_botao = pygame.Rect(x_btn, y_btn, largura_btn, altura_btn)

    # Desenha o retângulo do botão (Cinza claro com borda branca)
    pygame.draw.rect(tela, (50, 50, 50), rect_botao)
    pygame.draw.rect(tela, (255, 255, 255), rect_botao, 2)

    # Texto do botão
    fonte = pygame.font.SysFont(None, 30)
    texto = fonte.render("REINICIAR", True, (255, 255, 255))

    # Centraliza o texto dentro do botão
    x_texto = x_btn + (largura_btn - texto.get_width()) // 2
    y_texto = y_btn + (altura_btn - texto.get_height()) // 2
    tela.blit(texto, (x_texto, y_texto))

    return rect_botao

# mapa
largura_mapa = 3000

# Plataformas
plataformas = [
    (0, 420, largura_mapa, 20),
]

# Sprites
sprite_balin = pygame.image.load("sprites/balin/GandalfHardcore Warrior.png").convert_alpha()

# FPS
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
    # 1. Ler eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        # --- EVENTO DE TECLADO (Alinhado corretamente) ---
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

        # --- EVENTO DE CLIQUE DO MOUSE (Agora totalmente independente do teclado!) ---
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if estado_jogo != "jogando":
                pos_mouse = pygame.mouse.get_pos()
                # Cria um rect virtual idêntico ao do botão para testar a colisão do clique
                rect_botao = pygame.Rect((800 - 200) // 2, 360, 200, 50)

                if rect_botao.collidepoint(pos_mouse):
                    # 🔄 RESETA TODAS AS VARIÁVEIS DO JOGO
                    x, y = 100, 300
                    vel_x, vel_y = 0, 0
                    em_dialogo = False
                    fim_dialogo = False
                    missao_aceita = False
                    npc_atual = None

                    # Reseta o Pai
                    npc1.dialogos = [
                        "Cavaleiro, preciso da sua ajuda...",
                        "Dizem que minha filha está amaldiçoada.",
                        "Você toparia resolver isso por mim?"
                    ]
                    npc1.escolhas = ["Sim, farei o serviço", "Não posso fazer isso"]
                    npc1.fala_atual = 0
                    npc1.escolha_atual = 0

                    # Reseta a Princesa
                    princesa.dialogos = [
                        "Espere, cavaleiro! Não me mate!",
                        "Eu não sou um monstro, apenas sofro com essa maldição...",
                        "O que você vai fazer?"
                    ]
                    princesa.escolhas = ["Cumprir o contrato (Matar)", "Esqueça isso, vamos fugir juntos"]
                    princesa.fala_atual = 0
                    princesa.escolha_atual = 0

                    # Volta pro jogo
                    estado_jogo = "jogando"
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

    # Parede Temporária
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

        # Desenha o Balin
        frame = sprite_balin.subsurface((frame_atual * 80, linha_animacao * 65, 65, 65))
        frame = pygame.transform.scale(frame, (tamanho_sprite, tamanho_sprite))
        frame = pygame.transform.flip(frame, True, False)
        tela.blit(frame, (x - camera_x, y - (tamanho_sprite - altura)))

        # Desenha os NPCs
        npc1.desenhar(tela, camera_x)
        if missao_aceita:
            princesa.desenhar(tela, camera_x)

        for plataforma in plataformas:
            pygame.draw.rect(tela, (150, 75, 0),
                             (plataforma[0] - camera_x, plataforma[1], plataforma[2], plataforma[3]))

    elif estado_jogo == "fim_recusou":
        tela.fill((0, 0, 0))
        fonte = pygame.font.SysFont(None, 35)
        texto_linha1 = fonte.render("FIM DE JOGO", True, (255, 0, 0))  # Vermelho
        texto_linha2 = fonte.render("Você recusou a missão e seguiu para sua próxima aventura.", True,
                                    (255, 255, 255))  # Branco
        tela.blit(texto_linha1, (320, 180))
        tela.blit(texto_linha2, (60, 240))
        desenhar_botao_reiniciar(tela)

    elif estado_jogo == "fim_matou":
        tela.fill((0, 0, 0))
        fonte = pygame.font.SysFont(None, 35)
        texto_linha1 = fonte.render("FIM: O MERCENÁRIO", True, (255, 215, 0))  # Dourado
        texto_linha2 = fonte.render("Você derrotou a princesa! Ganhou +1000 XP e +500 Ouro.", True, (255, 255, 255))
        tela.blit(texto_linha1, (280, 180))
        tela.blit(texto_linha2, (70, 240))
        desenhar_botao_reiniciar(tela)

    elif estado_jogo == "fim_amor":
        tela.fill((20, 10, 20))  # Um fundo levemente roxo/romântico
        fonte = pygame.font.SysFont(None, 30)
        texto_linha1 = fonte.render("FIM: AMOR PROIBIDO", True, (255, 105, 180))  # Rosa
        texto_linha2 = fonte.render("Você poupou a Princesa. Vocês fugiram juntos para viver uma nova vida.", True,
                                    (255, 255, 255))
        tela.blit(texto_linha1, (280, 180))
        tela.blit(texto_linha2, (45, 240))
        desenhar_botao_reiniciar(tela)

    pygame.display.flip()
    clock.tick(60)  # limita a 60 frames por segundo

pygame.quit()