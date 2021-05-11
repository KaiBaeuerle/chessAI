import pygame as p
from Chess import ChessEngine, SmartMoveFinder, DataToLearn, VisualizData
import time
import xml.etree.ElementTree as gfg
import os.path
from Chess.DataTree import TreeNode


WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
WHITE_PIECE_CAPTUED = []
BLACK_PIECE_CAPTUED = []
BLACK_EVALUATION = 0.5  # Win percentage at start
test = p.Rect(200 + HEIGHT * (1 - BLACK_EVALUATION), HEIGHT + 20 + 60,
              WIDTH * BLACK_EVALUATION, 50)  # Show win percentage


# Here we load the image ones
def loadImages():
    pieces = ['P', 'R', 'N', 'B', 'K', 'Q', 'p', 'r', 'n', 'b', 'k', 'q']
    pics_name = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'p', 'r', 'n', 'b', 'k', 'q']
    for i in range(len(pieces)):
        IMAGES[pieces[i]] = p.transform.scale(p.image.load("allData/images/" + pics_name[i] + ".png"),
                                              (SQ_SIZE, SQ_SIZE))


def main():
    global MOVE_TIME_START
    global TREE
    global CURRENT_NODE
    p.init()
    # loading the history
    if os.stat('Tree_history_next.xml').st_size == 0:
        start = "<Level-0><State><FEN>rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR</FEN><ImportedEvaluation>0</ImportedEvaluation><Evaluation>0</Evaluation><Wins>0</Wins><Plays>0</Plays><Move /></State></Level-0>"
        fileer = open("Tree_history_next.xml", "wb")
        fileer.write(start)
        fileer.close()

    MOVE_TIME_START = time.time()
    tree = gfg.parse('Tree_history_next.xml').getroot()
    TREE = TreeNode([tree.getchildren()[0].getchildren()[0].text, tree.getchildren()[0].getchildren()[1].text,
                     tree.getchildren()[0].getchildren()[2].text, tree.getchildren()[0].getchildren()[3].text,
                     tree.getchildren()[0].getchildren()[4].text], "")
    if len(tree.getchildren()[0].getchildren()) > 6:
        TREE.read_tree(tree.getchildren()[0].getchildren()[6])
    print("Time to load: ", time.time() - MOVE_TIME_START)
    CURRENT_NODE = TREE
    VisualizData.visualize_data_print(CURRENT_NODE)
    loadImages()
    moveSound = p.mixer.Sound('allData/sound/moveSound.wav')
    conquerePieceSound = p.mixer.Sound('allData/sound/conquerePieceSound.mp3')
    screen = p.display.set_mode((WIDTH + 400, HEIGHT + 80 + 60))
    p.display.set_caption("K(ing) AI")
    clock = p.time.Clock()
    screen.fill(p.Color("beige"))
    gs = ChessEngine.GameState()
    gs.moveLogLong.append(CURRENT_NODE)
    first_move = True
    validMoves = gs.getValidMoves()
    moveMade = False  # flag variable for a valid move
    animate = False  # flag whether eh should animate
    running = True
    sqSelected = ()  # keep track of the last click of the user tuple (row,col)
    playerClicks = []  # keeps track of player clicks (two tuples: [(row,col),(row,col)]
    gameOver = False
    playerOne = False  # If human is playing white = true
    playerTwo = False  # If human is playing black = true

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # Mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()  # (x,y) of mouse
                    col = (location[0] - 200) // SQ_SIZE
                    row = (location[1] - 10 - 60) // SQ_SIZE
                    if location[0] > 200 and location[0] < WIDTH + 200 and location[1] > 10 + 60 and location[
                        1] < HEIGHT + 10 + 60:
                        if sqSelected == (row, col):  # check whether the user clicked the square twice
                            sqSelected = ()  # deselect
                            playerClicks = []  # clear player clicks
                        else:
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected)
                        if len(playerClicks) == 2:
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)

                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    if len(CURRENT_NODE.children) < 1:
                                        timer = time.time()
                                        SmartMoveFinder.addToTree(gs, CURRENT_NODE)
                                        print("time to add: ", time.time() - timer)
                                    gs.makeMove(validMoves[i])
                                    CURRENT_NODE = changeCurrentNode(gs)
                                    gs.moveLogLong.append(CURRENT_NODE)
                                    moveMade = True
                                    animate = True
                                    first_move = False
                                    print("Player-time: ", time.time() - MOVE_TIME_START)
                                    MOVE_TIME_START = time.time()
                                    if move.pieceCaptured != "--":
                                        conquerePieceSound.play()
                                    else:
                                        moveSound.play()
                                    # recalculate the win percentage
                                    BLACK_EVALUATION = 0.5 - float(CURRENT_NODE.evaluation) / 1000
                                    if BLACK_EVALUATION > 0.99:
                                        BLACK_EVALUATION = 0.99
                                    test.update(200 + HEIGHT * (1 - BLACK_EVALUATION), HEIGHT + 20 + 60,
                                                WIDTH * BLACK_EVALUATION, 50)
                                    sqSelected = ()
                                    playerClicks = []
                            if not moveMade:
                                playerClicks = [sqSelected]


            # key handers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo if "z" is pressed
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == p.K_r:  # reset the board when pressing "r"
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
                if e.key == p.K_1:  # save data
                    MOVE_TIME_START = time.time()
                    TREE.save_tree("Tree_history_next.xml")
                    print("Time to save: ", time.time() - MOVE_TIME_START)
                if e.key == p.K_2:
                    MOVE_TIME_START = time.time()
                    # updatePlayAndWins(gs) # save?
                    gs.checkMate = True
                    gameOver = True
                    print("Time to update the data: ", time.time() - MOVE_TIME_START)
                if e.key == p.K_3:
                    gs.staleMate = True
                    gameOver = True
                # white lost (from surrender)
                if e.key == p.K_4:
                    if gs.whiteToMove:
                        gs.checkMate = True
                        gameOver = True
                else:
                    gs.whiteToMove = True
                    gs.checkMate = True
                    gameOver = True
                # black lost (from surrender)
                if e.key == p.K_5:
                    if not gs.whiteToMove:
                        gs.checkMate = True
                        gameOver = True
                else:
                    gs.whiteToMove = False
                    gs.checkMate = True
                    gameOver = True

        # AI Movefinder
        if not gameOver and not humanTurn:
            if len(CURRENT_NODE.children) < 1:
                timer = time.time()
                SmartMoveFinder.addToTree(gs, CURRENT_NODE)
                print("time to add: ", time.time() - timer)
            timerrr = time.time()
            AImove = SmartMoveFinder.findBestMoveMinMax(gs, validMoves, CURRENT_NODE)
            print("find new Move: ", time.time() - timerrr)
            if AImove is None:
                AImove = SmartMoveFinder.findRandomMove(validMoves)
            gs.makeMove(AImove)
            moveMade = True
            animate = True
            CURRENT_NODE = changeCurrentNode(gs)
            gs.moveLogLong.append(CURRENT_NODE)
            print("AI: ", time.time() - MOVE_TIME_START)
            MOVE_TIME_START = time.time()
            if AImove.pieceCaptured != "--":
                conquerePieceSound.play()
            else:
                moveSound.play()
            # recalculate the win percentage
            BLACK_EVALUATION = 0.5 - float(CURRENT_NODE.evaluation) / 1000
            if BLACK_EVALUATION > 0.99:
                BLACK_EVALUATION = 0.99
            test.update(200 + HEIGHT * (1 - BLACK_EVALUATION), HEIGHT + 20 + 60,
                        WIDTH * BLACK_EVALUATION, 50)

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected)
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                font1 = p.font.SysFont('Black wins by checkmate', 64)
                img1 = font1.render('Black wins by checkmate', True, "dark red")
                screen.blit(img1, (210, 280))
            else:
                font1 = p.font.SysFont('White wins by checkmate', 64)
                img1 = font1.render('White wins by checkmate', True, "dark red")
                screen.blit(img1, (210, 280))
                # drawText(screen, 'White wins by checkmate')
            updatePlayAndWins(gs)
            MOVE_TIME_START = time.time()
            TREE.save_tree("Tree_history_next.xml")
            print("Time to save: ", time.time() - MOVE_TIME_START)
            running = False
            time.sleep(60)
        elif gs.staleMate:
            font1 = p.font.SysFont('Stalemate', 64)
            img1 = font1.render('Stalemate', True, "dark red")
            screen.blit(img1, (210, 280))
            updatePlayAndWins(gs)
            MOVE_TIME_START = time.time()
            TREE.save_tree("Tree_history_next.xml")
            print("Time to save: ", time.time() - MOVE_TIME_START)
            running = False
            time.sleep(60)
        clock.tick(MAX_FPS)
        p.display.flip()


# Higlicght the square selected
def highlightSqaures(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if (gs.board[r][c].islower() and not gs.whiteToMove) or (not gs.board[r][c].islower() and gs.whiteToMove):
            # if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):  # sqSelected a piece that can be moved
            # highlight selected squares
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparancy value
            s.fill(p.Color('blue'))
            screen.blit(s, ((c * SQ_SIZE) + 200, (r * SQ_SIZE) + 10 + 60))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, ((SQ_SIZE * move.endCol) + 200, (move.endRow * SQ_SIZE) + 10 + 60))


def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)  # draw squares on the board
    highlightSqaures(screen, gs, validMoves, sqSelected)
    highlightLastMove(gs, screen)
    drawPieces(screen, gs.board)  # draw pieces on the top of those squares


def drawBoard(screen):
    global colors
    p.draw.rect(screen, "black", p.Rect(194, 64, HEIGHT + 12, WIDTH + 12))
    p.draw.rect(screen, "white", p.Rect(200 + WIDTH / 4, 10, WIDTH / 4, 40))
    p.draw.rect(screen, "grey", p.Rect(200 + WIDTH / 2, 10, WIDTH / 4, 40))
    p.draw.rect(screen, "white", p.Rect(200, HEIGHT + 20 + 60, WIDTH, 50))
    p.draw.rect(screen, "grey", test)

    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE + 200, r * SQ_SIZE + 10 + 60, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE + 200, r * SQ_SIZE + 10 + 60, SQ_SIZE, SQ_SIZE))


def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 4  # frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending sqaure
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect((move.endCol * SQ_SIZE) + 200, (move.endRow * SQ_SIZE) + 10 + 60, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect((c * SQ_SIZE) + 200, (r * SQ_SIZE) + 10 + 60, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)
    if move.pieceCaptured.isupper():
        screen.blit(IMAGES[move.pieceCaptured],
                    p.Rect(((len(WHITE_PIECE_CAPTUED) % 3)) * SQ_SIZE,
                           (len(WHITE_PIECE_CAPTUED) // 3) * SQ_SIZE + 10 + 60, SQ_SIZE, SQ_SIZE))
        WHITE_PIECE_CAPTUED.append(move.pieceCaptured)
    elif move.pieceCaptured.islower():
        screen.blit(IMAGES[move.pieceCaptured],
                    p.Rect(((len(BLACK_PIECE_CAPTUED) % 3)) * SQ_SIZE + WIDTH + 210,
                           (len(BLACK_PIECE_CAPTUED) // 3) * SQ_SIZE + 10 + 60, SQ_SIZE, SQ_SIZE))
        BLACK_PIECE_CAPTUED.append(move.pieceCaptured)


# highlight last move made
def highlightLastMove(gs, screen):
    if len(gs.moveLog) > 0:
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)  # transparancy value
        s.fill(p.Color('red'))
        screen.blit(s, ((gs.moveLog[-1].startCol * SQ_SIZE) + 200, (gs.moveLog[-1].startRow * SQ_SIZE) + 10 + 60))
        screen.blit(s, ((gs.moveLog[-1].endCol * SQ_SIZE) + 200, (gs.moveLog[-1].endRow * SQ_SIZE) + 10 + 60))


def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObject.get_width() / 2,
                                                    HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))


# change the current Node
def changeCurrentNode(gs):
    fen_now = DataToLearn.createFEN(gs)
    for states in CURRENT_NODE.children:
        if states.fEN == fen_now:
            return states


def updatePlayAndWins(gs):
    print (len(gs.moveLogLong))
    gs.checkMate = True
    TREE.plays = 1 + int(TREE.plays)
    if gs.checkMate and not gs.whiteToMove:
        TREE.wins = int(TREE.wins) + 1
    helperUpdatePlayAndWins(gs, TREE, level=1)

def helperUpdatePlayAndWins(gs, current_node, level):
    print(level)
    for state in current_node.children:
        if state == gs.moveLogLong[level]:
            state.plays = float(state.plays) + 1
            current_node = state
            if gs.checkMate and not gs.whiteToMove:
                state.wins = float(state.wins) + 1
            elif gs.staleMate:
                state.wins = float(state.wins) + 0.5
            if len(gs.moveLogLong) - 1 > level:
                helperUpdatePlayAndWins(gs, current_node, level + 1)


if __name__ == "__main__":
    main()

# todo: Add more evaluations (pieces covered)
# todo: try to get evaluation from the imported data
# todo: Add Player Specific Bot
# todo: make heurustic: which is the first move to watch (makes it faster)
