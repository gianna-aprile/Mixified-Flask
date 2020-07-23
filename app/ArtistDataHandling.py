import aiohttp
import random 
import asyncio
import ssl
import certifi

async def getRelatedArtists(token, startingArtists):
    async def getRelatedArtist(token, artist):
        artistId = artist['id']
        url = f'https://api.spotify.com/v1/artists/{artistId}/related-artists'
        ssl_context = ssl.create_default_context()
        ssl_context.load_verify_locations(certifi.where())
        HEADER =  {'Authorization': 'Bearer {}'.format(token)}
       
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADER, ssl=ssl_context) as resp:
                data = await resp.json(content_type=None)
                if 'artists' in data:
                    if len(data['artists']) >= 20:
                        rand = random.randrange(19)
                        relatedArtist = data['artists'][rand]
                        return relatedArtist

                    elif len(data['artists']) != 0: # Rare case: if artist does not have many related artists
                        relatedArtist = data['artists'][0]
                        return relatedArtist
                return
        
    return await asyncio.gather(*[getRelatedArtist(token, artist) for artist in startingArtists])

async def filterArtistsByGenre(token, artists, genre):
    artistIds = []
    for artist in artists:
        if 'id' in artist:
            artistIds.append(artist['id'])

    url = f'https://api.spotify.com/v1/artists'
    ssl_context = ssl.create_default_context()
    ssl_context.load_verify_locations(certifi.where())
    HEADER =  {'Authorization': 'Bearer {}'.format(token)}
    
    startingIndex = 0
    endIndex = len(artistIds) if len(artistIds) < 49 else 49
    retList = []

    while len(retList) < 50 and startingIndex < len(artistIds):
        choppedList = artistIds[startingIndex : endIndex]
        commaSepStr = ''
        for artistId in choppedList:
            if commaSepStr == '':
                commaSepStr = artistId
            else:
                commaSepStr = commaSepStr + ',' + artistId
       
        params = {'ids': commaSepStr}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADER, params=params, ssl=ssl_context) as resp:
                data = await resp.json(content_type=None)
                if 'artists' in data:
                    for artist in data['artists']:
                        if 'genres' in artist and genre in artist['genres']:
                           
                            retList.append(artist)
        
        startingIndex = startingIndex+50
        endIndex = endIndex+50 if endIndex+50 < len(artistIds) else len(artistIds)

    return retList


def getArtistsOfTracks(tracks):
    artists = []
    for track in tracks:
        artists.append(track['artists'][0])

    return artists


