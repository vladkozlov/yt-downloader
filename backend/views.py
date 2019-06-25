import asyncio
import json
import logging
import urllib.parse
from functools import wraps

import pytube
from aiohttp import web
from pytube.exceptions import RegexMatchError


def cache_yt_link_to_redis(ttl=1200):

    def decorator(fn):
        if asyncio.iscoroutinefunction(fn):
            @wraps(fn)
            async def wrapper(*args, **kwargs):
                (request, yt_link) = kwargs['request'],  kwargs['link']
                yt_video_id = pytube.extract.video_id(yt_link)

                redis = request.app['redis_pool']
                
                redis_video_key = 'cache::urls::'+yt_video_id
                data = await redis.get(redis_video_key)

                if not data:
                    logging.info('Cache miss on video_id ' + yt_video_id)

                    try:
                        result = await fn(*args, **kwargs)
                        
                        p = redis.pipeline()
                        p.set(redis_video_key, json.dumps(result))
                        p.expire(redis_video_key, timeout=ttl)
                        await p.execute()
                    except pytube.exceptions.VideoUnavailable:
                        # if video unavailable ban it for 24 hours
                        p = redis.pipeline()
                        p.set(redis_video_key, json.dumps({"error": "unavailable"}))
                        p.expire(redis_video_key, timeout=86400)
                        await p.execute()
                        raise pytube.exceptions.VideoUnavailable

                    return result

                logging.info('Cache hit on video_id ' + yt_video_id)
                json_data = json.loads(data)

                if 'error' in json_data:
                    raise pytube.exceptions.VideoUnavailable

                return json_data

            return wrapper
    return decorator

@cache_yt_link_to_redis(ttl=1200)
async def get_video_meta_data(request=None, link=None, progressive=None):
    loop = request.loop
    executor = request.app['executor']

    data =  await loop.run_in_executor(executor, pytube.YouTube, link)
    
    video_streams = data.streams.filter(progressive=True).all()

    resp = {
        "title" : data.title,
        "rating" : data.rating,
        "views" : data.views,
        "streams" : [{
            "itag": vid.itag, 
            "mimeType": vid.mime_type, 
            "resolution": vid.resolution, 
            "fps": vid.fps,
            "isProgressive": vid.is_progressive,
            "url": vid.url+'&title='+urllib.parse.quote_plus(data.title)
        } for vid in video_streams]
    }

    return resp


async def get_youtube_links(request):
    if 'link' not in request.query:
        return web.json_response({'error': 'NO_LINK_PROVIDED'}, status=400)

    yt_link = request.query['link']
    
    try:
        result = await get_video_meta_data(request=request, link=yt_link, progressive=True)

        return web.json_response(result)
    except pytube.exceptions.RegexMatchError:
        return web.json_response({'error': 'BAD_URL'}, status=400)
    except pytube.exceptions.VideoUnavailable:
        return web.json_response({'error': 'VIDEO_UNAVAILABLE'}, status=400)
