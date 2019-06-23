import asyncio
import logging
import urllib.parse

import pytube
from aiohttp import web


def get_video_meta(link):
    video = pytube.YouTube(link)
    return video

async def get_youtube_links(request):
    if 'link' in request.query:
        yt_link = request.query['link']
        yt_progressive = True

        if 'progressiveonly' in request.query:
            if request.query['progressiveonly'] == 'true':
                yt_progressive = True
            elif request.query['progressiveonly'] == 'false':
                yt_progressive = False
            else:
                return web.json_response({'error': 'BAD_ARGS'}, status=400)

        result = await request.loop.run_in_executor(request.app['executor'], get_video_meta, yt_link)

        video_streams = None
        if yt_progressive:
            video_streams = result.streams.filter(progressive=yt_progressive).all()
        else:
            video_streams = result.streams.all()

        resp = {
            "title" : result.title,
            "rating" : result.rating,
            "views" : result.views,
            "streams" : [{
                "itag": vid.itag, 
                "mimeType": vid.mime_type, 
                "resolution": vid.resolution, 
                "fps": vid.fps,
                "isProgressive": vid.is_progressive,
                "url": vid.url+'&title='+urllib.parse.quote_plus(result.title)
            } for vid in video_streams]
        }
        return web.json_response(resp)

    return web.json_response({'error': 'NO_LINK_PROVIDED'}, status=400)