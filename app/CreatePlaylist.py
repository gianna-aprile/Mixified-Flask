import asyncio
import requests
from app.ArtistDataHandling import getRelatedArtists, getArtistsOfTracks, filterArtistsByGenre
from app.TrackDataHandling import getTopSongsOfArtists
from app.GetUserData import getUserTopArtists, getUserId, getUserSavedTracks, getUserTopTracks

# *** Steps for topRelatedArtists, recentRelatedArtists, and topRelatedTracks type playlists
# Create a base artist list to start with depending on playlist type
# Find their related artists (randomization included)
# Randomly choose a top song of each of the relatedArtists
# Create the playlist and add tracks
def relatedArtistPlaylistDriver(token, playlistType):
    if playlistType == 'topRelatedArtists':
        startingArtists = asyncio.run(getUserTopArtists(token))
    elif playlistType == 'recentRelatedArtists':
        savedTracks = asyncio.run(getUserSavedTracks(token))
        startingArtists = getArtistsOfTracks(savedTracks)
        del(startingArtists[50:])
    elif playlistType == 'topRelatedTracks':
        topTracks = asyncio.run(getUserTopTracks(token))
        startingArtists = getArtistsOfTracks(topTracks)

    startingArtists = list(filter(None, startingArtists)) 
    relatedArtists = asyncio.run(getRelatedArtists(token, startingArtists))
    relatedArtists = list(filter(None, relatedArtists)) 

    topTracks = asyncio.run(getTopSongsOfArtists(token, relatedArtists))
    topTracks = list(filter(None, topTracks)) 

    if topTracks is not None and len(topTracks) > 0:
        userId = asyncio.run(getUserId(token))

        playlistID = generatePlaylist(token, playlistType, userId)
        snapshotID = addTracks(token, playlistID, topTracks, userId)

        if 'snapshot_id' in snapshotID:
            return 'success'
        elif 'error' in snapshotID: # Errors for UI
            error = snapshotID['error']
            if 'message' in error:
                message = error['message']
                if message == 'API rate limit exceeded':
                    return 'rate exceeded'
                elif message == 'Invalid playlist Id':
                    return 'creation error'
    return 'fail'


# *** Steps for Genre type playlists
# Gather collection of artists from the user's saved tracks
# Check to see if the artist belongs to the specified genre
# Find their related artists (randomization included)
# Randomly choose a top song of each of the relatedArtists
# Create the playlist and add tracks
def genrePlaylistDriver(token, playlistType):
    savedTracks = asyncio.run(getUserSavedTracks(token))
    artistsOfTracks = getArtistsOfTracks(savedTracks)
    artistsOfTracks = list(filter(None, artistsOfTracks)) 
 
    filteredArtists = asyncio.run(filterArtistsByGenre(token, artistsOfTracks, playlistType))

    if len(filteredArtists) == 0:
        return 'fail'

    del(filteredArtists[50:])

    relatedArtists = asyncio.run(getRelatedArtists(token, filteredArtists))
    relatedArtists = list(filter(None, relatedArtists)) 
    topTracks = asyncio.run(getTopSongsOfArtists(token, relatedArtists))
    topTracks = list(filter(None, topTracks)) 

    if topTracks is not None and len(topTracks) > 0:
        userId = asyncio.run(getUserId(token))

        playlistID = generatePlaylist(token, playlistType, userId)
        snapshotID = addTracks(token, playlistID, topTracks, userId)

        if 'snapshot_id' in snapshotID:
            return 'success'
        elif 'error' in snapshotID: # Errors for UI
            error = snapshotID['error']
            if 'message' in error:
                message = error['message']
                if message == 'API rate limit exceeded':
                    return 'rate exceeded'
                elif message == 'Invalid playlist Id':
                    return 'creation error'
    return 'fail'


def generatePlaylist(token, playlistType, userId):
    playlistName = choosePlaylistName(playlistType)
    
    description = "Thanks for using Mixified! Click here to make another playlist: https://gianna-aprile.github.io/Mixified-React/"
    
    reqHeader = {'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'application/json'}
    reqBody = {'name': playlistName, 'description': description}
    res = requests.post('https://api.spotify.com/v1/users/{}/playlists'.format(userId), headers=reqHeader, json=reqBody)
    
    if res.status_code in [200, 201]:
        playlistID = res.json()['id']
        return playlistID
    return 


def addTracks(token, playlistID, tracks, userId):
    trackURIs = []
    for track in tracks:
        trackURIs.append(track['uri'])

    reqHeader = {'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'application/json'}
    reqBody = {'uris': list(trackURIs)}

    res = requests.post('https://api.spotify.com/v1/users/{}/playlists/{}/tracks'.format(userId, playlistID), 
            headers=reqHeader, json=reqBody)
    return res.json()


def choosePlaylistName(playlistType):
    switcher={
        'topRelatedArtists':'Mixified Top Related Artists',
        'recentRelatedArtists':'Mixified Recent Related Artists',
        'topRelatedTracks':'Mixified Top Related Tracks',
        'pop':'Mixified Pop Playlist',
        'hip hop':'Mixified Hip Hop Playlist',
        'rap':'Mixified Rap Playlist',
        'r&b':'Mixified R&B Playlist',
        'edm':'Mixified EDM Playlist',
        'house':'Mixified House Playlist',
        'country':'Mixified Country Playlist',
        'alternative':'Mixified Alternative Playlist',
        'rock':'Mixified Rock Playlist'
    }
    return switcher.get(playlistType,"Invalid type")
