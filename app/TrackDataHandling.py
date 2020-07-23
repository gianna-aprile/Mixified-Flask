import aiohttp
import random 
import asyncio
import ssl
import certifi

async def getTopSongsOfArtists(token, artists):
    async def getTopSongsOfArtist(token, artist):
        artistId = artist['id']
        url = f'https://api.spotify.com/v1/artists/{artistId}/top-tracks?country=US'
        ssl_context = ssl.create_default_context()
        ssl_context.load_verify_locations(certifi.where())
        HEADER =  {'Authorization': 'Bearer {}'.format(token)}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADER, ssl=ssl_context) as resp:
                data = await resp.json(content_type=None)

                if 'tracks' in data:
                    if len(data['tracks']) >= 10:
                        rand = random.randrange(9)
                        addTrack = data['tracks'][rand]
                        return addTrack
                    
                    elif len(data['tracks']) != 0: # Artist only has a few songs, just add the first
                        addTrack = data['tracks'][0]
                        return addTrack

                return

    return await asyncio.gather(*[getTopSongsOfArtist(token, artist) for artist in artists])