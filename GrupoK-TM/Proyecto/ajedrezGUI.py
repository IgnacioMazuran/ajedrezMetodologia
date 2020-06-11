
import pygame, ajedrezLogica
from random import choice
from traceback import format_exc
from sys import stderr
from time import strftime
from copy import deepcopy
pygame.init()

CASILLERO_TAM = 65
AI_BUSCA_PROFUND = 2

JAQUE_ROJO   = (240, 150, 150)
GRIS_CLARO   = (212, 202, 190)
GRIS_OSCURO  = (100,  92,  89)


TABLERO_COLORES = [(GRIS_CLARO, GRIS_OSCURO)]

TABLERO_COLOR = choice(TABLERO_COLORES)

NEGRO_KING    = pygame.image.load('imagenes/rey_negro.png')
NEGRO_QUEEN   = pygame.image.load('imagenes/reina_negra.png')
NEGRO_TORRE   = pygame.image.load('imagenes/torre_negra.png')
NEGRO_ALFIL   = pygame.image.load('imagenes/alfil_negro.png')
NEGRO_CABALLO = pygame.image.load('imagenes/caballo_negro.png')
NEGRO_PEON    = pygame.image.load('imagenes/peon_negro.png')

BLANCO_KING    = pygame.image.load('imagenes/rey_blanco.png')
BLANCO_QUEEN   = pygame.image.load('imagenes/reina_blanca.png')
BLANCO_TORRE   = pygame.image.load('imagenes/torre_blanca.png')
BLANCO_ALFIL   = pygame.image.load('imagenes/alfil_blanco.png')
BLANCO_CABALLO = pygame.image.load('imagenes/caballo_blanco.png')
BLANCO_PEON    = pygame.image.load('imagenes/peon_blanco.png')

RELOJ = pygame.time.Clock()
RELOJ_TICK = 15

VENTANA = pygame.display.set_mode((8*CASILLERO_TAM, 8*CASILLERO_TAM))
VENTANA_TITULO = 'AJEDREZ - Metodologia de la Investigacion 2020'

pygame.display.set_icon(pygame.image.load('imagenes/icono.ico'))
pygame.display.set_caption(VENTANA_TITULO)

def print_tablero_vacio():
    VENTANA.fill(TABLERO_COLOR[0])
    pinta_casill_oscuros(TABLERO_COLOR[1])

def pinta_casill(casill, casill_color):
    col = ajedrezLogica.FILAS.index(casill[0])
    fil = 7-ajedrezLogica.RANGOS.index(casill[1])
    pygame.draw.rect(VENTANA, casill_color, (CASILLERO_TAM*col,CASILLERO_TAM*fil,CASILLERO_TAM,CASILLERO_TAM), 0)

def pinta_casill_oscuros(casill_color):
    for posicion in ajedrezLogica.indiv_gen(ajedrezLogica.CASILL_OSCUROS):
        pinta_casill(ajedrezLogica.bb2str(posicion), casill_color)

def get_casill_rect(casill):
    col = ajedrezLogica.FILAS.index(casill[0])
    fil = 7-ajedrezLogica.RANGOS.index(casill[1])
    return pygame.Rect((col*CASILLERO_TAM, fil*CASILLERO_TAM), (CASILLERO_TAM,CASILLERO_TAM))

def coord2str(posicion, color=ajedrezLogica.BLANCO):
    if color == ajedrezLogica.BLANCO:
        fila_index = int(posicion[0]/CASILLERO_TAM)
        rango_index = 7 - int(posicion[1]/CASILLERO_TAM)
        return ajedrezLogica.FILAS[fila_index] + ajedrezLogica.RANGOS[rango_index]
    if color == ajedrezLogica.NEGRO:
        fila_index = 7 - int(posicion[0]/CASILLERO_TAM)
        rango_index = int(posicion[1]/CASILLERO_TAM)
        return ajedrezLogica.FILAS[fila_index] + ajedrezLogica.RANGOS[rango_index]

def print_tablero(tablero, color=ajedrezLogica.BLANCO):
    if color == ajedrezLogica.BLANCO:
        printed_tablero = tablero
    if color == ajedrezLogica.NEGRO:
        printed_tablero = ajedrezLogica.rota_tablero(tablero)

    print_tablero_vacio()

    if ajedrezLogica.jaque(tablero, ajedrezLogica.BLANCO):
        pinta_casill(ajedrezLogica.bb2str(ajedrezLogica.get_king(printed_tablero, ajedrezLogica.BLANCO)), JAQUE_ROJO)
    if ajedrezLogica.jaque(tablero, ajedrezLogica.NEGRO):
        pinta_casill(ajedrezLogica.bb2str(ajedrezLogica.get_king(printed_tablero, ajedrezLogica.NEGRO)), JAQUE_ROJO)

    for posicion in ajedrezLogica.pieza_color_gen(printed_tablero, ajedrezLogica.KING,    ajedrezLogica.NEGRO):
        VENTANA.blit(pygame.transform.scale(NEGRO_KING,    (CASILLERO_TAM,CASILLERO_TAM)), get_casill_rect(ajedrezLogica.bb2str(posicion)))
    for posicion in ajedrezLogica.pieza_color_gen(printed_tablero, ajedrezLogica.QUEEN,   ajedrezLogica.NEGRO):
        VENTANA.blit(pygame.transform.scale(NEGRO_QUEEN,   (CASILLERO_TAM,CASILLERO_TAM)), get_casill_rect(ajedrezLogica.bb2str(posicion)))
    for posicion in ajedrezLogica.pieza_color_gen(printed_tablero, ajedrezLogica.TORRE,   ajedrezLogica.NEGRO):
        VENTANA.blit(pygame.transform.scale(NEGRO_TORRE,   (CASILLERO_TAM,CASILLERO_TAM)), get_casill_rect(ajedrezLogica.bb2str(posicion)))
    for posicion in ajedrezLogica.pieza_color_gen(printed_tablero, ajedrezLogica.ALFIL,   ajedrezLogica.NEGRO):
        VENTANA.blit(pygame.transform.scale(NEGRO_ALFIL,   (CASILLERO_TAM,CASILLERO_TAM)), get_casill_rect(ajedrezLogica.bb2str(posicion)))
    for posicion in ajedrezLogica.pieza_color_gen(printed_tablero, ajedrezLogica.CABALLO, ajedrezLogica.NEGRO):
        VENTANA.blit(pygame.transform.scale(NEGRO_CABALLO, (CASILLERO_TAM,CASILLERO_TAM)), get_casill_rect(ajedrezLogica.bb2str(posicion)))
    for posicion in ajedrezLogica.pieza_color_gen(printed_tablero, ajedrezLogica.PEON,    ajedrezLogica.NEGRO):
        VENTANA.blit(pygame.transform.scale(NEGRO_PEON,    (CASILLERO_TAM,CASILLERO_TAM)), get_casill_rect(ajedrezLogica.bb2str(posicion)))

    for posicion in ajedrezLogica.pieza_color_gen(printed_tablero, ajedrezLogica.KING,    ajedrezLogica.BLANCO):
        VENTANA.blit(pygame.transform.scale(BLANCO_KING,    (CASILLERO_TAM,CASILLERO_TAM)), get_casill_rect(ajedrezLogica.bb2str(posicion)))
    for posicion in ajedrezLogica.pieza_color_gen(printed_tablero, ajedrezLogica.QUEEN,   ajedrezLogica.BLANCO):
        VENTANA.blit(pygame.transform.scale(BLANCO_QUEEN,   (CASILLERO_TAM,CASILLERO_TAM)), get_casill_rect(ajedrezLogica.bb2str(posicion)))
    for posicion in ajedrezLogica.pieza_color_gen(printed_tablero, ajedrezLogica.TORRE,   ajedrezLogica.BLANCO):
        VENTANA.blit(pygame.transform.scale(BLANCO_TORRE,   (CASILLERO_TAM,CASILLERO_TAM)), get_casill_rect(ajedrezLogica.bb2str(posicion)))
    for posicion in ajedrezLogica.pieza_color_gen(printed_tablero, ajedrezLogica.ALFIL,   ajedrezLogica.BLANCO):
        VENTANA.blit(pygame.transform.scale(BLANCO_ALFIL,   (CASILLERO_TAM,CASILLERO_TAM)), get_casill_rect(ajedrezLogica.bb2str(posicion)))
    for posicion in ajedrezLogica.pieza_color_gen(printed_tablero, ajedrezLogica.CABALLO, ajedrezLogica.BLANCO):
        VENTANA.blit(pygame.transform.scale(BLANCO_CABALLO, (CASILLERO_TAM,CASILLERO_TAM)), get_casill_rect(ajedrezLogica.bb2str(posicion)))
    for posicion in ajedrezLogica.pieza_color_gen(printed_tablero, ajedrezLogica.PEON,    ajedrezLogica.BLANCO):
        VENTANA.blit(pygame.transform.scale(BLANCO_PEON,    (CASILLERO_TAM,CASILLERO_TAM)), get_casill_rect(ajedrezLogica.bb2str(posicion)))

    pygame.display.flip()

def set_titulo(titulo):
    pygame.display.set_caption(titulo) # setea un titulo a la ventana
    pygame.display.flip() # actualiza el contenido de la ventana

def hacer_AI_movim(juega, color):
    set_titulo(VENTANA_TITULO + ' - Analizando movimiento...') # al jugar CPU añade el string a la cabecera de la ventana
    new_juega = ajedrezLogica.mueve(juega, ajedrezLogica.get_AI_movim(juega, AI_BUSCA_PROFUND))
    set_titulo(VENTANA_TITULO)
    print_tablero(new_juega.tablero, color)
    return new_juega

# identifica si el movimiento de la figura es válido y lo  realiza
def intenta_movim(juega, movim_intentado):
    for movim in ajedrezLogica.movimientos_legales(juega, juega.mueve_prim):
        if movim == movim_intentado:
            juega = ajedrezLogica.mueve(juega, movim)
    return juega


def juega_con(juega, color):
    run = True
    ongoing = True

    try:
        while run:
            RELOJ.tick(RELOJ_TICK) # inicia el conteo del reloj
            print_tablero(juega.tablero, color)

            # imprime salida de pantalla al finalizar juego y detiene su ejecucion
            if ajedrezLogica.finaliza_juego(juega):
                set_titulo(VENTANA_TITULO + ' - ' + ajedrezLogica.get_salida(juega))
                ongoing = False

            if ongoing and juega.mueve_prim == ajedrezLogica.opuesto_color(color):
                juega = hacer_AI_movim(juega, color)
            
            if ajedrezLogica.finaliza_juego(juega):
                set_titulo(VENTANA_TITULO + ' - ' + ajedrezLogica.get_salida(juega))
                ongoing = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    abandona_casillero = coord2str(event.pos, color)
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    llegada_casillero = coord2str(event.pos, color)
                    
                    if ongoing and juega.mueve_prim == color:
                        movim = (ajedrezLogica.str2bb(abandona_casillero), ajedrezLogica.str2bb(llegada_casillero))
                        juega = intenta_movim(juega, movim)
                        print_tablero(juega.tablero, color)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == 113:
                        run = False
                    if event.key == 104 and ongoing: 		# tecla H - CPU realiza movimiento
                        juega = hacer_AI_movim(juega, color)
                    if event.key == 100: 					# tecla D - Deshacer jugada
                        juega = ajedrezLogica.deshace_movim(juega)
                        juega = ajedrezLogica.deshace_movim(juega)
                        set_titulo(VENTANA_TITULO)
                        print_tablero(juega.tablero, color)
                        ongoing = True
                    if event.key == 99: 	# tecla C - Cambia Color de Tablero
                        global TABLERO_COLOR
                        new_colores = deepcopy(TABLERO_COLORES)
                        new_colores.remove(TABLERO_COLOR)
                        TABLERO_COLOR = choice(new_colores)
                        print_tablero(juega.tablero, color)
                    if event.key == 112: # tecla P - Historial de Posiciones
                        print(juega.get_mov_list() + '\n')
                        print('\n'.join(juega.posicion_historial))
                    if event.key == 101: 	# tecla E - Evalua puntaje del juego
                        print('eval = ' + str(ajedrezLogica.evalua_juego(juega)/100))

    except:
        print(format_exc(), file=stderr)
        bug_file.write('ERROR!')
        bug_file.write('----- ' + strftime('%x %X') + ' -----\n')
        bug_file.write(format_exc())
        bug_file.write('\nJugando con BLANCO:\n\t' if color == ajedrezLogica.BLANCO else '\nJuegando con NEGRO:\n\t')
        bug_file.close()

def juega_con_blancas(juega=ajedrezLogica.Juega()):
    return juega_con(juega, ajedrezLogica.BLANCO)

def juega_con_negras(juega=ajedrezLogica.Juega()):
    return juega_con(juega, ajedrezLogica.NEGRO)

def juega_con_aleatorio(juega=ajedrezLogica.Juega()):
    color = choice([ajedrezLogica.BLANCO, ajedrezLogica.NEGRO])
    juega_con(juega, color)

juega_con_aleatorio()


