# kwarwp.kwarwp.main.py
# SPDX-License-Identifier: GPL-3.0-or-later
""" Jogo para ensino de programação Python.

    .. codeauthor:: Carlo Oliveira <carlo@ufrj.br>

    Classes neste módulo:
        - :py:class:`Kwarwp`    Jogo para ensino de programação.
        - :py:class:`Indio`     Personagem principal do jogo.
        - :py:class:`Vazio`     Espaço vago na arena do desafio.
        - :py:class:`Oca`       Destino final da aventura.
        - :py:class:`Piche`     Uma armadilha para prender o índio.

    Changelog
    ---------
    .. versionchanged::    20.08.b0
        Moveu constantes de classe VITOLLINO, LADO para Vazio.
        Moveu :class:`Vazio`, :class:`Oca`, :class:`Piche` para kwarwpart.
        
    .. versionadded::    20.08.a3
        Movimentação do índio para :py:meth:`Indio.esquerda` e 
        :py:meth:`Indio.direita`. Fala do índio: :py:meth:`Indio.fala`.
        classes Oca e Piche, double dispatch para sair.
            
    .. versionadded::    20.08.a2
        Classe Vazio que recebe cada componente do mapa.
        Movimentação do índio é feita pulando para outro vazio.
            
    .. versionadded::    20.08.a1
        Classe Indio que executa roteiro e anda.
            
    .. versionadded::    20.08.a0
        Fábrica de componentes
        classe Indio.
        Usa um mapa de caracteres para colocar os elementos.
            
    .. versionadded::    20.07
        classe Kwarwp.

"""
from collections import namedtuple as nt
from kwarwp.kwarwpart import Vazio, Piche, Oca, Tora, NULO

IMGUR = "https://imgur.com/"
"""Prefixo do site imgur."""
MAPA_INICIO = """
@....&
......
......
.#.^..
"""
"""Mapa com o posicionamento inicial dos elementos."""
Ponto = nt("Ponto", "x y")
"""Par de coordenadas na direção horizontal (x) e vertiacal (y)."""
Rosa = nt("Rosa", "n l s o")
"""Rosa dos ventos com as direções norte, leste, sul e oeste."""


class Indio():
    """ Cria o personagem principal na arena do Kwarwp na posição definida.

        :param imagem: A figura representando o índio na posição indicada.
        :param x: Coluna em que o elemento será posicionado.
        :param y: Cinha em que o elemento será posicionado.
        :param cena: Cena em que o elemento será posicionado.
        :param taba: Representa a taba onde o índio faz o desafio.
    """
    AZIMUTE = Rosa(Ponto(0, -1),Ponto(1, 0),Ponto(0, 1),Ponto(-1, 0),)
    """Constante com os pares ordenados que representam os vetores unitários dos pontos cardeais."""
    
    def __init__(self, imagem, x, y, cena, taba):
        self.lado = lado = Vazio.LADO
        self.azimute = self.AZIMUTE.n
        """índio olhando para o norte"""
        self.taba = taba
        self.vaga = self
        self.ocupante = NULO
        self.posicao = (x//lado,y//lado)
        self.indio = Vazio.VITOLLINO.a(imagem, w=lado, h=lado, x=x, y=y, cena=cena)
        self.x = x
        """Este x provisoriamente distingue o índio de outras coisas construídas com esta classe"""
        if x:
            self.indio.siz = (lado*3, lado*4)
            """Define as proporções da folha de sprites"""
            self.mostra()

    def mostra(self):
        """ Modifica a figura (Sprite) do índio mostrando para onde está indo.
        """
        sprite_col = sum(self.posicao) % 3
        """Faz com que três casas adjacentes tenha valores diferentes para a coluna do sprite"""
        sprite_lin = self.AZIMUTE.index(self.azimute)
        """A linha do sprite depende da direção dque índio está olhando"""
        self.indio.pos = (-self.lado*sprite_col, -self.lado*sprite_lin)

    def esquerda(self):
        """ Faz o índio mudar da direção em que está olhando para a esquerda.
        """
        self.azimute = self.AZIMUTE[self.AZIMUTE.index(self.azimute)-1]
        self.mostra()

    def direita(self):
        """ Faz o índio mudar da direção em que está olhando para a direita.
        """
        self.azimute = self.AZIMUTE[self.AZIMUTE.index(self.azimute)-3]
        self.mostra()

    def fala(self, texto=""):
        """ O índio fala um texto dado.
        
        :param texto: O texto a ser falado.
        """
        self.taba.fala(texto)

    def anda(self):
        """Objeto tenta sair, tem que consultar a vaga onde está"""
        self.vaga.sair()      

    def pega(self):
        """tenta pegar o objeto que está diante dele"""
        destino = (self.posicao[0]+self.azimute.x, self.posicao[1]+self.azimute.y)
        """A posição para onde o índio vai depende do vetor de azimute corrente"""
        taba = self.taba.taba
        if destino in taba:
            vaga = taba[destino]
            """Recupera na taba a vaga para a qual o índio irá se transferir"""
            vaga.pegar(self)

    def larga(self):
        """tenta largar o objeto que está segurando"""
        destino = (self.posicao[0]+self.azimute.x, self.posicao[1]+self.azimute.y)
        """A posição para onde o índio vai depende do vetor de azimute corrente"""
        taba = self.taba.taba
        if destino in taba:
            vaga = taba[destino]
            """Recupera na taba a vaga para a qual o índio irá se transferir"""
            # self.ocupante.largar(vaga)
            vaga.acessa(self.ocupante)

    def sair(self):
        """Objeto de posse do índio tenta sair e é autorizado"""
        self.vaga.ocupante.siga()      

    def siga(self):
        """Objeto tentou sair e foi autorizado"""
        self._anda()       

    def _anda(self):
        """ Faz o índio caminhar na direção em que está olhando.
        """
        destino = (self.posicao[0]+self.azimute.x, self.posicao[1]+self.azimute.y)
        """A posição para onde o índio vai depende do vetor de azimute corrente"""
        taba = self.taba.taba
        if destino in taba:
            vaga = taba[destino]
            """Recupera na taba a vaga para a qual o índio irá se transferir"""
            vaga.acessa(self)
 
    def ocupou(self, ocupante):
        """ O candidato à vaga decidiu ocupá-la e efetivamente entra neste espaço.
        
        :param ocupante: O canditato a ocupar a posição corrente.
        
        Este ocupante vai entrar no elemento do Vitollino e definitivamente se tornar
        o ocupante da vaga. Com isso ele troca o estado do método acessa para primeiro
        consultar a si mesmo, o ocupante corrente usando o protocolo definido em
        **_valida_acessa ()**

        """
        self.indio.ocupa(ocupante)
        self.ocupante = ocupante
        
    def sai(self):
        """ Rotina de saída falsa, o objeto Indio é usado como uma vaga nula.
        """
        pass
         
    def executa(self):
        """ Roteiro do índio. Conjunto de comandos para ele executar.
        """
        self.anda()

    @property        
    def elt(self):
        """ A propriedade elt faz parte do protocolo do Vitollino para anexar um elemento no outro .

        No caso do índio, retorna o elt do elemento do atributo **self.indio**.
        """
        return self.indio.elt
        
    def ocupa(self, vaga):
        """ Pedido por uma vaga para que ocupe a posição nela.
        
        :param vaga: A vaga que será ocupada pelo componente.

        No caso do índio, requisita que a vaga seja ocupada por ele.
        """
        self.vaga.sai()
        self.posicao = vaga.posicao
        vaga.ocupou(self)
        self.vaga = vaga
        if self.x:
            self.mostra()
        
    def acessa(self, ocupante):
        """ Pedido de acesso a essa posição, delegada ao ocupante pela vaga.
        
        :param ocupante: O componente candidato a ocupar a vaga já ocupada pelo índio.

        No caso do índio, ele age como um obstáculo e não prossegue com o protocolo.
        """
        pass


class Kwarwp():
    """ Jogo para ensino de programação.
    
        :param vitollino: Empacota o engenho de jogo Vitollino.
        :param mapa: Um texto representando o mapa do desafio.
        :param medidas: Um dicionário usado para redimensionar a tela.
    """
    
    def __init__(self, vitollino=None, mapa=MAPA_INICIO, medidas={}):
        Vazio.VITOLLINO = self.v = vitollino()
        """Referência estática para obter o engenho de jogo."""
        self.mapa = mapa.split()
        """Cria um matriz com os elementos descritos em cada linha de texto"""
        self.taba = {}
        """Cria um dicionário com os elementos traduzidos a partir da interpretação do mapa"""
        self.o_indio = NULO
        """Instância do personagem principal, o índio, vai ser atribuído pela fábrica do índio"""
        self.lado, self.col, self.lin = 100, len(self.mapa[0]), len(self.mapa)+1
        """Largura da casa da arena dos desafios, número de colunas e linhas no mapa"""
        Vazio.LADO = self.lado
        """Referência estática para definir o lado do piso da casa."""
        #kmain(self)
        w, h = self.col *self.lado, self.lin *self.lado
        medidas.update(width=w, height=f"{h}px")
        #self.cena = self.cria(mapa=self.mapa) if vitollino else None

    def cria(self, mapa=""):
        """ Fábrica de componentes.
        
        :param mapa: Um texto representando o mapa do desafio.
        """
        Fab = nt("Fab", "objeto imagem")
        """Esta tupla nomeada serve para definir o objeto construido e sua imagem."""

        fabrica = {
        "&": Fab(self.maloc, f"{IMGUR}dZQ8liT.jpg"), # OCA
        "^": Fab(self.indio, f"{IMGUR}UCWGCKR.png"), # INDIO
        ".": Fab(self.vazio, f"{IMGUR}npb9Oej.png"), # VAZIO
        "_": Fab(self.coisa, f"{IMGUR}sGoKfvs.jpg"), # SOLO
        "#": Fab(self.atora, f"{IMGUR}0jSB27g.png"), # TORA
        "@": Fab(self.barra, f"{IMGUR}tLLVjfN.png"), # PICHE
        "~": Fab(self.coisa, f"{IMGUR}UAETaiP.gif"), # CEU
        "*": Fab(self.coisa, f"{IMGUR}PfodQmT.gif"), # SOL
        "|": Fab(self.coisa, f"{IMGUR}uwYPNlz.png")  # CERCA       
        }
        """Dicionário que define o tipo e a imagem do objeto para cada elemento."""
        mapa = mapa if mapa != "" else self.mapa
        """Cria um cenário com imagem de terra de chão batido, céu e sol"""
        mapa = self.mapa
        lado = self.lado
        cena = self.v.c(fabrica["_"].imagem)
        self.ceu = self.v.a(fabrica["~"].imagem, w=lado*self.col, h=lado-10, x=0, y=0, cena=cena, vai=self.executa,
                       style={"padding-top": "10px", "text-align": "center"})
        """No argumento *vai*, associamos o clique no céu com o método **executa ()** desta classe.
           O *ceu* agora é um argumento de instância e por isso é referenciado como **self.ceu**.
        """
        sol = self.v.a(fabrica["*"].imagem, w=60, h=60, x=0, y=40, cena=cena, vai=self.esquerda)
        """No argumento *vai*, associamos o clique no sol com o método **esquerda ()** desta classe."""
        self.taba = {(i, j): fabrica[imagem].objeto(fabrica[imagem].imagem, x=i*lado, y=j*lado+lado, cena=cena)
            for j, linha in enumerate(mapa) for i, imagem in enumerate(linha)}
        """Posiciona os elementos segundo suas posições i, j na matriz mapa"""
        cena.vai()
        return cena
        
    def fala(self, texto=""):
        """ O Kwarwp é aqui usado para falar algo que ficará escrito no céu.
        """
        self.ceu.elt.html = texto
        pass
        
    def sai(self, *_):
        """ O Kwarwp é aqui usado como uma vaga falsa, o pedido de sair é ignorado.
        """
        pass
        
    def ocupa(self, *_):
        """ O Kwarwp é aqui usado como um ocupante falso, o pedido de ocupar é ignorado.
        """
        pass
        
    def esquerda(self, *_):
        """ Ordena a execução do roteiro do índio.
        """
        self.o_indio.esquerda()
        
    def executa(self, *_):
        """ Ordena a execução do roteiro do índio.
        """
        self.o_indio.executa()
        
    def atora(self, imagem, x, y, cena):
        """ Cria uma tora na arena do Kwarwp na posição definida.

        :param x: coluna em que o elemento será posicionado.
        :param y: linha em que o elemento será posicionado.
        :param cena: cena em que o elemento será posicionado.
        
        Cria uma vaga vazia e coloca o componente dentro dela.
        """
        coisa = Tora(imagem, x=0, y=0, cena=cena, taba=self)
        vaga = Vazio("", x=x, y=y, cena=cena, ocupante=coisa)
        coisa.vazio.vai = lambda *_: self.o_indio.larga()
        return vaga
        
    def maloc(self, imagem, x, y, cena):
        """ Cria uma maloca na arena do Kwarwp na posição definida.

        :param x: coluna em que o elemento será posicionado.
        :param y: linha em que o elemento será posicionado.
        :param cena: cena em que o elemento será posicionado.
        
        Cria uma vaga vazia e coloca o componente dentro dela.
        """
        coisa = Oca(imagem, x=0, y=0, cena=cena, taba=self)
        vaga = Vazio("", x=x, y=y, cena=cena, ocupante=coisa)
        return vaga
        
    def barra(self, imagem, x, y, cena):
        """ Cria uma armadilha na arena do Kwarwp na posição definida.

        :param x: coluna em que o elemento será posicionado.
        :param y: linha em que o elemento será posicionado.
        :param cena: cena em que o elemento será posicionado.
        
        Cria uma vaga vazia e coloca o componente dentro dela.
        """
        coisa = Piche(imagem, x=0, y=0, cena=cena, taba=self)
        vaga = Vazio("", x=x, y=y, cena=cena, ocupante=coisa)
        return vaga
        
    def coisa(self, imagem, x, y, cena):
        """ Cria um elemento na arena do Kwarwp na posição definida.

        :param x: coluna em que o elemento será posicionado.
        :param y: linha em que o elemento será posicionado.
        :param cena: cena em que o elemento será posicionado.
        
        Cria uma vaga vazia e coloca o componente dentro dela.
        """
        coisa = Indio(imagem, x=0, y=0, cena=cena, taba=self)
        vaga = Vazio("", x=x, y=y, cena=cena, ocupante=coisa)
        return vaga
        
    def vazio(self, imagem, x, y, cena):
        """ Cria um espaço vazio na arena do Kwarwp na posição definida.

        :param x: coluna em que o elemento será posicionado.
        :param y: linha em que o elemento será posicionado.
        :param cena: cena em que o elemento será posicionado.
        """
        vaga = Vazio(imagem, x=x, y=y, cena=cena, ocupante=NULO)
        """ O Kwarwp é aqui usado como um ocupante nulo, que não ocupa uma vaga vazia."""
        return vaga
        
    def indio(self, imagem, x, y, cena):
        """ Cria o personagem principal na arena do Kwarwp na posição definida.

        :param x: coluna em que o elemento será posicionado.
        :param y: linha em que o elemento será posicionado.
        :param cena: cena em que o elemento será posicionado.
        """
        self.o_indio = Indio(imagem, x=1, y=0, cena=cena, taba=self)
        """ O índio tem deslocamento zero, pois é relativo à vaga.
            O **x=1** serve para distinguir o indio de outros derivados.
        """
        self.o_indio.indio.vai = lambda *_: self.o_indio.pega()
        """o índio.vai é associado ao seu próprio metodo pega"""
        vaga = Vazio("", x=x, y=y, cena=cena, ocupante=self.o_indio)
        return vaga


def main(vitollino, medidas={}):
    """ Rotina principal que invoca a classe Kwarwp.
    
    :param vitollino: Empacota o engenho de jogo Vitollino.
    :param medidas: Um dicionário usado para redimensionar a tela.
    """
    # print(f"main(vitollino={vitollino} medidas={medidas}")
    Kwarwp(vitollino, medidas=medidas).cria()
        
    
if __name__ == "__main__":
    from _spy.vitollino.main import Jogo, STYLE
    STYLE.update(width=600, height="500px")
    main(Jogo, STYLE)
