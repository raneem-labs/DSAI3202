"""
Main entry point for the maze runner game with parallel explorers.
"""

import argparse
import time
from multiprocessing import Pool, cpu_count
from src.game import run_game
from src.maze import create_maze
from src.explorer import Explorer

def run_explorer(args):
    """Function to run a single explorer instance."""
    maze_type, width, height, explorer_id = args
    maze = create_maze(width, height, maze_type)
    explorer = Explorer(maze, visualize=False)
    start_time = time.time()
    time_taken, moves = explorer.solve()
    return {
        'explorer_id': explorer_id,
        'time_taken': time_taken,
        'moves': len(moves),
        'backtrack_count': explorer.backtrack_count,
        'moves_per_second': len(moves) / time_taken if time_taken > 0 else 0
    }

def compare_results(results):
    """Compare and display results from all explorers."""
    print("\n=== Exploration Results Comparison ===")
    print(f"{'Explorer':<10} {'Time (s)':<10} {'Moves':<10} {'Backtracks':<10} {'Moves/s':<10}")
    
    best_time = min(r['time_taken'] for r in results)
    best_moves = min(r['moves'] for r in results)
    best_backtracks = min(r['backtrack_count'] for r in results)
    best_speed = max(r['moves_per_second'] for r in results)
    
    for result in results:
        time_str = f"{result['time_taken']:.2f}"
        moves_str = f"{result['moves']}"
        backtracks_str = f"{result['backtrack_count']}"
        speed_str = f"{result['moves_per_second']:.2f}"
        
        # Highlight best performers
        if result['time_taken'] == best_time:
            time_str = f"\033[92m{time_str}\033[0m"
        if result['moves'] == best_moves:
            moves_str = f"\033[92m{moves_str}\033[0m"
        if result['backtrack_count'] == best_backtracks:
            backtracks_str = f"\033[92m{backtracks_str}\033[0m"
        if result['moves_per_second'] == best_speed:
            speed_str = f"\033[92m{speed_str}\033[0m"
        
        print(f"{result['explorer_id']:<10} {time_str:<10} {moves_str:<10} {backtracks_str:<10} {speed_str:<10}")
    
    print("=====================================")

def main():
    parser = argparse.ArgumentParser(description="Maze Runner Game with Parallel Explorers")
    parser.add_argument("--type", choices=["random", "static"], default="random",
                       help="Type of maze to generate (random or static)")
    parser.add_argument("--width", type=int, default=30,
                       help="Width of the maze (default: 30, ignored for static mazes)")
    parser.add_argument("--height", type=int, default=30,
                       help="Height of the maze (default: 30, ignored for static mazes)")
    parser.add_argument("--auto", action="store_true",
                       help="Run automated maze exploration")
    parser.add_argument("--visualize", action="store_true",
                       help="Visualize the automated exploration in real-time")
    parser.add_argument("--explorers", type=int, default=4,
                       help="Number of parallel explorers to run (default: 4)")
    
    args = parser.parse_args()
    
    if args.auto:
        if args.visualize and args.explorers > 1:
            print("Warning: Visualization disabled for multiple explorers")
            args.visualize = False
        
        if args.explorers == 1:
            # Single explorer mode (original behavior)
            maze = create_maze(args.width, args.height, args.type)
            explorer = Explorer(maze, visualize=args.visualize)
            time_taken, moves = explorer.solve()
            print(f"Maze solved in {time_taken:.2f} seconds")
            print(f"Number of moves: {len(moves)}")
            if args.type == "static":
                print("Note: Width and height arguments were ignored for the static maze")
        else:
            # Parallel explorers mode
            print(f"Running {args.explorers} explorers in parallel...")
            
            # Prepare arguments for each explorer
            explorer_args = [(args.type, args.width, args.height, i+1) 
                           for i in range(args.explorers)]
            
            # Create a pool of workers
            with Pool(processes=min(args.explorers, cpu_count())) as pool:
                results = pool.map(run_explorer, explorer_args)
            
            # Compare and display results
            compare_results(results)
    else:
        # Run the interactive game
        run_game(maze_type=args.type, width=args.width, height=args.height)

if __name__ == "__main__":
    main()
