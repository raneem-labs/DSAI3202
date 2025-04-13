"""
Enhanced visualization utilities for the maze game including performance comparisons.
"""

import pygame
import time
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
from collections import defaultdict
from .constants import WINDOW_SIZE, CELL_SIZE, WHITE, BLACK, RED, GREEN, BLUE, YELLOW, CYAN
from .explorer import Explorer

def visualize_maze(maze, screen):
    """
    Visualize a maze on the given screen.
    
    Args:
        maze: The maze to visualize
        screen: The Pygame screen to draw on
    """
    # Clear the screen
    screen.fill(WHITE)
    
    # Draw maze
    for y in range(maze.height):
        for x in range(maze.width):
            if maze.grid[y][x] == 1:
                pygame.draw.rect(screen, BLACK,
                               (x * CELL_SIZE, y * CELL_SIZE,
                                CELL_SIZE, CELL_SIZE))
    
    # Draw start and end points
    pygame.draw.rect(screen, GREEN,
                    (maze.start_pos[0] * CELL_SIZE,
                     maze.start_pos[1] * CELL_SIZE,
                     CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED,
                    (maze.end_pos[0] * CELL_SIZE,
                     maze.end_pos[1] * CELL_SIZE,
                     CELL_SIZE, CELL_SIZE))
    
    # Update the display
    pygame.display.flip()
    
    # Convert Pygame surface to numpy array for display
    data = pygame.surfarray.array3d(screen)
    data = np.transpose(data, (1, 0, 2))
    
    # Display the maze
    plt.figure(figsize=(10, 10))
    plt.imshow(data)
    plt.axis('off')
    plt.show()

class JupyterExplorer(Explorer):
    """
    Explorer class adapted for Jupyter notebook visualization.
    """
    def __init__(self, maze, screen):
        super().__init__(maze, visualize=True)
        self.screen = screen
        
    def draw_state(self):
        """Override draw_state to work with Jupyter"""
        # Clear the screen
        self.screen.fill(WHITE)
        
        # Draw maze
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if self.maze.grid[y][x] == 1:
                    pygame.draw.rect(self.screen, BLACK,
                                   (x * CELL_SIZE, y * CELL_SIZE,
                                    CELL_SIZE, CELL_SIZE))
        
        # Draw start and end points
        pygame.draw.rect(self.screen, GREEN,
                        (self.maze.start_pos[0] * CELL_SIZE,
                         self.maze.start_pos[1] * CELL_SIZE,
                         CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, RED,
                        (self.maze.end_pos[0] * CELL_SIZE,
                         self.maze.end_pos[1] * CELL_SIZE,
                         CELL_SIZE, CELL_SIZE))
        
        # Draw explorer
        pygame.draw.rect(self.screen, BLUE,
                        (self.x * CELL_SIZE, self.y * CELL_SIZE,
                         CELL_SIZE, CELL_SIZE))
        
        # Update the display
        pygame.display.flip()
        
        # Convert Pygame surface to numpy array for display
        data = pygame.surfarray.array3d(self.screen)
        data = np.transpose(data, (1, 0, 2))
        
        # Display the current state
        plt.figure(figsize=(10, 10))
        plt.imshow(data)
        plt.axis('off')
        plt.show()
        
        # Small delay to see the movement
        time.sleep(0.1)
        
        # Clear the output for the next frame
        clear_output(wait=True)

def compare_explorers(original_moves, enhanced_moves, maze):
    """
    Compare paths taken by original and enhanced explorers.
    
    Args:
        original_moves: List of positions from original explorer
        enhanced_moves: List of positions from enhanced explorer
        maze: The maze object
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    # Plot original path
    _plot_single_path(ax1, original_moves, maze, "Original Explorer", 'blue')
    
    # Plot enhanced path
    _plot_single_path(ax2, enhanced_moves, maze, "Enhanced Explorer", 'cyan')
    
    plt.tight_layout()
    plt.savefig('path_comparison.png')
    plt.show()

def _plot_single_path(ax, moves, maze, title, color):
    """Helper function to plot a single explorer's path"""
    # Create base maze
    maze_img = np.zeros((maze.height, maze.width, 3))
    for y in range(maze.height):
        for x in range(maze.width):
            if maze.grid[y][x] == 1:
                maze_img[y,x] = [0, 0, 0]  # Black walls
    
    # Draw path
    x_coords = [pos[0] for pos in moves]
    y_coords = [pos[1] for pos in moves]
    
    ax.imshow(maze_img)
    ax.plot(x_coords, y_coords, color=color, linewidth=2, alpha=0.7)
    
    # Mark start and end
    ax.scatter(maze.start_pos[0], maze.start_pos[1], c='green', s=200, label='Start')
    ax.scatter(maze.end_pos[0], maze.end_pos[1], c='red', s=200, label='End')
    
    ax.set_title(f"{title} - {len(moves)} moves")
    ax.axis('off')
    ax.legend()

def plot_performance_metrics(original_stats, enhanced_stats):
    """
    Plot comparative performance metrics between explorers.
    
    Args:
        original_stats: List of dicts with original explorer stats
        enhanced_stats: List of dicts with enhanced explorer stats
    """
    metrics = ['time_taken', 'moves', 'backtrack_count', 'moves_per_second']
    titles = ['Time Taken (s)', 'Total Moves', 'Backtrack Operations', 'Moves per Second']
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, metric in enumerate(metrics):
        orig_data = [s[metric] for s in original_stats]
        enh_data = [s[metric] for s in enhanced_stats]
        
        # Calculate means
        orig_mean = np.mean(orig_data)
        enh_mean = np.mean(enh_data)
        
        # Plot distributions
        axes[i].hist(orig_data, alpha=0.5, label=f'Original (μ={orig_mean:.1f})', color='blue')
        axes[i].hist(enh_data, alpha=0.5, label=f'Enhanced (μ={enh_mean:.1f})', color='cyan')
        
        axes[i].set_title(titles[i])
        axes[i].legend()
    
    plt.tight_layout()
    plt.savefig('performance_metrics.png')
    plt.show()

def visualize_exploration(moves, maze, title="Exploration Path"):
    """
    Visualize the complete exploration path.
    
    Args:
        moves: List of positions visited
        maze: The maze object
        title: Plot title
    """
    plt.figure(figsize=(10, 10))
    
    # Create base maze
    maze_img = np.zeros((maze.height, maze.width, 3))
    for y in range(maze.height):
        for x in range(maze.width):
            if maze.grid[y][x] == 1:
                maze_img[y,x] = [0, 0, 0]  # Black walls
    
    # Draw path
    x_coords = [pos[0] for pos in moves]
    y_coords = [pos[1] for pos in moves]
    
    plt.imshow(maze_img)
    plt.plot(x_coords, y_coords, 'b-', alpha=0.5)
    
    # Mark start and end
    plt.scatter(maze.start_pos[0], maze.start_pos[1], c='green', s=200, label='Start')
    plt.scatter(maze.end_pos[0], maze.end_pos[1], c='red', s=200, label='End')
    
    plt.title(f"{title} - {len(moves)} moves")
    plt.axis('off')
    plt.legend()
    plt.show()
