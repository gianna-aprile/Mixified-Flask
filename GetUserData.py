import aiohttp
import asyncio
import ssl
import certifi

async def getUserId(token):
    url = 'https://api.spotify.com/v1/me'
    ssl_context = ssl.create_default_context()
    ssl_context.load_verify_locations(certifi.where())
    HEADER =  {'Authorization': 'Bearer {}'.format(token)}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADER, ssl=ssl_context) as resp:
            data = await resp.json(content_type=None)
            if 'id' in data:
                userId = data['id']
                return userId
            return


async def getUserSavedTracks(token):
    savedTracks = []
    offset = 0
    ssl_context = ssl.create_default_context()
    ssl_context.load_verify_locations(certifi.where())
    HEADER =  {'Authorization': 'Bearer {}'.format(token)}
    url = f'https://api.spotify.com/v1/me/tracks?limit=50&offset={offset}'
    
    while len(savedTracks) < 300:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADER, ssl=ssl_context) as resp:
                data = await resp.json(content_type=None)
                if 'items' in data:
                    for item in data['items']:
                        savedTracks.append(item['track'])

                    offset += 50

    return savedTracks


async def getUserTopArtists(token):
    topArtists = []
    url = 'https://api.spotify.com/v1/me/top/artists?limit=50'
    ssl_context = ssl.create_default_context()
    ssl_context.load_verify_locations(certifi.where())
    HEADER =  {'Authorization': 'Bearer {}'.format(token)}
    params = {'time_range': 'medium_term'}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADER, params=params, ssl=ssl_context) as resp:
            data = await resp.json(content_type=None)
            if 'items' in data:
                topArtists = data['items']

    if len(topArtists) < 50:
        params = {'time_range': 'short_term'}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADER, params=params, ssl=ssl_context) as resp:
                data = await resp.json(content_type=None)
                if 'items' in data:
                    topArtists += data['items']
    
    if len(topArtists) < 50:
        params = {'time_range': 'long_term'}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADER, params=params, ssl=ssl_context) as resp:
                data = await resp.json(content_type=None)
                if 'items' in data:
                    topArtists += data['items']

    del(topArtists[50:])
    
    return topArtists
    

async def getUserTopTracks(token):
    topTracks = []
    url = 'https://api.spotify.com/v1/me/top/tracks?limit=50'
    ssl_context = ssl.create_default_context()
    ssl_context.load_verify_locations(certifi.where())
    HEADER =  {'Authorization': 'Bearer {}'.format(token)}
    params = {'time_range': 'medium_term'}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADER, params=params, ssl=ssl_context) as resp:
            data = await resp.json(content_type=None)
            if 'items' in data:
                topTracks = data['items']

    if len(topTracks) < 50:
        params = {'time_range': 'short_term'}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADER, params=params, ssl=ssl_context) as resp:
                data = await resp.json(content_type=None)
                if 'items' in data:
                    topTracks += data['items']
    
    if len(topTracks) < 50:
        params = {'time_range': 'long_term'}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADER, params=params, ssl=ssl_context) as resp:
                data = await resp.json(content_type=None)
                if 'items' in data:
                    topTracks += data['items']

    del(topTracks[50:])
    return topTracks