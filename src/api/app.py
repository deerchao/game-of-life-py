from urllib.parse import urlparse, parse_qs
import json
import asyncio
import websockets
import logging
from life_game import LifeGame
import rgb_color


worldWidth = 50
worldHeight = 50
interval = 3
bind_ip = "0.0.0.0"
bind_port = 5678



async def main():
    serving = websockets.serve(handle_user, bind_ip, bind_port)
    ticking = asyncio.create_task(run_game(interval))
    await asyncio.gather(ticking, serving)


async def run_game(interval):
    while True:
        await asyncio.sleep(interval)
        game.tick()
        await notify_users(state_sync_message())


async def handle_user(websocket, path):
    color = parse_qs(urlparse(path).query).get('color', ['0'])
    try:
        color = int(color[0])
    except:
        color = 0

    color = await register_user(websocket, color)

    try:
        async for message in websocket:
            data = json.loads(message)

            if data['action'] == "update-cell":
                r = data["row"]
                c = data["column"]
                game.update_cell(r, c, color)
                await notify_users(state_sync_message())
    except Exception as e:
        logging.error(e)
    finally:
        unregister_user(websocket)


async def register_user(websocket, color):
    if color == 0:
        color = generate_color()
        await websocket.send(user_init_message(color))

    users[websocket] = color
    print(f"user connected {websocket} {color}")
    return color


def unregister_user(websocket):
    users.pop(websocket)
    print(f"user disconnected {websocket}")


async def notify_users(message):
    sockets = users.keys()
    if len(sockets) > 0:
        await asyncio.gather(*[socket.send(message) for socket in sockets])


def generate_color():
    # exclude colors too close to black(0, means dead) so we can observe more easily
    return rgb_color.random(0x333333)


def state_sync_message():
    return json.dumps({"type": "sync", "board": game.board, "generation": game.generation, "version": game.version})


def user_init_message(color):
    return json.dumps({"type": "init", "color": color, "board": game.board, "generation": game.generation, "version": game.version})


def create_game(width, height):
    board = [[0] * width for _ in range(0, height)]
    return LifeGame(board)

logging.basicConfig()
users = {}  # {websocket: color}
game = create_game(worldWidth, worldHeight)

asyncio.run(main())
