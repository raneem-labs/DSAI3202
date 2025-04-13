Question 1: Description of the Automated Maze Explorer

 1. Algorithms Followed with the Explorer
The enhanced maze explorer applies the right-hand rule algorithm yet includes backtracking and loop detection features. The process works like this:

The explorer is instructed on the right as well as backward movement. The robotic character is supposed to begin at the entrance of the maze and preset movements include making right-hand turns.

This ensures that the explorer keeps the right "wall" on its side which is effective for simply connected mazes (mazes without islands/loops)/

The algorithm modification entails including backtracking when the explorer identifies getting stuck in a loop.


2. Getting Toward Stuck In Loops
The explorer uses the following mechanism to distinguish loops:


With the help of `move history` tree, it is easy to map the last 3 moves. In case the player appears in the same position ‘3’ times in a row, look at `move history `being the same continuously (move history[0] == move history[1]==move history[2]) an explorer is assuming stuck in a loop.

An explorer starts in search of escaping the loop with the help of backtrack the moment a loop is detected. An explorer moves BACK.


3. Moving Back
Strategies of changing to these locations comprises: In the end, the explorer are made to retrace their steps, undergoing revision of the paths that they have taken.

Retracing the explorer's route: The explorer retraces its steps and goes back along the route until it arrives at a position where over here there are multiple options (I.E., more than one possible direction to move).   

Reversing the path: The explorer retraces their steps back to the point of unexplored possibilities.  

Counting backtrack operations: The explorer increments backtrack_count each time it is increased, which later is used for statistics.  

4. Provided Statistics  

The explorer outputs the following stats after exploration:  

Total time taken - The time (in seconds) it took to solve the maze.  

Total moves made - The moves performed by the explorer.  

Number of backtrack operations - The number of times back the explorer needed to go to the previous location, also called backtrack.  

Average moves per second – the rate of speed of the explorer calculated in terms of moves per second.
Important Points to Note:

Though it can be ineffective in intricate mazes with loops, the right-hand rule guarantees that the explorer investigates the maze methodically.
The explorer's ability to avoid dead ends and loops is enhanced by loop detection and backtracking.
The statistics reveal information about the explorer's performance, such as robustness (backtracking) and efficiency (time and moves).
An overview of the specifics of implementation:

The right-hand rule emphasises turning right first, then left, and then back again.
Loop detection: Identifies recurring positions using move_history.
Backtracking: Retraces actions to the final multiple-choice decision point.
Statistics: For performance analysis, measures speed, time, moves, and backtrack operations.


