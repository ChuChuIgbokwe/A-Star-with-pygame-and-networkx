# A-Star-with-pygame-and-networkx

I implemented a A star game in Python using the pygame and networkx libraries.
* I built my 2d grid simulator using pygame and mapped it to an actual 2D grid lattice in networkx. 
* I used the A star algorithm to solve a policy guiding the robot from start to goal which I implemented using Networkx’s in built A star function. 
* The A star is edge based so for a node in the graph to be an obstacle all the edges connected to that node have to be weighted. I weighted obstacle nodes using the _set_barrier_weights method.
* I used the euclidean distance(_dist method) as my heuristic and passed it to the a star function
* The _draw_cell method is used for filling out grid squares clicked on
* The _clear_cell method is used for clearing out grid squares clicked on
* The _draw_path method is used to fill out the simulator with the A star path
* The _whipeout method fills the grid with orange if no path can be found between the start and goal cells
* To run it all I use four flags start, goal, obstacle and solved flags. This ensures that the program flows from 
  * setting a start point to 
  * setting a goal to 
  * adding obstacles and solving the path or just solving the path
  * to resetting the simulator. Either removing obstacles and the solved path or removing everything on the simulator
* The A star function works as expected, however it’s failure condition behaves poorly. If there isn’t any path , it’ll create a path that goes through an obstacle. I fix this with 
```python 
set(path).intersection(self.barriers) == set()
``` 
which compares path nodes to barrier nodes and ensures there is no intersection 
* The instructions to run the program are 
  * Place your start point
  * Place your end point
  * Add obstacles or press spacebar to solve
  * Press ENTER to restart simulator
  * Press R to remove obstacles 
