#!/usr/bin/env python3

from game import ChessGame
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
import sys

def main():
    console = Console()
    
    console.print(Panel.fit(
        "[bold cyan]Chess Engine with Minimax & Alpha-Beta Pruning[/bold cyan]\n"
        "[dim]Developed in Python with Advanced Heuristics[/dim]",
        border_style="blue"
    ))
    
    console.print("\n[yellow]Welcome to the Chess Engine![/yellow]\n")
    
    while True:
        try:
            depth_input = Prompt.ask(
                "[cyan]Select engine difficulty (search depth)[/cyan]",
                choices=["1", "2", "3", "4", "5"],
                default="3"
            )
            depth = int(depth_input)
            break
        except ValueError:
            console.print("[red]Please enter a valid number[/red]")
    
    game = ChessGame(engine_depth=depth)
    
    console.print("\n[bold green]Game started![/bold green]")
    console.print("[dim]Commands: 'move e4', 'suggest', 'legal', 'undo', 'history', 'quit'[/dim]\n")
    
    while not game.is_game_over():
        game.display_board()
        
        if game.board.turn == chess.WHITE:
            console.print("\n[bold]Your turn (White)[/bold]")
            
            while True:
                command = Prompt.ask("[cyan]Enter command[/cyan]").strip().lower()
                
                if command == 'quit' or command == 'exit':
                    if Confirm.ask("[yellow]Are you sure you want to quit?[/yellow]"):
                        console.print("[bold]Thanks for playing![/bold]")
                        sys.exit(0)
                    continue
                
                elif command == 'suggest' or command == 'analysis' or command == 'analyze':
                    game.display_top_moves(5)
                    continue
                
                elif command == 'legal' or command == 'moves':
                    game.show_legal_moves()
                    continue
                
                elif command == 'undo' or command == 'back':
                    game.undo_move()
                    break
                
                elif command == 'history' or command == 'moves-history':
                    game.display_move_history()
                    continue
                
                elif command == 'help':
                    console.print("\n[bold cyan]Available Commands:[/bold cyan]")
                    console.print("  [green]<move>[/green]     - Make a move (e.g., 'e4', 'Nf3', 'e2e4')")
                    console.print("  [green]suggest[/green]    - Show top engine move suggestions")
                    console.print("  [green]legal[/green]      - Show all legal moves")
                    console.print("  [green]undo[/green]       - Undo last move")
                    console.print("  [green]history[/green]    - Show move history")
                    console.print("  [green]quit[/green]       - Exit the game\n")
                    continue
                
                elif command:
                    if game.make_move(command):
                        break
                    else:
                        console.print("[yellow]Try again or type 'help' for commands[/yellow]")
                else:
                    console.print("[red]Please enter a command[/red]")
        
        else:
            console.print("\n[bold]Engine's turn (Black)[/bold]")
            game.make_engine_move()
    
    console.print("\n")
    game.display_board()
    game.display_move_history()
    
    result = game.get_game_result()
    console.print(Panel.fit(
        f"[bold yellow]{result}[/bold yellow]",
        border_style="yellow"
    ))

if __name__ == "__main__":
    try:
        import chess
        main()
    except KeyboardInterrupt:
        console = Console()
        console.print("\n[bold yellow]Game interrupted. Thanks for playing![/bold yellow]")
        sys.exit(0)
    except Exception as e:
        console = Console()
        console.print(f"[bold red]An error occurred: {e}[/bold red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)
