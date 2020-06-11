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

