from copy import deepcopy
from random import choice
from time import sleep, time

COLOR_MASK = 1 << 3
BLANCO = 0 << 3
NEGRO = 1 << 3

FINJUEG_PIEZA_RESUL = 7

PIEZA_MASK = 0b111
VACIO   = 0
PEON    = 1
CABALLO = 2
ALFIL   = 3
TORRE   = 4
QUEEN   = 5
KING    = 6

PIEZA_TIPOS = [ PEON, CABALLO, ALFIL, TORRE, QUEEN, KING ]
PIEZA_VALOR = { VACIO:0, PEON:100, CABALLO:300, ALFIL:300, TORRE:500, QUEEN:900, KING:42000 }

FILAS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
RANGOS = ['1', '2', '3', '4', '5', '6', '7', '8']

ENROCAR_KINGSIDE_BLANCO  = 0b1 << 0
ENROCAR_QUEENSIDE_BLANCO = 0b1 << 1
ENROCAR_KINGSIDE_NEGRO   = 0b1 << 2
ENROCAR_QUEENSIDE_NEGRO  = 0b1 << 3

FULL_ENROQUE_REGLAS = ENROCAR_KINGSIDE_BLANCO|ENROCAR_QUEENSIDE_BLANCO|ENROCAR_KINGSIDE_NEGRO|ENROCAR_QUEENSIDE_NEGRO

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

FILA_MASK  = [FILA_A, FILA_B, FILA_C, FILA_D, FILA_E, FILA_F, FILA_G, FILA_H]
RANGO_MASK = [RANGO_1, RANGO_2, RANGO_3, RANGO_4, RANGO_5, RANGO_6, RANGO_7, RANGO_8]

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
                VACIO:         '.' }
PIEZA_CODIG.update({v: k for k, v in PIEZA_CODIG.items()})

DUPLICA_PEON_PENALIZA      = 10
PEON_AISLADO_PENALIZA      = 20
RETROC_PEON_PENALIZA       = 8
PEON_PASADO_BONUS          = 20
TORRE_SEMI_OPEN_FILE_BONUS = 10
TORRE_OPEN_FILE_BONUS      = 15
TORRE_EN_SEPTIMA_BONUS     = 20

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

    def get_mov_list(self):
        return ' '.join(self.movimientos_historial)
    
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


def get_pieza(tablero, bitboard):
    return tablero[bb2index(bitboard)]
        
def bb2index(bitboard):
    for i in range(64):
        if bitboard & (0b1 << i):
            return i

def str2index(posicion_str):
    fille = FILAS.index(posicion_str[0].lower())
    rango = RANGOS.index(posicion_str[1])
    return 8*rango + fille

def bb2str(bitboard):
    for i in range(64):
        if bitboard & (0b1 << i):
            fille = i%8
            rango = int(i/8)
            return '{}{}'.format(FILAS[fille], RANGOS[rango])

def str2bb(posicion_str):
    return 0b1 << str2index(posicion_str)

def movim2str(movim):
    return bb2str(movim[0]) + bb2str(movim[1])

def indiv_gen(bitboard):
    for i in range(64):
        bit = 0b1 << i
        if bitboard & bit:
            yield bit

def pieza_gen(tablero, pieza_codig):
    for i in range(64):
        if tablero[i]&PIEZA_MASK == pieza_codig:
            yield 0b1 << i

def pieza_color_gen(tablero, pieza_codig, color):
    for i in range(64):
        if tablero[i] == pieza_codig|color:
            yield 0b1 << i
            
def opuesto_color(color):
    if color == BLANCO:
        return NEGRO
    if color == NEGRO:
        return BLANCO

def pieza_str(pieza):
    return PIEZA_CODIG[pieza]

def str2pieza(string):
    return PIEZA_CODIG[string]

def print_tablero(tablero):
    print('')
    for i in range(len(RANGOS)):
        rango_str = str(8-i) + ' '
        primer = len(tablero) - 8*(i+1)
        for fille in range(len(FILAS)):
            rango_str += '{} '.format(pieza_str(tablero[primer+fille]))
        print(rango_str)
    print('  a b c d e f g h')

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

def lsb(bitboard):
    for i in range(64):
        bit = (0b1 << i) 
        if bit & bitboard:
            return bit

def msb(bitboard):
    for i in range(64):
        bit = (0b1 << (63-i)) 
        if bit & bitboard:
            return bit

def get_piezas_color(tablero, color):
    return list2int([ (i != VACIO and i&COLOR_MASK == color) for i in tablero ])

def vacio_casilleros(tablero):
    return list2int([ i == VACIO for i in tablero ])

def ocupado_casilleros(tablero):
    return nnot(vacio_casilleros(tablero))

def list2int(lst):
    rev_list = lst[:]
    rev_list.reverse()
    return int('0b' + ''.join(['1' if i else '0' for i in rev_list]), 2)

def nnot(bitboard):
    return ~bitboard & CASILLEROS

def rota_tablero(tablero):
    rotar_tablero = deepcopy(tablero)
    rotar_tablero.reverse()
    return rotar_tablero

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

def lado_este(bitboard):
    return (bitboard << 1) & nnot(FILA_A)

def lado_oeste(bitboard):
    return (bitboard >> 1) & nnot(FILA_H)

def lado_norte(bitboard):
    return (bitboard << 8) & nnot(RANGO_1)

def lado_sur(bitboard):
    return (bitboard >> 8) & nnot(RANGO_8)

def lado_NE(bitboard):
    return lado_norte(lado_este(bitboard))

def lado_NO(bitboard):
    return lado_norte(lado_oeste(bitboard))

def lado_SE(bitboard):
    return lado_sur(lado_este(bitboard))

def lado_SO(bitboard):
    return lado_sur(lado_oeste(bitboard))

def mueve_pieza(tablero, movim):
    new_tablero = deepcopy(tablero)
    new_tablero[bb2index(movim[1])] = new_tablero[bb2index(movim[0])] 
    new_tablero[bb2index(movim[0])] = VACIO
    return new_tablero

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

def deshace_movim(juega):
    if len(juega.posicion_historial) < 2:
        return deepcopy(juega)
    
    new_juega = Juega(juega.posicion_historial[-2])
    new_juega.movimientos_historial = deepcopy(juega.movimientos_historial)[:-1]
    new_juega.posicion_historial = deepcopy(juega.posicion_historial)[:-1]
    return new_juega

def get_rango(rango_num):
    rango_num = int(rango_num)
    return RANGO_MASKS[rango_num]
     
def get_fila(fila_str):
    fila_str = fila_str.lower()
    fila_num = FILAS.index(fila_str)
    return FILA_MASK[fila_num]

def get_filtro(filtro_str):
    if filtro_str in FILAS:
        return get_fila(filtro_str)
    if filtro_str in RANGOS:
        return get_rango(filtro_str)
def get_peones_total(tablero):
    return list2int([ i&PIEZA_MASK == PEON for i in tablero ])  #obtiene todos los peones del tablero

def get_peones(tablero, color):  #obtiene todos los peones de un color y del otro
    return list2int([ i == color|PEON for i in tablero ])

def peon_movimientos(moviendo_pieza, juega, color): #obtiene  el peon que fue movido o desplazado tomando como referencia su color
    return peon_avance(moviendo_pieza, juega.tablero, color) | peon_capturas(moviendo_pieza, juega, color)

def peon_capturas(moviendo_pieza, juega, color):
    return peon_simple_capturas(moviendo_pieza, juega, color) | peon_ep_capturas(moviendo_pieza, juega, color)

def peon_avance(moviendo_pieza, tablero, color):
    return peon_simple_avance(moviendo_pieza, tablero, color) | peon_doble_avance(moviendo_pieza, tablero, color)

def peon_simple_capturas(atacando_pieza, juega, color): #obtiene el ataque del peon y la pieza que fue atacada tomando como referencia el color del peon
    return peon_ataca(atacando_pieza, juega.tablero, color) & get_piezas_color(juega.tablero, opuesto_color(color))    #linea 29- 39 movimientos del peon

def peon_ep_capturas(atacando_pieza, juega, color):  #retorna el rango y color del cuadrado que quedo libre luego del ataque del peon y lo retorna
    if color == BLANCO:
        ep_casilleros = juega.ep_casill & RANGO_6
    if color == NEGRO:
        ep_casilleros = juega.ep_casill & RANGO_3
    return peon_ataca(atacando_pieza, juega.tablero, color) & ep_casilleros

def peon_ataca(atacando_pieza, tablero, color):  #retorna los peones que atacaron tomado como referencia el este y oeste del tablero
    return peon_este_ataca(atacando_pieza, tablero, color) | peon_oeste_ataca(atacando_pieza, tablero, color)

def peon_simple_avance(moviendo_pieza, tablero, color):
    if color == BLANCO:
        return lado_norte(moviendo_pieza) & vacio_casilleros(tablero)
    if color == NEGRO:
        return lado_sur(moviendo_pieza) & vacio_casilleros(tablero)

def peon_doble_avance(moviendo_pieza, tablero, color):
    if color == BLANCO:
        return lado_norte(peon_simple_avance(moviendo_pieza, tablero, color)) & (vacio_casilleros(tablero) & RANGO_4)
    if color == NEGRO:
        return lado_sur(peon_simple_avance(moviendo_pieza, tablero, color)) & (vacio_casilleros(tablero) & RANGO_5)

def peon_este_ataca(atacando_pieza, tablero, color):
    if color == BLANCO:
        return lado_NE(atacando_pieza & get_piezas_color(tablero, color))
    if color == NEGRO:
        return lado_SE(atacando_pieza & get_piezas_color(tablero, color))

def peon_oeste_ataca(atacando_pieza, tablero, color):
    if color == BLANCO:
        return lado_NO(atacando_pieza & get_piezas_color(tablero, color))
    if color == NEGRO:
        return lado_SO(atacando_pieza & get_piezas_color(tablero, color))

def peon_doble_ataca(atacando_pieza, tablero, color):
    return peon_este_ataca(atacando_pieza, tablero, color) & peon_este_ataca(atacando_pieza, tablero, color)

def doble_avance(abandona_casillero, destino_casillero):
    return (abandona_casillero&RANGO_2 and destino_casillero&RANGO_4) or \
           (abandona_casillero&RANGO_7 and destino_casillero&RANGO_5)

def new_ep_casill(abandona_casillero):
    if abandona_casillero&RANGO_2:
        return lado_norte(abandona_casillero)
    if abandona_casillero&RANGO_7:
        return lado_sur(abandona_casillero)

def remueve_ep_capturado(juega):
    new_tablero = deepcopy(juega.tablero)
    if juega.ep_casill & RANGO_3:
        new_tablero[bb2index(lado_norte(juega.ep_casill))] = VACIO
    if juega.ep_casill & RANGO_6:
        new_tablero[bb2index(lado_sur(juega.ep_casill))] = VACIO
    return new_tablero

# ========== Caballos ==========
#obtine la lista de los caballos

def get_caballos(tablero, color):
    return list2int([ i == color|CABALLO for i in tablero ])

def caballo_movimientos(moviendo_pieza, tablero, color):
    return caballo_ataca(moviendo_pieza) & nnot(get_piezas_color(tablero, color))

def caballo_ataca(moviendo_pieza):
    return caballo_NNE(moviendo_pieza) | \
           caballo_ENE(moviendo_pieza) | \
           caballo_NNO(moviendo_pieza) | \
           caballo_ONO(moviendo_pieza) | \
           caballo_SSE(moviendo_pieza) | \
           caballo_ESE(moviendo_pieza) | \
           caballo_SSO(moviendo_pieza) | \
           caballo_OSO(moviendo_pieza)

def caballo_ONO(moviendo_pieza):
    return moviendo_pieza << 6 & nnot(FILA_G | FILA_H)

def caballo_ENE(moviendo_pieza):
    return moviendo_pieza << 10 & nnot(FILA_A | FILA_B)

def caballo_NNO(moviendo_pieza):
    return moviendo_pieza << 15 & nnot(FILA_H)

def caballo_NNE(moviendo_pieza):
    return moviendo_pieza << 17 & nnot(FILA_A)

def caballo_ESE(moviendo_pieza):
    return moviendo_pieza >> 6 & nnot(FILA_A | FILA_B)

def caballo_OSO(moviendo_pieza):
    return moviendo_pieza >> 10 & nnot(FILA_G | FILA_H)

def caballo_SSE(moviendo_pieza):
    return moviendo_pieza >> 15 & nnot(FILA_A)

def caballo_SSO(moviendo_pieza):
    return moviendo_pieza >> 17 & nnot(FILA_H)

def caballo_llena(moviendo_pieza, n):
    llena = moviendo_pieza
    for _ in range(n):
        llena |= caballo_ataca(llena)
    return llena

def caballo_distancia(pos1, pos2):
    init_bitboard = str2bb(pos1)
    end_bitboard = str2bb(pos2)
    llena = init_bitboard
    dist = 0
    while llena & end_bitboard == 0:
        dist += 1
        llena = caballo_llena(init_bitboard, dist)
    return dist

# ========== REY ==========
#obtiene rey segun su color
def get_king(tablero, color):
    return list2int([ i == color|KING for i in tablero ])

def king_movimientos(moviendo_pieza, tablero, color):
    return king_ataca(moviendo_pieza) & nnot(get_piezas_color(tablero, color))

def king_ataca(moviendo_pieza):
    king_atq = moviendo_pieza | lado_este(moviendo_pieza) | lado_oeste(moviendo_pieza)
    king_atq |= lado_norte(king_atq) | lado_sur(king_atq)
    return king_atq & nnot(moviendo_pieza)

def puede_enrocar_kingside(juega, color):
    if color == BLANCO:
        return (juega.enroque_reglas & ENROCAR_KINGSIDE_BLANCO) and \
                juega.tablero[str2index('f1')] == VACIO and \
                juega.tablero[str2index('g1')] == VACIO and \
                (not bajo_ataque(str2bb('e1'), juega.tablero, opuesto_color(color))) and \
                (not bajo_ataque(str2bb('f1'), juega.tablero, opuesto_color(color))) and \
                (not bajo_ataque(str2bb('g1'), juega.tablero, opuesto_color(color)))
    if color == NEGRO:
        return (juega.enroque_reglas & ENROCAR_KINGSIDE_NEGRO) and \
                juega.tablero[str2index('f8')] == VACIO and \
                juega.tablero[str2index('g8')] == VACIO and \
                (not bajo_ataque(str2bb('e8'), juega.tablero, opuesto_color(color))) and \
                (not bajo_ataque(str2bb('f8'), juega.tablero, opuesto_color(color))) and \
                (not bajo_ataque(str2bb('g8'), juega.tablero, opuesto_color(color)))

def puede_enrocar_queenside(juega, color):
    if color == BLANCO:
        return (juega.enroque_reglas & ENROCAR_QUEENSIDE_BLANCO) and \
                juega.tablero[str2index('b1')] == VACIO and \
                juega.tablero[str2index('c1')] == VACIO and \
                juega.tablero[str2index('d1')] == VACIO and \
                (not bajo_ataque(str2bb('c1'), juega.tablero, opuesto_color(color))) and \
                (not bajo_ataque(str2bb('d1'), juega.tablero, opuesto_color(color))) and \
                (not bajo_ataque(str2bb('e1'), juega.tablero, opuesto_color(color)))
    if color == NEGRO:
        return (juega.enroque_reglas & ENROCAR_QUEENSIDE_NEGRO) and \
                juega.tablero[str2index('b8')] == VACIO and \
                juega.tablero[str2index('c8')] == VACIO and \
                juega.tablero[str2index('d8')] == VACIO and \
                (not bajo_ataque(str2bb('c8'), juega.tablero, opuesto_color(color))) and \
                (not bajo_ataque(str2bb('d8'), juega.tablero, opuesto_color(color))) and \
                (not bajo_ataque(str2bb('e8'), juega.tablero, opuesto_color(color)))

def enrocar_kingside_movim(juega):
    if juega.mueve_prim == BLANCO:
        return (str2bb('e1'), str2bb('g1'))
    if juega.mueve_prim == NEGRO:
        return (str2bb('e8'), str2bb('g8'))

def enrocar_queenside_movim(juega):
    if juega.mueve_prim == BLANCO:
        return (str2bb('e1'), str2bb('c1'))
    if juega.mueve_prim == NEGRO:
        return (str2bb('e8'), str2bb('c8'))

def remueve_enroque_reglas(juega, removidas_reglas):
    return juega.enroque_reglas & ~removidas_reglas

# ========== ALFIL ==========

def get_alfiles(tablero, color):
    return list2int([ i == color|ALFIL for i in tablero ])

def alfil_linea(moviendo_pieza):
    return linea_diag(moviendo_pieza) | linea_anti_diag(moviendo_pieza)

def linea_diag(moviendo_pieza):
    return NE_linea(moviendo_pieza) | SO_linea(moviendo_pieza)

def linea_anti_diag(moviendo_pieza):
    return NO_linea(moviendo_pieza) | SE_linea(moviendo_pieza)

def linea_NE(moviendo_pieza):
    linea_atq = lado_NE(moviendo_pieza)
    for _ in range(6):
        linea_atq |= lado_NE(linea_atq)
    return linea_atq & CASILLEROS

def linea_SE(moviendo_pieza):
    linea_atq = lado_SE(moviendo_pieza)
    for _ in range(6):
        linea_atq |= lado_SE(linea_atq)
    return linea_atq & CASILLEROS

def linea_NO(moviendo_pieza):
    linea_atq = lado_NO(moviendo_pieza)
    for _ in range(6):
        linea_atq |= lado_NO(linea_atq)
    return linea_atq & CASILLEROS

def linea_SO(moviendo_pieza):
    linea_atq = lado_SO(moviendo_pieza)
    for _ in range(6):
        linea_atq |= lado_SO(linea_atq)
    return linea_atq & CASILLEROS



def ataca_NE(pieza_indiv, tablero, color):
    bloq = lsb(linea_NE(pieza_indiv) & ocupado_casilleros(tablero))
    if bloq:
        return linea_NE(pieza_indiv) ^ linea_NE(bloq)
    else:
        return linea_NE(pieza_indiv)

def ataca_NO(pieza_indiv, tablero, color):
    bloq = lsb(linea_NO(pieza_indiv) & ocupado_casilleros(tablero))
    if bloq:
        return linea_NO(pieza_indiv) ^ linea_NO(bloq)
    else:
        return linea_NO(pieza_indiv)

def ataca_SE(pieza_indiv, tablero, color):
    bloq = msb(linea_SE(pieza_indiv) & ocupado_casilleros(tablero))
    if bloq:
        return linea_SE(pieza_indiv) ^ linea_SE(bloq)
    else:
        return linea_SE(pieza_indiv)

def ataca_SO(pieza_indiv, tablero, color):
    bloq = msb(linea_SO(pieza_indiv) & ocupado_casilleros(tablero))
    if bloq:
        return linea_SO(pieza_indiv) ^ linea_SO(bloq)
    else:
        return linea_SO(pieza_indiv)

def diagonal_ataca(pieza_indiv, tablero, color):
    return ataca_NE(pieza_indiv, tablero, color) | ataca_SO(pieza_indiv, tablero, color)

def anti_diagonal_ataca(pieza_indiv, tablero, color):
    return ataca_NO(pieza_indiv, tablero, color) | ataca_SE(pieza_indiv, tablero, color)

def alfil_ataca(moviendo_pieza, tablero, color):
    atq = 0
    for pieza in indiv_gen(moviendo_pieza):
        atq |= diagonal_ataca(pieza, tablero, color) | anti_diagonal_ataca(pieza, tablero, color)
    return atq

def alfil_movimientos(moviendo_pieza, tablero, color):
    return alfil_ataca(moviendo_pieza, tablero, color) & nnot(get_piezas_color(tablero, color))

# ========== TORRES ==========
#obtiene TORRES segun su color
def get_torres(board, color):
    return list2int([ i == color|TORRE for i in tablero ])

def torre_lineas(moviendo_pieza):
    return rango_lineas(moviendo_pieza) | fila_lineas(moviendo_pieza)

def rango_lineas(moviendo_pieza):
    return linea_este(moviendo_pieza) | linea_oeste(moviendo_pieza)

def fila_lineas(moviendo_pieza):
    return linea_norte(moviendo_pieza) | linea_sur(moviendo_pieza)

def linea_este(moviendo_pieza):
    linea_atq = lado_este(moviendo_pieza)
    for _ in range(6):
        linea_atq |= lado_este(linea_atq)
    return linea_atq & CASILLEROS

def linea_oeste(moviendo_pieza):
    linea_atq = lado_oeste(moviendo_pieza)
    for _ in range(6):
        linea_atq |= lado_oeste(linea_atq)
    return linea_atq & CASILLEROS

def linea_norte(moviendo_pieza):
    linea_atq = lado_norte(moviendo_pieza)
    for _ in range(6):
        linea_atq |= lado_norte(linea_atq)
    return linea_atq & CASILLEROS

def linea_sur(moviendo_pieza):
    linea_atq = lado_sur(moviendo_pieza)
    for _ in range(6):
        linea_atq |= lado_sur(linea_atq)
    return linea_atq & CASILLEROS

def ataca_este(pieza_indiv, tablero, color):
    bloq = lsb(linea_este(pieza_indiv) & ocupado_casilleros(tablero))
    if bloq:
        return linea_este(pieza_indiv) ^ linea_este(bloq)
    else:
        return linea_este(pieza_indiv)

def ataca_oeste(pieza_indiv, tablero, color):
    bloq = msb(linea_oeste(pieza_indiv) & ocupado_casilleros(tablero))
    if bloq:
        return linea_oeste(pieza_indiv) ^ linea_oeste(bloq)
    else:
        return linea_oeste(pieza_indiv)

def rango_ataca(pieza_indiv, tablero, color):
    return ataca_este(pieza_indiv, tablero, color) | ataca_oeste(pieza_indiv, tablero, color)

def ataca_norte(pieza_indiv, tablero, color):
    bloq = lsb(linea_norte(pieza_indiv) & ocupado_casilleros(tablero))
    if bloq:
        return linea_norte(pieza_indiv) ^ linea_norte(bloq)
    else:
        return linea_norte(pieza_indiv)

def ataca_sur(pieza_indiv, tablero, color):
    bloq = msb(linea_sur(pieza_indiv) & ocupado_casilleros(tablero))
    if bloq:
        return linea_sur(pieza_indiv) ^ linea_sur(bloq)
    else:
        return linea_sur(pieza_indiv)

def fila_ataca(pieza_indiv, tablero, color):
    return ataca_norte(pieza_indiv, tablero, color) | ataca_sur(pieza_indiv, tablero, color)

def torre_ataca(moviendo_pieza, tablero, color):
    atq = 0
    for pieza_indiv in indiv_gen(moviendo_pieza):
        atq |= rango_ataca(pieza_indiv, tablero, color) | fila_ataca(pieza_indiv, tablero, color)
    return atq

def torre_movimientos(moviendo_pieza, tablero, color):
    return torre_ataca(moviendo_pieza, tablero, color) & nnot(get_piezas_color(tablero, color))

# ========== REINA ==========
#obtiene total de  las reinas
def get_queen(tablero, color):
    return list2int([ i == color|QUEEN for i in tablero ])
#retorna los moviemientos disponibles de la reina tomando por referencia concatenacion los de las torres y los alfiles
def queen_lineas(moviendo_pieza):
    return torre_lineas(moviendo_pieza) | alfil_linea(moviendo_pieza)

#retorna los moviemientos de ataque  de la reina tomando por referencia concatenacion los de Alfiles y las torres
def queen_ataca(moviendo_pieza, tablero, color):
    return alfil_ataca(moviendo_pieza, tablero, color) | torre_ataca(moviendo_pieza, tablero, color)
#retorna el moviemiento realizado por la reina
def queen_movimientos(moviendo_pieza, tablero, color):
    return alfil_movimientos(moviendo_pieza, tablero, color) | torre_movimientos(moviendo_pieza, tablero, color)

