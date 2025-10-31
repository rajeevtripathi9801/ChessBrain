import chess
from evaluator import PositionEvaluator

class ChessEngine:
    
    def __init__(self, depth=3):
        self.depth = depth
        self.evaluator = PositionEvaluator()
        self.nodes_evaluated = 0
        self.best_move_score = 0
    
    def find_best_move(self, board, depth=None):
        if depth is None:
            depth = self.depth
        
        self.nodes_evaluated = 0
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        legal_moves = list(board.legal_moves)
        legal_moves = self._order_moves(board, legal_moves)
        
        color_multiplier = 1 if board.turn == chess.WHITE else -1
        
        for move in legal_moves:
            board.push(move)
            score = -self._negamax(board, depth - 1, -beta, -alpha)
            board.pop()
            
            if score > best_score:
                best_score = score
                best_move = move
            
            alpha = max(alpha, score)
        
        self.best_move_score = best_score * color_multiplier
        return best_move
    
    def _negamax(self, board, depth, alpha, beta):
        self.nodes_evaluated += 1
        
        if depth == 0 or board.is_game_over():
            eval_score = self.evaluator.evaluate_position(board)
            color_multiplier = 1 if board.turn == chess.WHITE else -1
            return eval_score * color_multiplier
        
        legal_moves = list(board.legal_moves)
        legal_moves = self._order_moves(board, legal_moves)
        
        max_score = float('-inf')
        for move in legal_moves:
            board.push(move)
            score = -self._negamax(board, depth - 1, -beta, -alpha)
            board.pop()
            
            max_score = max(max_score, score)
            alpha = max(alpha, score)
            
            if beta <= alpha:
                break
        
        return max_score
    
    def _order_moves(self, board, moves):
        def move_priority(move):
            score = 0
            
            if board.is_capture(move):
                captured_piece = board.piece_at(move.to_square)
                moving_piece = board.piece_at(move.from_square)
                if captured_piece and moving_piece:
                    score += 10 * self.evaluator.PIECE_VALUES[captured_piece.piece_type]
                    score -= self.evaluator.PIECE_VALUES[moving_piece.piece_type]
            
            if move.promotion:
                score += self.evaluator.PIECE_VALUES[move.promotion]
            
            board.push(move)
            if board.is_check():
                score += 50
            board.pop()
            
            return score
        
        return sorted(moves, key=move_priority, reverse=True)
    
    def analyze_position(self, board, num_top_moves=5):
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return []
        
        move_scores = []
        color_multiplier = 1 if board.turn == chess.WHITE else -1
        
        for move in legal_moves:
            board.push(move)
            score = -self._negamax(board, self.depth - 1, float('-inf'), float('inf'))
            board.pop()
            move_scores.append((move, score * color_multiplier))
        
        move_scores.sort(key=lambda x: x[1], reverse=True)
        
        return move_scores[:num_top_moves]
    
    def get_move_evaluation(self, board, move):
        board.push(move)
        score = self.evaluator.evaluate_position(board)
        board.pop()
        return score
