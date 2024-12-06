import json
import pathlib
import argparse
from aiohttp import web


websockets = set()
current_annotations = []


async def index(request):
    """Serve the static HTML file"""
    static_dir = pathlib.Path(__file__).parent / "static"
    return web.FileResponse(static_dir / "index.html")


async def websocket_handler(request):
    """Handle WebSocket connections"""
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    websockets.add(ws)

    try:
        # Send current state to new client
        if current_annotations:
            for annotation in current_annotations:
                await ws.send_str(json.dumps(annotation))

        # Send init complete signal
        await ws.send_str(json.dumps({"action": "init-complete"}))

        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                data = json.loads(msg.data)
                if data.get('action') == 'clear-all':
                    current_annotations.clear()
                    for client in websockets:
                        if client != ws:
                            await client.send_str(msg.data)
                elif 'number' in data and 1 <= data['number'] <= 100:
                    current_annotations.append(data)
                    for client in websockets:
                        if client != ws:
                            await client.send_str(msg.data)
            elif msg.type == web.WSMsgType.ERROR:
                print(f'WebSocket connection closed with exception {ws.exception()}')
    finally:
        websockets.remove(ws)

    return ws


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='WebSocket server with configurable host and port')
    parser.add_argument('--host', default='localhost', help='Host to bind the server to (default: localhost)')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on (default: 8000)')
    return parser.parse_args()


def main():
    """Initialize and run the server"""
    args = parse_arguments()

    app = web.Application()
    app.router.add_get("/", index)
    app.router.add_get("/ws", websocket_handler)

    print(f"Starting server on {args.host}:{args.port}")
    web.run_app(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
