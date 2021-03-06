# Game of Life

This is an implemention of Conway's Game of Life. It has a WEB frontend and a python backend, communicating with websockets. You can check for the [online demo](https://deerchao.cn/game-of-life-py).


The game world is in size of 50 by 50, and cyclic, i.e. opposit sides are considered as connected. I intended to make it 500 by 500 at first, and then found out it will be too small on screen for observation, and too slow with a naive backend implemention. Since this is only a demo, I choose to quickly finish the job, and improve it later if really necessary. 

---

## Run

### With Docker

Just run `docker-compose up`, and see it at `http://localhost:8080`.

---

### Without Docker

In order to run, you should first start the server:

    py src/api/app.py

If there is a problem, check if these packages are installed:

    pip install websockets

Then open `src/ui/index.html` in your browser. Note that random color is generated for browsers at first connection to the backend, and then saved to localStorage. So if you want to replace your color, you can clear local storages and refresh the page.

---

## Deploy

### Without Docker

#### Publish
Run `build.bat` to prepare the `dist` folder. Copy everything inside to `/var/www/game-of-life-py`.

#### Serve UI
Serve the frontend in an existing, ssl secured nginx website:

    location /game-of-life-py {
            alias /var/www/game-of-life-py/ui;
            try_files $uri index.html =404;
    }

#### Serve API
Create a daemon service for backend(`/etc/systemd/system/game-of-life.service`)

    [Unit]
    Description=Game of Life Backend

    [Service]
    WorkingDirectory=/var/www/game-of-life-py/api
    ExecStart=/usr/bin/python3.8 /var/www/game-of-life-py/api/app.py
    Restart=always
    # Restart service after 10 seconds if the service crashes:
    RestartSec=10
    KillSignal=SIGINT
    SyslogIdentifier=python3-gameoflife
    User=www-data
    Environment=ASPNETCORE_ENVIRONMENT=Production
    Environment=DOTNET_PRINT_TELEMETRY_MESSAGE=false

    [Install]
    WantedBy=multi-user.target

Enable and start the service

    sudo systemctl enable game-of-life.service
    sudo systemctl start game-of-life.service

#### Add Security for API
Expose the backend to the public web securely via ngnix:

	location /ws/gameoflifepy {
		proxy_pass http://127.0.0.1:5678;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header Host $host;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

		# WebSocket support
		proxy_http_version 1.1;
		proxy_set_header Upgrade $http_upgrade;
		proxy_set_header Connection $http_connection;
	}

#### Done
Check `https://yousite.com/game-of-life-py` and celebrate.

---

### With Docker

#### Server UI and API

Copy `docker-compose-publish.yml` to your server, rename it to `docker-compose.yml`, run `docker-compose up`. You can also set up a service in the way described in the `Serve API` section without docker.

#### Add Security for UI and API

Expose the services to public web securely via ngnix:

	location ~ ^/game-of-life-py(/?)(.*) {
		proxy_pass http://127.0.0.1:8080/$2$is_args$args;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header Host $host;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	}

	location /ws/gameoflifepy {
		proxy_pass http://127.0.0.1:5678;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header Host $host;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

		# WebSocket support
		proxy_http_version 1.1;
		proxy_set_header Upgrade $http_upgrade;
		proxy_set_header Connection $http_connection;
	}

#### Done
Check `https://yousite.com/game-of-life-py` and celebrate.
