import random
import numpy as np
import DataToLearn
import time
from ChessEngine import Move
from Chess.DataTree import TreeNode

valuesPiece = {
    "Q": 900,
    "K": 0,
    "R": 500,
    "B": 330,
    "N": 320,
    "P": 100,
}

boardInArrayValues = {
    "bR": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "bN": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "bB": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "bQ": [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    "bK": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    "bp": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    "wR": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    "wN": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    "wB": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    "wQ": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    "wK": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    "wp": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    "--": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # "w": [1, 0],  # next turn white
    # "g": [0, 1]  # next turn black
}
positionValuesTheory = {
    "Q": [[-2, -1, -1, 0.5, 0.5, -1, -1, -2],
          [-1, 0, 0, 0, 0, 0, 0, -1],
          [-1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1],
          [-0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
          [0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
          [-1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1],
          [-2, 0, 0.5, 0, 0, 0, 0, -1],
          [-2, -1, -1, -0.5, -0.5, -1, -1, -2]],
    "K": [[-3, -4, -4, -5, -5, -4, -4, -3],
          [-3, -4, -4, -5, -5, -4, -4, -3],
          [-3, -4, -4, -5, -5, -4, -4, -3],
          [-3, -4, -4, -5, -5, -4, -4, -3],
          [-2, -3, -3, -4, -4, -3, -2, -2],
          [-1, -2, -2, -2, -2, -2, -2, -1],
          [2, 2, 0, 0, 0, 0, 2, 2],
          [2, 3, 1, 0, 0, 1, 3, 2]],
    "R": [[0, 0, 0, 0, 0, 0, 0, 0],
          [0.5, 1, 1, 1, 1, 1, 1, 0.5],
          [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
          [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
          [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
          [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
          [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
          [0, -0.5, 0, 0.5, 0.5, 0, -0.5, 0]],
    "B": [[-2, -1, -1, -1, -1, -1, -1, -2],
          [-1, 0.5, 0, 0, 0, 0, 0.5, -1],
          [-1, 0, 0.5, 1, 1, 0.5, 0, -1],
          [-1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1],
          [-1, 0, 1, 1, 1, 1, 0, 0],
          [-1, 1, 1, 1, 1, 1, 1, -1],
          [-1, 0.5, 0, 0, 0, 0, 0.5, -1],
          [-2, -1, -1, -1, -1, -1, -1, -2]],
    "N": [[-5, -4, -3, -3, -3, -3, -4, -5],
          [-4, -2, 0, 0, 0, 0, -2, -4],
          [-3, 0, 1, 1.5, 1.5, 1, 0, -3],
          [-3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3],
          [-3, 0, 1.5, 2, 2, 1.5, 0, -3],
          [-3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3],
          [-4, -2, 0, 0.5, 0.5, 0, -2, -4],
          [-5, -4, -3, -3, -3, -3, -4, -5]],
    "P": [[0, 0, 0, 0, 0, 0, 0, 0],
          [5, 5, 5, 5, 5, 5, 5, 5],
          [1, 1, 2, 3, 3, 2, 1, 1],
          [0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],
          [0, 0, 0, 3, 3, 0, 0, 0],
          [0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],
          [0.5, 1, 1, -2, -2, 1, 1, 0.5],
          [0, 0, 0, 0, 0, 0, 0, 0]],
    "q": [[-2, -1, -1, -0.5, -0.5, -1, -1, -2],
          [-1, 0, 0, 0, 0, 0.5, 0, -1],
          [-1, 0, 0.5, 0.5, 0.5, 0.5, 0.5, -1],
          [-0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
          [-0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, 0],
          [-1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1],
          [-1, 0, 0, 0, 0, 0, 0, -1],
          [-2, -1, -1, -0.5, -0.5, -1, -1, -2]],
    "k": [[2, 3, 1, 0, 0, 1, 3, 2],
          [2, 2, 0, 0, 0, 0, 2, 2],
          [-1, -2, -2, -2, -2, -2, -2, -1],
          [-2, -3, -3, -4, -4, -3, -2, -2],
          [-3, -4, -4, -5, -5, -4, -4, -3],
          [-3, -4, -4, -5, -5, -4, -4, -3],
          [-3, -4, -4, -5, -5, -4, -4, -3],
          [-3, -4, -4, -5, -5, -4, -4, -3]],
    "r": [[0, -0.5, 0, 0.5, 0.5, 0, -0.5, 0],
          [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
          [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
          [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
          [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
          [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
          [0.5, 1, 1, 1, 1, 1, 1, 0.5],
          [0, 0, 0, 0, 0, 0, 0, 0]],
    "b": [[-2, -1, -1, -1, -1, -1, -1, -2],
          [-1, 0.5, 0, 0, 0, 0, 0.5, -1],
          [-3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3],
          [-1, 0, 1, 1, 1, 1, 0, 0],
          [-1, 0, 0.5, 1, 1, 0.5, 0, -1],
          [-1, 0, 0.5, 1, 1, 0.5, 0, -1],
          [-1, 0, 0, 0, 0, 0, 0, -1],
          [-2, -1, -1, -1, -1, -1, -1, -2]],
    "n": [[-5, -4, -3, -3, -3, -3, -4, -5],
          [-4, -2, 0, 0.5, 0.5, 0, -2, -4],
          [-3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3],
          [-3, 0, 1.5, 2, 2, 1.5, 0, -3],
          [-3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3],
          [-3, 0, 1, 1.5, 1.5, 1, 0, -3],
          [-4, -2, 0, 0, 0, 0, -2, -4],
          [-5, -3, -3, -3, -3, -3, -3, -5]],
    "p": [[0, 0, 0, 0, 0, 0, 0, 0],
          [0.5, 1, 1, -2, -2, 1, 1, 0.5],
          [0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],
          [0, 0, 0, 3, 3, 0, 0, 0],
          [0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],
          [1, 1, 2, 3, 3, 2, 1, 1],
          [5, 5, 5, 5, 5, 5, 5, 5],
          [0, 0, 0, 0, 0, 0, 0, 0]],
}

CHECKMATE = 100000
STALEMATE = 0
DEPTH = 3


def findRandomMove(validMoves):
    if len(validMoves) != 0:
        return validMoves[random.randint(0, len(validMoves) - 1)]
    else:
        pass


def findBestMove(gs, validMoves):
    turnMutliplayer = 1 if gs.whiteToMove else -1  # black or white
    opponentsMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()

        if gs.staleMate:
            opponentsMaxScore = STALEMATE
        elif gs.checkMate:
            opponentsMaxScore = - CHECKMATE
        else:
            opponentsMaxScore = -CHECKMATE
            for opponentsMove in opponentsMoves:
                gs.makeMove(opponentsMove)
                # gs.getValidMoves() # Needed?
                if gs.checkMate:
                    score = CHECKMATE
                elif gs.staleMate:
                    score = 0
                else:
                    score = evluatePositions(gs.board) * -turnMutliplayer
                    score = score + scoreBorad(gs) * -turnMutliplayer
                if score > opponentsMaxScore:
                    opponentsMaxScore = score
                gs.undoMove()
        if opponentsMaxScore < opponentsMinMaxScore:
            opponentsMinMaxScore = opponentsMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove


# Helper method to make the first recursive call
def findBestMoveMinMax(gs, validMoves, current_node):
    global nextMove
    nextMove = None
    if float(current_node.plays) > 4:
        print("now!")
        list_child = []
        if len(current_node.children) < 1:
            addToTree(gs, current_node)
        children = current_node.children
        multi = 1 if gs.whiteToMove else -1
        for child in children:
            list_child.append((float(child.wins) / float(child.plays)) if float(child.plays) != 0 else -10 * multi)
        # Just when more then halt of the games are won with this state otherwise a new move
        if max(list_child) < 0.5 and gs.whiteToMove:
            nextMove = gs.getValidMoves()[list_child.index(-10 * multi)]
        elif not gs.whiteToMove and min(list_child) > 0.5:
            nextMove = gs.getValidMoves()[list_child.index(-10 * multi)]
        else:
            if gs.whiteToMove:
                nextMove = gs.getValidMoves()[list_child.index(max(list_child))]
            else:
                nextMove = gs.getValidMoves()[list_child.index(min(list_child))]
    else:
        timerrrr = time.time()
        findMoveMinMax(gs, validMoves, DEPTH, -1000, 1000, gs.whiteToMove, current_node)
        print("Recur: ", time.time() - timerrrr)
    return nextMove


def findMoveMinMax(gs, validMoves, depth, alpha, beta, whiteToMove, current_node):
    global nextMove
    if depth == 0:
        timerrrrrrrrrr = time.time()
        return (float(current_node.importedEvaluation) * 3 + float(current_node.evaluation) * 2 + ((float(current_node.wins) / float(current_node.plays)) if float(current_node.plays) != 0 else 0) * 100)
        print("ONE EVE CHECK : ", time.time() - timerrrrrrrrrr)
    if len(current_node.children) < 1:
        timerrrrrrr = time.time()
        addToTree(gs, current_node)
        print("ONE ADD : ", time.time() - timerrrrrrr)
    if whiteToMove:
        maxScore = - CHECKMATE
        for i in range(len(validMoves)):
            gs.makeMove(validMoves[i])
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, alpha, beta, False, current_node.children[i])
            gs.undoMove()
            if score > maxScore:
                maxScore = score
                if alpha < score:
                    alpha = score
                if depth == DEPTH:
                    nextMove = validMoves[i]
                if beta <= alpha:
                    break
        return maxScore
    else:
        minScore = CHECKMATE
        for i in range(len(validMoves)):
            gs.makeMove(validMoves[i])
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, alpha, beta, True, current_node.children[i])
            gs.undoMove()
            if score < minScore:
                minScore = score
                if beta > score:
                    beta = score
                if depth == DEPTH:
                    nextMove = validMoves[i]
                if beta <= alpha:
                    break
        return minScore


# Positive score is good for white, a negative score is good for black
def scoreBorad(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif gs.staleMate:
        return 0
    score = 0
    for row in gs.board:
        for square in row:
            if square.isupper():
                score += valuesPiece[square]
            elif square.islower():
                score -= valuesPiece[square.upper()]
    return score


# Positive score is good for white and a negative score bad for white
def evaluate_attacks(gs):
    multiplicator = 1 if gs.whiteToMove else -1
    gs.whiteToMove = not gs.whiteToMove
    valid_moves = gs.getValidMoves()
    gs.whiteToMove = not gs.whiteToMove
    valid_moves_opp = gs.getValidMoves()
    score_attack = 0
    for move in valid_moves:
        if move.pieceCaptured != '--':
            score_attack = score_attack + valuesPiece[move.pieceCaptured.upper()]/300
    # number of moves
    number_of_moves = (len(valid_moves_opp) - len(valid_moves)) * multiplicator
    king_moves = 0
    check_check = 0
    # check
    if gs.inCheck():
        check_check = -5 * multiplicator
        # if check every move which king cant go is good
        if gs.whiteToMove:
            for move in valid_moves_opp:
                if move.pieceMoved == "K":
                    king_moves += 1
        else:
            for move in valid_moves_opp:
                if move.pieceMoved == "k":
                    king_moves += 1
    else:
        king_moves = 8

    return float(number_of_moves) + float(score_attack) / 5 + check_check + (64 - king_moves * king_moves)


def evluatePositions(board):
    scorePositions = 0
    pieces = {"P", "K", "Q", "B", "R", "N", "p", "k", "q", "b", "r", "n"}
    for piece in pieces:
        if piece.isupper():
            scorePositions += vertorMulti(refeactorBoardInArray(board, piece), positionValuesTheory[piece])
        elif piece.islower():
            scorePositions -= vertorMulti(refeactorBoardInArray(board, piece), positionValuesTheory[piece])
    return scorePositions


def refeactorBoardInArray(board, figure):
    boardNew = np.empty([8, 8])
    rowNumb = 0
    for row in board:
        squareNumb = 0
        for square in row:
            if square == figure:
                boardNew[rowNumb][squareNumb] = 1.0
            else:
                boardNew[rowNumb][squareNumb] = 0.0
            squareNumb = squareNumb + 1
        rowNumb = rowNumb + 1
    return boardNew


def vertorMulti(matOne, matTwo):
    sum = 0
    for i in range(len(matOne)):
        sum += np.sum(matOne[i] * matTwo[i])
    return sum


def addToTree(gs, current_node):
    for move in gs.getValidMoves():
        gs.makeMove(move)
        current_node.add_child(
            TreeNode([DataToLearn.createFEN(gs), 0, scoreBorad(gs) + evluatePositions(gs.board) + evaluate_attacks(gs), 0, 0], move.getChessNotation()))
        gs.undoMove()
