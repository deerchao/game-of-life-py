# Game of Life

This is an implemention of Conway's Game of Life. It has a WEB frontend and a python backend, communicating with websockets.


The game world is in size of 50 by 50, and cyclic, i.e. opposit sides are considered as connected. I intended to make it 500 by 500 at first, and then found out it will be too small on screen for observation, and too slow with a naive backend implemention. Since this is only a demo, I choose to quickly finish the job, and improve it later if really necessary. 


## Run

In order to run, you should first start the server:

    py src/api/app.py

If there is a problem, check if these packages are installed:

    pip install py-linq
    pip install websockets

Then open `src/ui/index.html` in your browser. Note that random color are generated for browsers at first connection to the backend, and then saved to localStorage. So if you want to replace your color, you can clear local storages and refresh the page.
