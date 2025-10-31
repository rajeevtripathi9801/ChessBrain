import chess
from engine import ChessEngine
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich import box

class ChessGame:
    
    def __init__(self, engine_depth=3):
        self.board = chess.Board()
        self.engine = ChessEngine(depth=engine_depth)
        self.console = Console()
        self.move_history = []
    
    def display_board(self):
        board_str = str(self.board)
        
        pieces = {
            'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
            'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙',
            '.': '·'
        }
        
        lines = board_str.split('\n')
        display_lines = []
        
        for i, line in enumerate(lines):
            rank = 8 - i
            rank_str = f" {rank} "
            
            for char in line.split():
                rank_str += f" {pieces.get(char, char)} "
            
            display_lines.append(rank_str)
        
        display_lines.append("    a  b  c  d  e  f  g  h")
        
        board_display = '\n'.join(display_lines)
        
        turn_text = "White" if self.board.turn == chess.WHITE else "Black"
        status = f"[bold cyan]{turn_text} to move[/bold cyan]"
        
        if self.board.is_check():
            status += " [bold red]- CHECK![/bold red]"
        
        self.console.print(Panel(board_display, title="Chess Board", subtitle=status, border_style="green"))
    
    def display_move_history(self):
        if not self.move_history:
            return
        
        table = Table(title="Move History", box=box.ROUNDED)
        table.add_column("Move #", style="cyan", justify="center")
        table.add_column("White", style="white")
        table.add_column("Black", style="dim white")
        
        for i in range(0, len(self.move_history), 2):
            move_num = (i // 2) + 1
            white_move = self.move_history[i]
            black_move = self.move_history[i + 1] if i + 1 < len(self.move_history) else ""
            table.add_row(str(move_num), white_move, black_move)
        
        self.console.print(table)
    
    def display_top_moves(self, num_moves=5):
        self.console.print(f"\n[bold yellow]Analyzing position...[/bold yellow]")
        top_moves = self.engine.analyze_position(self.board, num_moves)
        
        if not top_moves:
            self.console.print("[red]No legal moves available[/red]")
            return
        
        table = Table(title=f"Top {len(top_moves)} Engine Suggestions", box=box.ROUNDED)
        table.add_column("Rank", style="cyan", justify="center")
        table.add_column("Move", style="green")
        table.add_column("Score", style="yellow", justify="right")
        table.add_column("Evaluation", style="magenta")
        
        for i, (move, score) in enumerate(top_moves, 1):
            eval_text = self._score_to_evaluation(score)
            table.add_row(
                str(i),
                self.board.san(move),
                f"{score:+d}",
                eval_text
            )
        
        self.console.print(table)
        self.console.print(f"[dim]Nodes evaluated: {self.engine.nodes_evaluated:,}[/dim]")
    
    def _score_to_evaluation(self, score):
        if score > 900:
            return "Winning"
        elif score > 300:
            return "Much better"
        elif score > 100:
            return "Better"
        elif score > -100:
            return "Equal"
        elif score > -300:
            return "Worse"
        elif score > -900:
            return "Much worse"
        else:
            return "Losing"
    
    def make_move(self, move_str):
        try:
            move = self.board.parse_san(move_str)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.move_history.append(move_str)
                return True
            else:
                self.console.print(f"[red]Illegal move: {move_str}[/red]")
                return False
        except ValueError:
            try:
                move = chess.Move.from_uci(move_str)
                if move in self.board.legal_moves:
                    move_san = self.board.san(move)
                    self.board.push(move)
                    self.move_history.append(move_san)
                    return True
                else:
                    self.console.print(f"[red]Illegal move: {move_str}[/red]")
                    return False
            except:
                self.console.print(f"[red]Invalid move format: {move_str}[/red]")
                return False
    
    def make_engine_move(self):
        self.console.print("[bold yellow]Engine is thinking...[/bold yellow]")
        best_move = self.engine.find_best_move(self.board)
        
        if best_move:
            move_san = self.board.san(best_move)
            self.board.push(best_move)
            self.move_history.append(move_san)
            
            self.console.print(f"[bold green]Engine plays: {move_san}[/bold green]")
            self.console.print(f"[dim]Evaluation: {self.engine.best_move_score:+d} | Nodes: {self.engine.nodes_evaluated:,}[/dim]")
            return True
        return False
    
    def is_game_over(self):
        return self.board.is_game_over()
    
    def get_game_result(self):
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn == chess.WHITE else "White"
            return f"Checkmate! {winner} wins!"
        elif self.board.is_stalemate():
            return "Stalemate! Game is a draw."
        elif self.board.is_insufficient_material():
            return "Draw due to insufficient material."
        elif self.board.is_fifty_moves():
            return "Draw by fifty-move rule."
        elif self.board.is_repetition():
            return "Draw by threefold repetition."
        else:
            return "Game over."
    
    def show_legal_moves(self):
        legal_moves = [self.board.san(move) for move in self.board.legal_moves]
        self.console.print(f"[cyan]Legal moves ({len(legal_moves)}):[/cyan] {', '.join(legal_moves)}")
    
    def undo_move(self):
        if len(self.board.move_stack) >= 2:
            self.board.pop()
            self.board.pop()
            self.move_history = self.move_history[:-2]
            self.console.print("[green]Undone last move[/green]")
            return True
        elif len(self.board.move_stack) == 1:
            self.board.pop()
            self.move_history = self.move_history[:-1]
            self.console.print("[green]Undone last move[/green]")
            return True
        else:
            self.console.print("[red]No moves to undo[/red]")
            return False
