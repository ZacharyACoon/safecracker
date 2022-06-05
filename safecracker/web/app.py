import trio
import json
from pathlib import Path
from quart import websocket, render_template
from quart_trio import QuartTrio

app = QuartTrio("yay", template_folder=Path(__file__).parent / "templates")
app.websocket_connections = set()


@app.route("/")
async def hello():
  return await render_template("index.html")


@app.websocket("/api/v1/websocket/data")
async def websocket_data():
  try:
    app.websocket_connections.add(websocket._get_current_object())
    async with trio.open_nursery() as nursery:
      nursery.start_soon(heartbeat)
  finally:
    app.websocket_connections.remove(websocket._get_current_object())


async def heartbeat():
  while True:
    await trio.sleep(5)
    await websocket.send(json.dumps({"type": "heartbeat"}))
