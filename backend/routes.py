from backend.views import get_youtube_links
import aiohttp_cors

def setup_routes(app, cors):

    resource = cors.add(app.router.add_resource("/getlinks"))
    route = cors.add(
    resource.add_route("GET", get_youtube_links), {
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            allow_headers=("X-Requested-With", "Content-Type"),
        )
    })