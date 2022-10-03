# shortest_path_finder

## Description

I created a Shortest path finder earlier withouth graphical interface (based on TechWithTim's Youtube channel), which worked fine but I missed the GUI and some features. Because of this, I modified my script and added the GUI with the help of Pygame.

The User receives a pre-made board of 18 X 18. This board contains a starting point, an end point, and "walls". The User can remove or add walls, and run the script which will find the shortest way between the starting point and the end point. The searching process and the shortest path are made visible for the User via the GUI.

Note: the goal of this project was to create the algorithm and make some GUI, not to make a full working game. Altough I see its incompleteness, I'm not planning to improve the script regarding its playing experience.

## How to use

By running the script, the User gets a pre-made board of 18 X 18. This board has the following items:
- The starting point, marked by 'O'
- The end point, marked by 'X'
- Walls, marked by '#'

The User can select cells by the mouse. It is also possible to modify the board: If the selected cell is empty, the User can change it to '#' by pushing the Enter. Also, a '#' cell can be cleared by selecting the cell and pushing the Enter.

Once the board is ready, the User can run the Path finder script by pushing the Space. The script finds the Starting point, looks for neighboring cells and adds them and the path to them to a Queue. It repeats these steps until the End point is found.
