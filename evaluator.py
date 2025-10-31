import chess

class PositionEvaluator:
    
    PIECE_VALUES = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }
    
    PAWN_TABLE = [
        0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5,  5, 10, 25, 25, 10,  5,  5,
        0,  0,  0, 20, 20,  0,  0,  0,
        5, -5,-10,  0,  0,-10, -5,  5,
        5, 10, 10,-20,-20, 10, 10,  5,
        0,  0,  0,  0,  0,  0,  0,  0
    ]
    
    KNIGHT_TABLE = [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50,
    ]
    
    BISHOP_TABLE = [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -20,-10,-10,-10,-10,-10,-10,-20,
    ]
    
    ROOK_TABLE = [
        0,  0,  0,  0,  0,  0,  0,  0,
        5, 10, 10, 10, 10, 10, 10,  5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        0,  0,  0,  5,  5,  0,  0,  0
    ]
    
    QUEEN_TABLE = [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
        -5,  0,  5,  5,  5,  5,  0, -5,
        0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20
    ]
    
    KING_MIDDLE_TABLE = [
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -10,-20,-20,-20,-20,-20,-20,-10,
        20, 20,  0,  0,  0,  0, 20, 20,
        20, 30, 10,  0,  0, 10, 30, 20
    ]
    
    KING_END_TABLE = [
        -50,-40,-30,-20,-20,-30,-40,-50,
        -30,-20,-10,  0,  0,-10,-20,-30,
        -30,-10, 20, 30, 30, 20,-10,-30,
        -30,-10, 30, 40, 40, 30,-10,-30,
        -30,-10, 30, 40, 40, 30,-10,-30,
        -30,-10, 20, 30, 30, 20,-10,-30,
        -30,-30,  0,  0,  0,  0,-30,-30,
        -50,-30,-30,-30,-30,-30,-30,-50
    ]
    
    def __init__(self):
        self.position_tables = {
            chess.PAWN: self.PAWN_TABLE,
            chess.KNIGHT: self.KNIGHT_TABLE,
            chess.BISHOP: self.BISHOP_TABLE,
            chess.ROOK: self.ROOK_TABLE,
            chess.QUEEN: self.QUEEN_TABLE,
            chess.KING: self.KING_MIDDLE_TABLE
        }
    
    def evaluate_position(self, board):
        if board.is_checkmate():
            return -20000 if board.turn else 20000
        
        if board.is_stalemate() or board.is_insufficient_material():
            return 0
        
        score = 0
        
        score += self._evaluate_material(board)
        score += self._evaluate_piece_positioning(board)
        score += self._evaluate_mobility(board)
        score += self._evaluate_pawn_structure(board)
        score += self._evaluate_king_safety(board)
        
        return score
    
    def _evaluate_material(self, board):
        score = 0
        for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            score += len(board.pieces(piece_type, chess.WHITE)) * self.PIECE_VALUES[piece_type]
            score -= len(board.pieces(piece_type, chess.BLACK)) * self.PIECE_VALUES[piece_type]
        return score
    
    def _evaluate_piece_positioning(self, board):
        score = 0
        is_endgame = self._is_endgame(board)
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is None:
                continue
            
            piece_type = piece.piece_type
            color = piece.color
            
            if piece_type == chess.KING:
                table = self.KING_END_TABLE if is_endgame else self.KING_MIDDLE_TABLE
            else:
                table = self.position_tables.get(piece_type, [0] * 64)
            
            table_square = square if color == chess.WHITE else chess.square_mirror(square)
            position_value = table[table_square]
            
            if color == chess.WHITE:
                score += position_value
            else:
                score -= position_value
        
        return score
    
    def _evaluate_mobility(self, board):
        original_turn = board.turn
        
        board.turn = chess.WHITE
        white_mobility = board.legal_moves.count()
        
        board.turn = chess.BLACK
        black_mobility = board.legal_moves.count()
        
        board.turn = original_turn
        
        return (white_mobility - black_mobility) * 10
    
    def _evaluate_pawn_structure(self, board):
        score = 0
        
        white_pawns = board.pieces(chess.PAWN, chess.WHITE)
        black_pawns = board.pieces(chess.PAWN, chess.BLACK)
        
        for file in range(8):
            white_file_pawns = sum(1 for sq in white_pawns if chess.square_file(sq) == file)
            black_file_pawns = sum(1 for sq in black_pawns if chess.square_file(sq) == file)
            
            if white_file_pawns > 1:
                score -= 10 * (white_file_pawns - 1)
            if black_file_pawns > 1:
                score += 10 * (black_file_pawns - 1)
        
        for pawn_square in white_pawns:
            file = chess.square_file(pawn_square)
            if file > 0:
                if not any(chess.square_file(sq) == file - 1 for sq in white_pawns):
                    if file < 7:
                        if not any(chess.square_file(sq) == file + 1 for sq in white_pawns):
                            score -= 15
        
        for pawn_square in black_pawns:
            file = chess.square_file(pawn_square)
            if file > 0:
                if not any(chess.square_file(sq) == file - 1 for sq in black_pawns):
                    if file < 7:
                        if not any(chess.square_file(sq) == file + 1 for sq in black_pawns):
                            score += 15
        
        return score
    
    def _evaluate_king_safety(self, board):
        score = 0
        
        white_king_sq = board.king(chess.WHITE)
        black_king_sq = board.king(chess.BLACK)
        
        if white_king_sq:
            white_king_file = chess.square_file(white_king_sq)
            if white_king_file < 3 or white_king_file > 4:
                score += 20
        
        if black_king_sq:
            black_king_file = chess.square_file(black_king_sq)
            if black_king_file < 3 or black_king_file > 4:
                score -= 20
        
        return score
    
    def _is_endgame(self, board):
        queens = len(board.pieces(chess.QUEEN, chess.WHITE)) + len(board.pieces(chess.QUEEN, chess.BLACK))
        minor_pieces = (len(board.pieces(chess.KNIGHT, chess.WHITE)) + 
                       len(board.pieces(chess.BISHOP, chess.WHITE)) +
                       len(board.pieces(chess.KNIGHT, chess.BLACK)) + 
                       len(board.pieces(chess.BISHOP, chess.BLACK)))
        
        return queens == 0 or (queens == 2 and minor_pieces <= 2)
