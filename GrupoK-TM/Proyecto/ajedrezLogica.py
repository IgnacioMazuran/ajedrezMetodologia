from copy import deepcopy
from random import choice
from time import sleep, time
#mascara de colores donde se ubican  las piezas (Blanco y Negro)
COLOR_MASK = 1 << 3
BLANCO = 0 << 3
NEGRO = 1 << 3
#Total  tipos de piezas disponibles ordenas segun su importancia en el juego(de peones a rey )
FINJUEG_PIEZA_RESUL = 7

PIEZA_MASK = 0b111
VACIO   = 0
PEON    = 1
CABALLO = 2
ALFIL   = 3
TORRE   = 4
QUEEN   = 5
KING    = 6
#tipo de piezas disponibles
PIEZA_TIPOS = [ PEON, CABALLO, ALFIL, TORRE, QUEEN, KING ]
#valor de las piezas
PIEZA_VALOR = { VACIO:0, PEON:100, CABALLO:300, ALFIL:300, TORRE:500, QUEEN:900, KING:42000 }
#ELEMENTOS FILAS(HORIZONTALES) , ELEMENTOS RANGO(VERTICAL)
FILAS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
RANGOS = ['1', '2', '3', '4', '5', '6', '7', '8']

ENROCAR_KINGSIDE_BLANCO  = 0b1 << 0
ENROCAR_QUEENSIDE_BLANCO = 0b1 << 1
ENROCAR_KINGSIDE_NEGRO   = 0b1 << 2
ENROCAR_QUEENSIDE_NEGRO  = 0b1 << 3
#TOTAL DE CASTILLOS DISPONIBLES EN EL TABLERO
FULL_ENROQUE_REGLAS = ENROCAR_KINGSIDE_BLANCO|ENROCAR_QUEENSIDE_BLANCO|ENROCAR_KINGSIDE_NEGRO|ENROCAR_QUEENSIDE_NEGRO
#POSICION , NUMERO DE RANGO (PERTENECIENTE A CADA ELEMENTO DE LAS FILAS ) 
CASILLEROS        = 0xFFFFFFFFFFFFFFFF
FILA_A            = 0x0101010101010101
FILA_B            = 0x0202020202020202
FILA_C            = 0x0404040404040404
FILA_D            = 0x0808080808080808
FILA_E            = 0x1010101010101010
FILA_F            = 0x2020202020202020
FILA_G            = 0x4040404040404040
FILA_H            = 0x8080808080808080
RANGO_1           = 0x00000000000000FF
RANGO_2           = 0x000000000000FF00
RANGO_3           = 0x0000000000FF0000
RANGO_4           = 0x00000000FF000000
RANGO_5           = 0x000000FF00000000
RANGO_6           = 0x0000FF0000000000
RANGO_7           = 0x00FF000000000000
RANGO_8           = 0xFF00000000000000
DIAG_A1H8         = 0x8040201008040201
DIAG_INV_H1A8     = 0x0102040810204080
CASILL_CLAROS    = 0x55AA55AA55AA55AA
CASILL_OSCUROS     = 0xAA55AA55AA55AA55
#filas ordenadas por letras segun su posicion(FILA_A=primera Fila...)
FILA_MASK  = [FILA_A, FILA_B, FILA_C, FILA_D, FILA_E, FILA_F, FILA_G, FILA_H]
#Rangos ordenados por numero segun su posicion
RANGO_MASK = [RANGO_1, RANGO_2, RANGO_3, RANGO_4, RANGO_5, RANGO_6, RANGO_7, RANGO_8]
#ORGANIZACION DE LAS PIEZAS EN EL TABLERO (SECTOR BLANCO Y SECTOR NEGRO) Y ESPACIOS VACIOS(TOTAL)
TABLERO_INICIO = [  BLANCO|TORRE, BLANCO|CABALLO, BLANCO|ALFIL, BLANCO|QUEEN, BLANCO|KING, BLANCO|ALFIL, BLANCO|CABALLO, BLANCO|TORRE,
                    BLANCO|PEON,  BLANCO|PEON,    BLANCO|PEON,  BLANCO|PEON,  BLANCO|PEON, BLANCO|PEON,  BLANCO|PEON,    BLANCO|PEON, 
                  	VACIO,        VACIO,          VACIO,        VACIO,        VACIO,       VACIO,        VACIO,          VACIO,
                  	VACIO,        VACIO,          VACIO,        VACIO,        VACIO,       VACIO,        VACIO,          VACIO,
                  	VACIO,        VACIO,          VACIO,        VACIO,        VACIO,       VACIO,        VACIO,          VACIO,
                  	VACIO,        VACIO,          VACIO,        VACIO,        VACIO,       VACIO,        VACIO,          VACIO,
                  	NEGRO|PEON,   NEGRO|PEON,     NEGRO|PEON,   NEGRO|PEON,   NEGRO|PEON,  NEGRO|PEON,   NEGRO|PEON,     NEGRO|PEON,
                  	NEGRO|TORRE,  NEGRO|CABALLO,  NEGRO|ALFIL,  NEGRO|QUEEN,  NEGRO|KING,  NEGRO|ALFIL,  NEGRO|CABALLO,  NEGRO|TORRE ]

TABLERO_VACIO = [ VACIO for _ in range(64) ]

INICIAL_FEN = 'tcaqkact/pppppppp/8/8/8/8/PPPPPPPP/TCAQKACT w KQkq - 0 1'
STROKES_YOLO = '1k6/2a1p3/Qp4C1/4t2P/2A2q2/1T6/2Pc2K1/8 w - - 0 1'
#IDENTIFICACION DE CADA UNA DE LAS PIEZAS (Con un caracter utilizado como id)
PIEZA_CODIG = { BLANCO|KING :  'K',
                BLANCO|QUEEN:  'Q',
                BLANCO|TORRE:  'T',
                BLANCO|ALFIL:  'A',
                BLANCO|CABALLO:'C',
                BLANCO|PEON:   'P',
                NEGRO |KING :  'k',
                NEGRO |QUEEN:  'q',
                NEGRO |TORRE:  't',
                NEGRO |ALFIL:  'a',
                NEGRO |CABALLO:'c',
                NEGRO |PEON:   'p',
 #se agregan los codigos asignados a cada una de las piezas 
PIEZA_CODIG.update({v: k for k, v in PIEZA_CODIG.items()})
#VALORES ACCIONES DE PEONES Y TORRES
DUPLICA_PEON_PENALIZA      = 10
PEON_AISLADO_PENALIZA      = 20
RETROC_PEON_PENALIZA       = 8
PEON_PASADO_BONUS          = 20
TORRE_SEMI_OPEN_FILE_BONUS = 10
TORRE_OPEN_FILE_BONUS      = 15
TORRE_EN_SEPTIMA_BONUS     = 20
#BONOS POR TIPO DE PIEZA
PEON_BONUS = [0,   0,   0,   0,   0,   0,   0,   0,
              0,   0,   0, -40, -40,   0,   0,   0,
              1,   2,   3, -10, -10,   3,   2,   1,
              2,   4,   6,   8,   8,   6,   4,   2,
              3,   6,   9,  12,  12,   9,   6,   3,
              4,   8,  12,  16,  16,  12,   8,   4,
              5,  10,  15,  20,  20,  15,  10,   5,
              0,   0,   0,   0,   0,   0,   0,   0]

CABALLO_BONUS = [-10, -30, -10, -10, -10, -10, -30, -10,
                 -10,   0,   0,   0,   0,   0,   0, -10,
                 -10,   0,   5,   5,   5,   5,   0, -10,
                 -10,   0,   5,  10,  10,   5,   0, -10,
                 -10,   0,   5,  10,  10,   5,   0, -10,
                 -10,   0,   5,   5,   5,   5,   0, -10,
                 -10,   0,   0,   0,   0,   0,   0, -10,
                 -10, -10, -10, -10, -10, -10, -10, -10]
 
ALFIL_BONUS = [-10, -10, -20, -10, -10, -20, -10, -10,
               -10,   0,   0,   0,   0,   0,   0, -10,
               -10,   0,   5,   5,   5,   5,   0, -10,
               -10,   0,   5,  10,  10,   5,   0, -10,
               -10,   0,   5,  10,  10,   5,   0, -10,
               -10,   0,   5,   5,   5,   5,   0, -10,
               -10,   0,   0,   0,   0,   0,   0, -10,
               -10, -10, -10, -10, -10, -10, -10, -10]

KING_BONUS = [  0,  20,  40, -20,   0, -20,  40,  20,
              -20, -20, -20, -20, -20, -20, -20, -20,
              -40, -40, -40, -40, -40, -40, -40, -40,
              -40, -40, -40, -40, -40, -40, -40, -40,
              -40, -40, -40, -40, -40, -40, -40, -40,
              -40, -40, -40, -40, -40, -40, -40, -40,
              -40, -40, -40, -40, -40, -40, -40, -40,
              -40, -40, -40, -40, -40, -40, -40, -40]

KING_FINJUEG_BONUS = [ 0,  10,  20,  30,  30,  20,  10,   0,
                      10,  20,  30,  40,  40,  30,  20,  10,
                      20,  30,  40,  50,  50,  40,  30,  20,
                      30,  40,  50,  60,  60,  50,  40,  30,
                      30,  40,  50,  60,  60,  50,  40,  30,
                      20,  30,  40,  50,  50,  40,  30,  20,
                      10,  20,  30,  40,  40,  30,  20,  10,
                       0,  10,  20,  30,  30,  20,  10,   0]

verbose = False

# ========== JUEGO ==========

class Juega:
	#funcion donde se instancia el talero Y MOVIMIENTOS
    def __init__(self, FEN=''):
        self.tablero = TABLERO_INICIO
        self.mueve_prim = BLANCO
        self.ep_casill = 0
        self.enroque_reglas = FULL_ENROQUE_REGLAS
        self.halfmove_clock = 0
        self.fullmove_number = 1

        self.posicion_historial = []
        if FEN != '':
            self.load_FEN(FEN)
            self.posicion_historial.append(FEN)
        else:
            self.posicion_historial.append(INICIAL_FEN)
            
        self.movimientos_historial = []
   #FUNCION QUE RETORNA LOS MOVIMIENTOS
    def get_mov_list(self):
        return ' '.join(self.movimientos_historial)
    #FUNCION QUE TRABAJA CON EL RANGO DE MOVIEMIENTOS DE LAS FICHAS (ZONA VERTICAL DEL TABLERO)
    def to_FEN(self):
        FEN_str = ''

        for i in range(len(RANGOS)):
            primer = len(self.tablero) - 8*(i+1)
            vacio_casill = 0
            for fille in range(len(FILAS)):
                pieza = self.tablero[primer+fille]
                if pieza&PIEZA_MASK == VACIO:
                    vacio_casill += 1
                else:
                    if vacio_casill > 0:
                        FEN_str += '{}'.format(vacio_casill)
                    FEN_str += '{}'.format(pieza_str(pieza))
                    vacio_casill = 0
            if vacio_casill > 0:
                FEN_str += '{}'.format(vacio_casill)
            FEN_str += '/'
        FEN_str = FEN_str[:-1] + ' '

        if self.mueve_prim == BLANCO:
            FEN_str += 'b '
        if self.mueve_prim == NEGRO:
            FEN_str += 'n '

        if self.enroque_reglas & ENROCAR_KINGSIDE_BLANCO:
            FEN_str += 'K'
        if self.enroque_reglas & ENROCAR_QUEENSIDE_BLANCO:
            FEN_str += 'Q'
        if self.enroque_reglas & ENROCAR_KINGSIDE_NEGRO:
            FEN_str += 'k'
        if self.enroque_reglas & ENROCAR_QUEENSIDE_NEGRO:
            FEN_str += 'q'
        if self.enroque_reglas == 0:
            FEN_str += '-'
        FEN_str += ' '

        if self.ep_casill == 0:
            FEN_str += '-'
        else:
            FEN_str += bb2str(self.ep_casill)

        FEN_str += ' {}'.format(self.halfmove_clock)
        FEN_str += ' {}'.format(self.fullmove_number)
        return FEN_str
    # funcion que separa y ordena las piezas del tablero(Blancas y Negras ) en una especie de Lista o cadena separadas
    # una de otra instanciado los objetos que seran invocados para utilizar el metodo 
    def load_FEN(self, FEN_str):
        FEN_list = FEN_str.split(' ')
        
        tablero_str = FEN_list[0]
        rango_list = tablero_str.split('/')
        rango_list.reverse()
        self.tablero = []

        for rango in rango_list:
            rango_piezas = []
            for p in rango:
                if p.isdigit():
                    for _ in range(int(p)):
                        rango_piezas.append(VACIO)
                else:
                    rango_piezas.append(pieza_str(p))
            self.tablero.extend(rango_piezas)

        mueve_prim_str = FEN_list[1].lower()
        if mueve_prim_str == 'b':
            self.mueve_prim = BLANCO
        if mueve_prim_str == 'n':
            self.mueve_prim = NEGRO

        enroque_reglas_str = FEN_list[2]
        self.enroque_reglas = 0
        if enroque_reglas_str.find('K') >= 0:
            self.enroque_reglas |= ENROCAR_KINGSIDE_BLANCO
        if enroque_reglas_str.find('Q') >= 0:
            self.enroque_reglas |= ENROCAR_QUEENSIDE_BLANCO
        if enroque_reglas_str.find('k') >= 0:
            self.enroque_reglas |= ENROCAR_KINGSIDE_NEGRO
        if enroque_reglas_str.find('q') >= 0:
            self.enroque_reglas |= ENROCAR_QUEENSIDE_NEGRO

        ep_str = FEN_list[3]
        if ep_str == '-':
            self.ep_casill = 0
        else:
            self.ep_casill = str2bb(ep_str)
        
        self.halfmove_clock = int(FEN_list[4])
        self.fullmove_number = int(FEN_list[5])

# ================================

#se le asigna un indice a los bits disponibles para el tablero
def get_pieza(tablero, bitboard):
    return tablero[bb2index(bitboard)]
#Disonibilidad de espacios disponibles en el tablero para realizar la jugada       
def bb2index(bitboard):
    for i in range(64):
        if bitboard & (0b1 << i):
            return i
#distibucion de filas y rangos en el tablero utilizando una matriz de 8X8
def str2index(posicion_str):
    fille = FILAS.index(posicion_str[0].lower())
    rango = RANGOS.index(posicion_str[1])
    return 8*rango + fille
#se realiza la division de la cantidad de espacios(64) y se los distribuye de forma equitativa entre filas y rangos
def bb2str(bitboard):
    for i in range(64):
        if bitboard & (0b1 << i):
            fille = i%8
            rango = int(i/8)
            return '{}{}'.format(FILAS[fille], RANGOS[rango])
#se encadenan las Letras y Los Rangos uno por uno dentro de los bits correspondientes al tablero
def str2bb(posicion_str):
    return 0b1 << str2index(posicion_str)

def movim2str(movim):
    return bb2str(movim[0]) + bb2str(movim[1])
#se dsitribuye los rangos y Letras dentro del Tablero respetando el rango de 64(Espacios=Mtriz de 8X8)
def indiv_gen(bitboard):
    for i in range(64):
        bit = 0b1 << i
        if bitboard & bit:
            yield bit
#Se distribuyen las piezas en el tablero(Utilizando su codigo o id)  dentro del 
#Rango del tablero (64)
def pieza_gen(tablero, pieza_codig):
    for i in range(64):
        if tablero[i]&PIEZA_MASK == pieza_codig:
            yield 0b1 << i
#Se ordenan las piezas por su codigo y color dentro del Rango del tablero ((64)) 
def pieza_color_gen(tablero, pieza_codig, color):
    for i in range(64):
        if tablero[i] == pieza_codig|color:
            yield 0b1 << i
#devuelve el color opuesto al ordenado            
def opuesto_color(color):
    if color == BLANCO:
        return NEGRO
    if color == NEGRO:
        return BLANCO
#Retorna el codigo de cada pieza 
def pieza_str(pieza):
    return PIEZA_CODIG[pieza]
#Retorna cada pieza atraves de su codigo en cada posicion del Arreglo
def str2pieza(string):
    return PIEZA_CODIG[string]
#Imprime EL orden del tablero de un lado y distribucion de los cuadrados de cada pieza  (8 Letras )
def print_tablero(tablero):
    print('')
    for i in range(len(RANGOS)):
        rango_str = str(8-i) + ' '
        primer = len(tablero) - 8*(i+1)
        for fille in range(len(FILAS)):
            rango_str += '{} '.format(pieza_str(tablero[primer+fille]))
        print(rango_str)
    print('  a b c d e f g h')
#Imprime EL orden del tablero del lado opuesto  y distribucion de los cuadrados de cada pieza  (8 Letras )
#Utilizando la tecnica de espejo
def print_rotar_tablero(tablero):
    r_tablero = rota_tablero(tablero)
    print('')
    for i in range(len(RANGOS)):
        rango_str = str(i+1) + ' '
        primer = len(r_tablero) - 8*(i+1)
        for fille in range(len(FILAS)):
            rango_str += '{} '.format(pieza_str(r_tablero[primer+fille]))
        print(rango_str)
    print('  h g f e d c b a')
#devuelve la distribucion del Tablero comprobando si son Numeros o Caracteres para ordenarlos segun corresponda
def print_bitboard(bitboard):
    print('')
    for rango in range(len(RANGOS)):
        rango_str = str(8-rango) + ' '
        for fille in range(len(FILAS)):
            if (bitboard >> (fille + (7-rango)*8)) & 0b1:
                rango_str += '# '
            else:
                rango_str += '. '
        print(rango_str)
    print('  a b c d e f g h')
#Retorna los bits correspondiente dentro del rango de tablero (64)
def lsb(bitboard):
    for i in range(64):
        bit = (0b1 << i) 
        if bit & bitboard:
            return bit
#Retorna los bit correspondientes a medida que se recorre el arreglo de bits se lo va restando al total del Tablero
def msb(bitboard):
    for i in range(64):
        bit = (0b1 << (63-i)) 
        if bit & bitboard:
            return bit
#obtiene el color de cada pieza del tablero avanzando atraves de un arreglo
def get_piezas_color(tablero, color):
    return list2int([ (i != VACIO and i&COLOR_MASK == color) for i in tablero ])
#obtiene color de los caudros vacios avanzando atraves de un arreglo
def vacio_casilleros(tablero):
    return list2int([ i == VACIO for i in tablero ])
#Permite identificar los cuadrados ocupados en el tablero devolviendo los que no cumplen la condicion de  Vacios
def ocupado_casilleros(tablero):
    return nnot(vacio_casilleros(tablero))
#invierte la lista de las piezas
def list2int(lst):
    rev_list = lst[:]
    rev_list.reverse()
    return int('0b' + ''.join(['1' if i else '0' for i in rev_list]), 2)

def nnot(bitboard):
    return ~bitboard & CASILLEROS
#recibe el tablero y lo rota 
def rota_tablero(tablero):
    rotar_tablero = deepcopy(tablero)
    rotar_tablero.reverse()
    return rotar_tablero
#copia el tablero invertido dentro del rango del tablero(64)
def inv_tablero_v(tablero):
    inv =  [56,  57,  58,  59,  60,  61,  62,  63,
            48,  49,  50,  51,  52,  53,  54,  55,
            40,  41,  42,  43,  44,  45,  46,  47,
            32,  33,  34,  35,  36,  37,  38,  39,
            24,  25,  26,  27,  28,  29,  30,  31,
            16,  17,  18,  19,  20,  21,  22,  23,
             8,   9,  10,  11,  12,  13,  14,  15,
             0,   1,   2,   3,   4,   5,   6,   7]

    return deepcopy([tablero[inv[i]] for i in range(64)])
#retorna  opuesto de Fila A 
def lado_este(bitboard):
    return (bitboard << 1) & nnot(FILA_A)
#retorna opuesto Fila H del lado contrario de tablero
def lado_oeste(bitboard):
    return (bitboard >> 1) & nnot(FILA_H)
#Retorna los rangos para el Usuario desde 8 a 1 
def lado_norte(bitboard):
    return (bitboard << 8) & nnot(RANGO_1)
#Rtorna los rangos del lado opuesto desde 1 a 8
def lado_sur(bitboard):
    return (bitboard >> 8) & nnot(RANGO_8)
#Retorna primer bit NE
def lado_NE(bitboard):
    return lado_norte(lado_este(bitboard))
#Retorna primer bit NO
def lado_NO(bitboard):
    return lado_norte(lado_oeste(bitboard))
#Retorna primer bit SE
def lado_SE(bitboard):
    return lado_sur(lado_este(bitboard))
#Retrona primer bit SO
def lado_SO(bitboard):
    return lado_sur(lado_oeste(bitboard))
#Retorna espacio libre luego de un movimiento
def mueve_pieza(tablero, movim):
    new_tablero = deepcopy(tablero)
    new_tablero[bb2index(movim[1])] = new_tablero[bb2index(movim[0])] 
    new_tablero[bb2index(movim[0])] = VACIO
    return new_tablero
#nueva posicion adquirida en el tablero
def mueve(juega, movim):
    new_juega = deepcopy(juega)
    abandona_posicion = movim[0]
    nueva_posicion = movim[1]

    # actualiza_reloj
    new_juega.halfmove_clock += 1
    if new_juega.mueve_prim == NEGRO:
        new_juega.fullmove_number += 1

    # resetea reloj con captura
    if get_pieza(new_juega.tablero, nueva_posicion) != VACIO:
        new_juega.halfmove_clock = 0

    # peones: resetea reloj, remueve ep capturado, establece nuevo ep, promote
    if get_pieza(new_juega.tablero, abandona_posicion)&PIEZA_MASK == PEON:
        new_juega.halfmove_clock = 0
        
        if nueva_posicion == juega.ep_casill:
            new_juega.tablero = remueve_ep_capturado(new_juega)
    
        if doble_avance(abandona_posicion, nueva_posicion):
            new_juega.ep_casill = new_ep_casill(abandona_posicion)
            
        if nueva_posicion&(RANGO_1|RANGO_8):
            new_juega.tablero[bb2index(abandona_posicion)] = new_juega.mueve_prim|QUEEN

    # resetea ep casill si no fue actualizado
    if new_juega.ep_casill == juega.ep_casill:
        new_juega.ep_casill = 0

    # actualiza reglas de enroque para la torre
    if abandona_posicion == str2bb('a1'):
        new_juega.enroque_reglas = remueve_enroque_reglas(new_juega, ENROCAR_QUEENSIDE_BLANCO)
    if abandona_posicion == str2bb('h1'):
        new_juega.enroque_reglas = remueve_enroque_reglas(new_juega, ENROCAR_KINGSIDE_BLANCO)
    if abandona_posicion == str2bb('a8'):
        new_juega.enroque_reglas = remueve_enroque_reglas(new_juega, ENROCAR_QUEENSIDE_NEGRO)
    if abandona_posicion == str2bb('h8'):
        new_juega.enroque_reglas = remueve_enroque_reglas(new_juega, ENROCAR_KINGSIDE_NEGRO)

    # enroque
    if get_pieza(new_juega.tablero, abandona_posicion) == BLANCO|KING:
        new_juega.enroque_reglas = remueve_enroque_reglas(new_juega, ENROCAR_KINGSIDE_BLANCO|ENROCAR_QUEENSIDE_BLANCO)
        if abandona_posicion == str2bb('e1'):
            if nueva_posicion == str2bb('g1'):
                new_juega.tablero = mueve_pieza(new_juega.tablero, [str2bb('h1'), str2bb('f1')])
            if nueva_posicion == str2bb('c1'):
                new_juega.tablero = mueve_pieza(new_juega.tablero, [str2bb('a1'), str2bb('d1')])

    if get_pieza(new_juega.tablero, abandona_posicion) == NEGRO|KING:
        new_juega.enroque_reglas = remueve_enroque_reglas(new_juega, ENROCAR_KINGSIDE_NEGRO|ENROCAR_QUEENSIDE_NEGRO)
        if abandona_posicion == str2bb('e8'):
            if nueva_posicion == str2bb('g8'):
                new_juega.tablero = mueve_pieza(new_juega.tablero, [str2bb('h8'), str2bb('f8')])
            if nueva_posicion == str2bb('c8'):
                new_juega.tablero = mueve_pieza(new_juega.tablero, [str2bb('a8'), str2bb('d8')])

    # actualiza posiciones y siguiente movimiento
    new_juega.tablero = mueve_pieza(new_juega.tablero, (abandona_posicion, nueva_posicion))
    new_juega.mueve_prim = opuesto_color(new_juega.mueve_prim)
    
    # actualiza historial
    new_juega.movimientos_historial.append(movim2str(movim))
    new_juega.posicion_historial.append(new_juega.to_FEN())
    return new_juega
#retorna el historial de nuevos moviemientos
def deshace_movim(juega):
    if len(juega.posicion_historial) < 2:
        return deepcopy(juega)
    
    new_juega = Juega(juega.posicion_historial[-2])
    new_juega.movimientos_historial = deepcopy(juega.movimientos_historial)[:-1]
    new_juega.posicion_historial = deepcopy(juega.posicion_historial)[:-1]
    return new_juega
#Retorna el nuevo enmascarado dentro de los rangos 
def get_rango(rango_num):
    rango_num = int(rango_num)
    return RANGO_MASKS[rango_num]
#retorna el numero de la posicion correspondiente a cada fila dentro de la cadena  
def get_fila(fila_str):
    fila_str = fila_str.lower()
    fila_num = FILAS.index(fila_str)
    return FILA_MASK[fila_num]
#Filtra cadenas o rangos segun donde se encuentre 
def get_filtro(filtro_str):
    if filtro_str in FILAS:
        return get_fila(filtro_str)
    if filtro_str in RANGOS:
        return get_rango(filtro_str)


# ===========================

#define situacion de ataque segun color c/contador
def bajo_ataque(objetivo, tablero, atacando_color):
    return cuenta_ataques(objetivo, tablero, atacando_color) > 0
#define situacion de jaque cuando rey esta bajo ataque
def jaque(tablero, color):
    return bajo_ataque(get_king(tablero, color), tablero, opuesto_color(color))
#retorna la pieza la pieza y color que ataca
def get_ataques(moviendo_pieza, tablero, color):
    pieza = tablero[bb2index(moviendo_pieza)]

    if pieza&PIEZA_MASK == PEON:
        return peon_ataca(moviendo_pieza, tablero, color)
    elif pieza&PIEZA_MASK == CABALLO:
        return caballo_ataca(moviendo_pieza)
    elif pieza&PIEZA_MASK == ALFIL:
        return alfil_ataca(moviendo_pieza, tablero, color)
    elif pieza&PIEZA_MASK == TORRE:
        return torre_ataca(moviendo_pieza, tablero, color)
    elif pieza&PIEZA_MASK == QUEEN:
        return queen_ataca(moviendo_pieza, tablero, color)
    elif pieza&PIEZA_MASK == KING:
        return king_ataca(moviendo_pieza)
#define movimiento de piezas anclando el tipo de pieza
def get_movimientos(moviendo_pieza, juega, color):
    pieza = juega.tablero[bb2index(moviendo_pieza)]

    if pieza&PIEZA_MASK == PEON:
        return peon_movimientos(moviendo_pieza, juega, color)
    elif pieza&PIEZA_MASK == CABALLO:
        return caballo_movimientos(moviendo_pieza, juega.tablero, color)
    elif pieza&PIEZA_MASK == ALFIL:
        return alfil_movimientos(moviendo_pieza, juega.tablero, color)
    elif pieza&PIEZA_MASK == TORRE:
        return torre_movimientos(moviendo_pieza, juega.tablero, color)
    elif pieza&PIEZA_MASK == QUEEN:
        return queen_movimientos(moviendo_pieza, juega.tablero, color)
    elif pieza&PIEZA_MASK == KING:
        return king_movimientos(moviendo_pieza, juega.tablero, color)
#contador de ataques por color
def cuenta_ataques(objetivo, tablero, atacando_color):
    ataque_contador = 0

    for index in range(64):
        pieza = tablero[index]
        if pieza != VACIO and pieza&COLOR_MASK == atacando_color:
            pos = 0b1 << index
            
            if get_ataques(pos, tablero, atacando_color) & objetivo:
                ataque_contador += 1
                      
    return ataque_contador
#cuenta el material en tablero
def material_sumat(tablero, color):
    material = 0
    for pieza in tablero:
        if pieza&COLOR_MASK == color:
            material += PIEZA_VALOR[pieza&PIEZA_MASK]
    return material
#evalua diferencia de material entre jugadores
def material_saldo(tablero):
    return material_sumat(tablero, BLANCO) - material_sumat(tablero, NEGRO)
#evalua diferenccia de movimientos entre jugadores
def movimientos_saldo(juega):
    return cont_movim_legales(juega, BLANCO) - cont_movim_legales(juega, NEGRO)
# evalua estado del juego
def evalua_juego(juega):
    if finaliza_juego(juega):
        return evalua_final(juega)
    else:
        return material_saldo(juega.tablero) + saldo_posicion(juega)
#evalua condicion de finalizacion
def evalua_final(juega):
    if jaquemate(juega, juega.mueve_prim):
        return puntaje(juega.mueve_prim)
    elif juego_ahogado(juega) or \
         material_insuficiente(juega) or \
         menos_75_movim_regla(juega):
        return 0


#========= PUNTAJES ==========

def saldo_posicion(juega):
    return bonus_posicion(juega, BLANCO) - bonus_posicion(juega, NEGRO) 

def bonus_posicion(juega, color):
    bonus = 0
    
    if color == BLANCO:
        tablero = juega.tablero
    elif color == NEGRO:
        tablero = inv_tablero_v(juega.tablero)
        
    for index in range(64):
        pieza = tablero[index]
        
        if pieza != VACIO and pieza&COLOR_MASK == color:
            pieza_tipo = pieza&PIEZA_MASK
            
            if pieza_tipo == PEON:
                bonus += PEON_BONUS[index]
            elif pieza_tipo == CABALLO:
                bonus += CABALLO_BONUS[index]
            elif pieza_tipo == ALFIL:
                bonus += ALFIL_BONUS[index]
             
            elif pieza_tipo == TORRE:
                posicion = 0b1 << index
                 
                if is_open_file(posicion, tablero):
                    bonus += TORRE_OPEN_FILE_BONUS
                elif is_semi_open_file(posicion, tablero):
                    bonus += TORRE_SEMI_OPEN_FILE_BONUS
                     
                if posicion & RANGO_7:
                    bonus += TORRE_EN_SEPTIMA_BONUS
                 
            elif pieza_tipo == KING:
                if fin_del_juego(tablero):
                    bonus += KING_FINJUEG_BONUS[index]
                else:
                    bonus += KING_BONUS[index]
    
    return bonus

def fin_del_juego(tablero):
    return cuenta_piezas(ocupado_casilleros(tablero)) <= FINJUEG_PIEZA_RESUL
#open file: fila sin peones
def is_open_file(bitboard, tablero):
    for f in FILAS:
        rango_filtro = get_fila(f)
        if bitboard & rango_filtro:
            return cuenta_piezas(get_peones_total(tablero)&rango_filtro) == 0
#semi open file: fila con peones de un solo color
def is_semi_open_file(bitboard, tablero):
    for f in FILAS:
        rango_filtro = get_fila(f)
        if bitboard & rango_filtro:
            return cuenta_piezas(get_peones_total(tablero)&rango_filtro) == 1
#cuenta espacios ocupados en el tablero de bits
def cuenta_piezas(bitboard):
    return bin(bitboard).count("1")
#evalua puntaje por color
def puntaje(color):
    if color == BLANCO:
        return -10*PIEZA_VALOR[KING]
    if color == NEGRO:
        return 10*PIEZA_VALOR[KING]
#movimientos que no tienen en cuenta las demas piezas
def movim_pseudo_legales(juega, color):
    for index in range(64):
        pieza = juega.tablero[index]

        if pieza != VACIO and pieza&COLOR_MASK == color:
            pieza_pos = 0b1 << index
            
            for objetivo in indiv_gen(get_movimientos(pieza_pos, juega, color)):
                yield (pieza_pos, objetivo)

    if puede_enrocar_kingside(juega, color):
        yield (get_king(juega.tablero, color), lado_este(lado_este(get_king(juega.tablero, color))))
    if puede_enrocar_queenside(juega, color):
        yield (get_king(juega.tablero, color), lado_oeste(lado_oeste(get_king(juega.tablero, color))))
#movimientos permitidos
def movimientos_legales(juega, color):
    for movim in movim_pseudo_legales(juega, color):
        if movim_legal(juega, movim):
            yield movim
#movimientos que no dejan al propio rey en jaque
def movim_legal(juega, movim):
    new_juega = mueve(juega, movim)
    return not jaque(new_juega.tablero, juega.mueve_prim)
#contador de movimientos permitidos
def cont_movim_legales(juega, color):
    cuenta_movim = 0
    for _ in movimientos_legales(juega, color):
        cuenta_movim += 1
    return cuenta_movim

def juego_ahogado(juega):
    for _ in movimientos_legales(juega, juega.mueve_prim):
        return False
    return not jaque(juega.tablero, juega.mueve_prim)
  
def jaquemate(juega, color):
    for _ in movimientos_legales(juega, juega.mueve_prim):
        return False
    return jaque(juega.tablero, color)  

def misma_posicion(FEN_a, FEN_b):
    FEN_a_list = FEN_a.split(' ')
    FEN_b_list = FEN_b.split(' ')
    return FEN_a_list[0] == FEN_b_list[0] and \
           FEN_a_list[1] == FEN_b_list[1] and \
           FEN_a_list[2] == FEN_b_list[2] and \
           FEN_a_list[3] == FEN_b_list[3]

#==== REGLAS ====
#Si la misma posicion ocurre 3 veces -> tablas
def triple_repeticion(juega):
    posicion_actual = juega.posicion_historial[-1]
    cuenta_posicion = 0
    for posicion in juega.posicion_historial:
        if misma_posicion(posicion_actual, posicion):
            cuenta_posicion += 1
    return cuenta_posicion >= 3
#si luego de 50 movimientos no se producen capturas -> tablas
def menos_50_movim_regla(juega):
    return juega.halfmove_clock >= 100
#si no hay capturas en 75 movimientos -> tablas
def menos_75_movim_regla(juega):
    return juega.halfmove_clock >= 150
#EVALUA LAS 4 COMBINACIONES PARA QUE SE DE UN EMPATE POR MATERIAL INSUFICIENTE (MATERIALES SON LAS PIEZAS 
#EN EL TABLERO), LA REGLA TIENE EN CUENTA ALFILES, CABALLOS Y REY
def material_insuficiente(juega):
    if material_sumat(juega.tablero, BLANCO) + material_sumat(juega.tablero, NEGRO) == 2*PIEZA_VALOR[KING]:
        return True
    if material_sumat(juega.tablero, BLANCO) == PIEZA_VALOR[KING]:
        if material_sumat(juega.tablero, NEGRO) == PIEZA_VALOR[KING] + PIEZA_VALOR[CABALLO] and \
        (get_caballos(juega.tablero, NEGRO) != 0 or get_alfiles(game.tablero, NEGRO) != 0):
            return True
    if material_sumat(juega.tablero, NEGRO) == PIEZA_VALOR[KING]:
        if material_sumat(juega.tablero, BLANCO) == PIEZA_VALOR[KING] + PIEZA_VALOR[CABALLO] and \
        (get_caballos(juega.tablero, BLANCO) != 0 or get_alfiles(juega.tablero, BLANCO) != 0):
            return True
    return False #DEVUELVE FALSO SI NO SE DA LA CONDICION

#devuelve la condicion del juego terminado
def finaliza_juego(juega):
    return jaquemate(juega, BLANCO) or \
           jaquemate(juega, NEGRO) or \
           juego_ahogado(juega) or \
           material_insuficiente(juega) or \
           menos_75_movim_regla(juega)

def movim_aleat(juega, color):
    return choice(movim_legal(juega, color))
#evalua puntajes y guarda los mayores
def movim_evaluado(juega, color):
    mejor_puntaje = puntaje(color)
    mejor_movimientos = []
    
    for movim in movimientos_legales(juega, color):
        evalua = evalua_juego(mueve(juega, movim))
        
        if jaquemate(mueve(juega, movim), opuesto_color(juega.mueve_prim)):
            return [movim, evalua]
        
        if (color == BLANCO and evalua > mejor_puntaje) or \
           (color == NEGRO  and evalua < mejor_puntaje):
            mejor_puntaje = evalua
            mejor_movimientos = [movim]
        elif evalua == mejor_puntaje:
            mejor_movimientos.append(movim)
                
    return [choice(mejor_movimientos), mejor_puntaje]

# ===========================

#genera arbol binario de movimientos optimos 
def minimax(juega, color, profund=1):
    if finaliza_juego(juega):
        return [None, evalua_juego(juega)]
    
    [movim_simple, evaluacion_simple] = movim_evaluado(juega, color)
    
    if profund == 1 or \
       evaluacion_simple == puntaje(opuesto_color(color)):
        return [movim_simple, evaluacion_simple]
    
    mejor_puntaje = puntaje(color)
    mejor_movimientos = []
    
    for movim in movim_legal(juega, color):
        su_juego = mueve(juega, movim)
        
        if jaquemate(su_juego, su_juego.mueve_prim):
            return [movim, puntaje(su_juego.mueve_prim)]
            
        [_, evalua] = minimax(su_juego, opuesto_color(color), profund-1)
        
        if evalua == puntaje(opuesto_color(color)):
            return [movim, evalua]
        
        if (color == BLANCO and evalua > mejor_puntaje) or \
           (color == NEGRO and evalua < mejor_puntaje):
            mejor_puntaje = evalua
            mejor_movimientos = [movim]
        elif evalua == mejor_puntaje:
            mejor_movimientos.append(movim)
        
    return [choice(mejor_movimientos), mejor_puntaje]
#"poda" los subarboles de minimax que considera que NO seran seleccionados
def alpha_beta(juega, color, profund, alpha=-float('inf'), beta=float('inf')):
    if finaliza_juego(juega):
        return [None, evalua_juego(juega)]
    
    [movim_simple, evaluacion_simple] = movim_evaluado(juega, color)
    
    if profund == 1 or \
       evaluacion_simple == puntaje(opuesto_color(color)):
        return [movim_simple, evaluacion_simple]

    mejor_movimientos = []
        
    if color == BLANCO:
        for movim in movimientos_legales(juega, color):
            if verbose:
                print('\t'*profund + str(profund) + '. evaluando ' + PIEZA_CODIG[get_pieza(juega.tablero, movim[0])] + movim2str(movim))
                
            new_juega = mueve(juega, movim)
            [_, puntos] = alpha_beta(new_juega, opuesto_color(color), profund-1, alpha, beta)
            
            if verbose:
                print('\t'*profund + str(profund) + '. ' + str(puntos) + ' [{},{}]'.format(alpha, beta))
            
            if puntos == puntaje(opuesto_color(color)):
                return [movim, puntos]
            
            if puntos == alpha:
                mejor_movimientos.append(movim)
            if puntos > alpha: # blanco maximiza puntaje
                alpha = puntos
                mejor_movimientos = [movim]
                if alpha > beta: # poda alpha-beta 
                    if verbose:
                        print('\t'*profund + 'poda')
                    break
        if mejor_movimientos:
            return [choice(mejor_movimientos), alpha]
        else:
            return [None, alpha]
    
    if color == NEGRO:
        for movim in movimientos_legales(juega, color):
            if verbose:
                print('\t'*profund + str(profund) + '. evaluando ' + PIEZA_CODIG[get_pieza(juega.tablero, movim[0])] + movim2str(movim))
                
            new_juega = mueve(juega, movim)
            [_, puntos] = alpha_beta(new_juega, opuesto_color(color), profund-1, alpha, beta)
            
            if verbose:
                print('\t'*profund + str(profund) + '. ' + str(puntos) + ' [{},{}]'.format(alpha, beta))
            
            if puntos == puntaje(opuesto_color(color)):
                return [movim, puntos]
            
            if puntos == beta:
                mejor_movimientos.append(movim)
            if puntos < beta: # negro minimiza puntaje
                beta = puntos
                mejor_movimientos = [movim]
                if alpha > beta: # poda alpha-beta
                    if verbose:
                        print('\t'*profund + 'poda')
                    break
        if mejor_movimientos:
            return [choice(mejor_movimientos), beta]
        else:
            return [None, beta]
#evalua condiciones para hacer el movimiento
def analiza_codig_movim(juega, movim_codigo):
    movim_codigo = movim_codigo.replace(" ","")
    movim_codigo = movim_codigo.replace("x","")

    if movim_codigo.upper() == 'O-O' or movim_codigo == '0-0':
        if puede_enrocar_kingside(juega, juega.mueve_prim):
            return enrocar_kingside_movim(juega)
        
    if movim_codigo.upper() == 'O-O-O' or movim_codigo == '0-0-0':
        if puede_enrocar_queenside(juega, juega.mueve_prim):
            return enrocar_queenside_movim(juega)

    if len(movim_codigo) < 2 or len(movim_codigo) > 4:
        return False
    
    if len(movim_codigo) == 4:
        filtra_casilleros = get_filtro(movim_codigo[1])
    else:
        filtra_casilleros = CASILLEROS

    destino_str = movim_codigo[-2:]
    if destino_str[0] in FILAS and destino_str[1] in RANGOS:
        casill_objetivo = str2bb(destino_str)
    else:
        return False

    if len(movim_codigo) == 2:
        pieza = PEON
    else:
        pieza_codig = movim_codigo[0]
        if pieza_codig in FILAS:
            pieza = PEON
            filtra_casilleros = get_filtro(pieza_codig)
        elif pieza_codig in PIEZA_CODIG:
            pieza = PIEZA_CODIG[pieza_codig]&PIEZA_MASK
        else:
            return False

    movim_validos = []
    for movim in movim_legal(juega, juega.mueve_prim):
        if movim[1] & casill_objetivo and \
           movim[0] & filtra_casilleros and \
           get_pieza(juega.tablero, movim[0])&PIEZA_MASK == pieza:
            movim_validos.append(movim) 

    if len(movim_validos) == 1:
        return movim_validos[0]
    else:
        return False
#obtiene y evalua el movimiento del usuario
def get_movim_usuario(juega):
    movim = None
    while not movim:
        movim = analiza_codig_movim(juega, input())
        if not movim:
            print('Movimiento No Váido!!!')
    return movim
#obtiene y evalua el movimiento de la AI
def get_AI_movim(juega, profund=2):
    if verbose:
        print('Blanco analizando mejor jugada...' if juega.mueve_prim == BLANCO else 'Negro analizando mejor jugada...')
    start_time = time()

    if busca_en_libro(juega):
        movim = get_movim_libro(juega)  #movimiento de libro ("book.txt")
    else:
        movim = alpha_beta(juega, juega.mueve_prim, profund)[0]

    end_time = time()
    if verbose:
        print('Movimiento encontrado ' + PIEZA_CODIG[get_pieza(juega.tablero, movim[0])] + ' desde ' + str(bb2str(movim[0])) + ' hasta ' + str(bb2str(movim[1])) + ' en {:.3f} segundos'.format(end_time-start_time) + ' ({},{})'.format(evalua_juego(juega), evalua_juego(mueve(juega, movim))))
    return movim    #retorna el movimiento y detiene el reloj
#imprime salida por pantalla
def print_salida(juega):
    print(get_salida(juega))
#obtiene salida
def get_salida(juega):
    if juego_ahogado(juega):
        return 'Empate por Juego Ahogado'
    if jaquemate(juega, BLANCO):
        return 'NEGRAS ganan!'
    if jaquemate(juega, NEGRO):
        return 'BLANCAS ganan!'
    if material_insuficiente(juega):
        return 'Empate por piezas insuficientes!'
    if menos_75_movim_regla(juega):
        return 'Empate por regla de los 75 movimientos!'

#==== MODOS DE JUEGO ====

def juega_con_blancas(juega=Juega()):
    print('Jugador: BLANCAS!')
    while True:
        print_tablero(juega.tablero)
        if finaliza_juego(juega):
            break

        juega = mueve_prim(juega, get_movim_usuario(juega))
        
        print_tablero(juega.tablero)
        if finaliza_juego(juega):
            break
        
        juega = mueve_prim(juega, get_AI_movim(juega))
    print_salida(juega)

def juega_con_negras(juega=Juega()):
    print('Jugador: NEGRAS!')
    while True:
        print_rotar_tablero(juega.tablero)
        if finaliza_juego(juega):
            break

        juega = mueve(juega, get_AI_movim(juega))
        
        print_rotar_tablero(juega.tablero)
        if finaliza_juego(juega):
            break
        
        juega = mueve(juega, get_movim_usuario(juega))
    print_salida(juega)

def modo_espectador(juega=Juega(), sleep_seconds=0):
    print('Modo espectador:  AI vs AI ')
    while True:
        print_tablero(juega.tablero)
        if finaliza_juego(juega):
            break
                
        juega = mueve(juega, get_AI_movim(juega))
        sleep(sleep_seconds)
    print_salida(juega)

def juega_con(color):
    if color == BLANCO:
        juega_con_blancas()
    if color == NEGRO:
        juega_con_negras()

def juega_con_aleatorio():
    color = choice([BLANCO, NEGRO])
    juega_con(color)

#==== FICHERO ====

def busca_en_libro(juega):
    if juega.posicion_historial[0] != INICIAL_FEN:
        return False

    fichero = []
    fichero_libro = open("book.txt")
    for line in fichero_libro:
        if line.startswith(juega.get_mov_list()) and line.rstrip() > juega.get_mov_list():
            fichero.append(line.rstrip())
    fichero_libro.close()
    return fichero

def get_movim_libro(juega):
    fichero = busca_en_libro(juega)
    opc_fichero = choice(fichero)
    movim_siguientes = opc_fichero.replace(juega.get_mov_list(), '').lstrip()
    movim_str = movim_siguientes.split(' ')[0]
    movim = [str2bb(movim_str[:2]), str2bb(movim_str[-2:])]
    return movim
