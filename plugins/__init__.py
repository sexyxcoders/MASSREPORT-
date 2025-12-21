from aiohttp import web

# ───────────────── ROUTES ───────────────── #

routes = web.RouteTableDef()


@routes.get("/", allow_head=True)
async def root_handler(request):
    return web.json_response(
        {
            "status": "ok",
            "service": "Nexa Report Bot",
            "message": "Bot is running"
        }
    )


# ───────────────── WEB SERVER ───────────────── #

async def web_server():
    app = web.Application(client_max_size=30 * 1024 * 1024)
    app.add_routes(routes)
    return app