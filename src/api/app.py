from urllib.parse import urlparse, parse_qs
import json
import asyncio
import websockets
import logging
from life_game import LifeGame
import rgb_color


worldWidth = 500
worldHeight = 500
interval = 3
bind_ip = "127.0.0.1"
bind_port = 5678


def create_game(width, height):
    board = [[0] * width for _ in range(0, height)]
    return LifeGame(board)


async def run_game(game, interval):
    while True:
        await asyncio.sleep(interval)
        game.tick()


def generate_color():
    # exclude colors too close to black(0, means dead) so we can observe more easily
    return rgb_color.random(0x333333)


def state_sync_message():
    return json.dumps({"type": "sync", "board": game.board, "generation": game.generation})


def user_init_message(color):
    return json.dumps({"type": "init", "color": color})


async def handle_user(websocket, path):
    color = parse_qs(urlparse(path).query).get('color', ['0'])
    try:
        color = int(color[0])
    except:
        color = 0

    if color == 0:
        color = generate_color()
        await websocket.send(user_init_message(color))

    users[websocket] = color

    while True:
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
            users.pop(websocket)
            return


async def notify_users(message):
    sockets = users.keys()
    if len(sockets) > 0:
        await asyncio.wait([socket.send(message) for socket in sockets])


logging.basicConfig()

# [websocket: color]
users = {}
game = create_game(worldWidth, worldHeight)

start_server = websockets.serve(handle_user, bind_ip, bind_port)

loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.create_task(run_game(game, interval))
loop.run_forever()
