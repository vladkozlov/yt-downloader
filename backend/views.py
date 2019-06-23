import asyncio
import logging
import random
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
                return web.json_response({'error': 'BAD_ARGS', "code": random.randint(0, 2000)}, status=400)

        result = await request.loop.run_in_executor(request.app['executor'], get_video_meta, yt_link)

        video_streams = None
        if yt_progressive:
            video_streams = result.streams.filter(progressive=yt_progressive).all()
        else:
            video_streams = result.streams.all()

        resp = {
            "title" : result.title,
            "description" : result.description,
            "length" : result.length,
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

    return web.json_response({'error': 'NO_LINK_PROVIDED', "code": random.randint(0, 2000)}, status=400)

# async def get_video_url(request):
#     if 'link' in request.query and 'itag' in request.query:
#         yt_link = request.query['link']
#         itag = request.query['itag']
#         result = await asyncio.create_task(get_video_meta(yt_link))
#         stream = result.streams.get_by_itag(itag)

#         if stream:
#             return web.HTTPTemporaryRedirect(stream.url+'&title=Hammond+Grapple+Guide+-+Master+The+Hook+ft.+Ventari')
#             # stream.url

# async def get_youtube_vid_by_itag(request):
#     if 'link' in request.query and 'itag' in request.query:
#         yt_link = request.query['link']
#         itag = request.query['itag']
#         result = await asyncio.create_task(get_video_meta(yt_link))
#         # video_streams = result.streams.filter(itag=itag).all()
#         stream = result.streams.get_by_itag(itag)

#         if stream:
#             resp = web.StreamResponse(status=200, reason="Ok", headers={'Content-Type': stream.mime_type})
            
#             stream_buffer = stream.stream_to_buffer()
#             await resp.prepare(request)

#             with stream_buffer as st:
#                 await resp.write(st)
#                 # await asyncio.sleep(1)
    
#             return resp

            
#             return resp
        
#         return web.json_response({'error':'No stream with itag {0} found!'.format(itag), "errorCode": random.randint(0, 2000)})

        
#     return web.json_response({'error':'No link or itag argument found!', "errorCode": random.randint(0, 2000)})
