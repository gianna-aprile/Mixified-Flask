from flask import Flask, jsonify, request
from flask_cors import CORS
from app.CreatePlaylist import relatedArtistPlaylistDriver, genrePlaylistDriver
import sys

app = Flask(__name__)
CORS(app)

@app.route('/api/topRelatedArtists', methods=['GET'])
def topRelatedArtists():
    token = request.args.get('token')
    res = relatedArtistPlaylistDriver(token, 'topRelatedArtists')
    response = jsonify({'data': res})
    return response

@app.route('/api/recentRelatedArtists', methods=['GET'])
def recentRelatedArtists():
    token = request.args.get('token')
    res = relatedArtistPlaylistDriver(token, 'recentRelatedArtists')
    response = jsonify({'data': res})
    return response

@app.route('/api/topRelatedTracks', methods=['GET'])
def topRelatedTracks():
    token = request.args.get('token')
    res = relatedArtistPlaylistDriver(token, 'topRelatedTracks')
    response = jsonify({'data': res})
    return response

@app.route('/api/pop', methods=['GET'])
def pop():
    token = request.args.get('token')
    res = genrePlaylistDriver(token, 'pop')
    response = jsonify({'data': res})
    return response

@app.route('/api/hiphop', methods=['GET'])
def hiphop():
    token = request.args.get('token')
    res = genrePlaylistDriver(token, 'hip hop')
    response = jsonify({'data': res})
    return response

@app.route('/api/rap', methods=['GET'])
def rap():
    token = request.args.get('token')
    res = genrePlaylistDriver(token, 'rap')
    response = jsonify({'data': res})
    return response

@app.route('/api/r&b', methods=['GET'])
def rNb():
    token = request.args.get('token')
    res = genrePlaylistDriver(token, 'r&b')
    response = jsonify({'data': res})
    return response

@app.route('/api/edm', methods=['GET'])
def edm():
    token = request.args.get('token')
    res = genrePlaylistDriver(token, 'edm')
    response = jsonify({'data': res})
    return response

@app.route('/api/house', methods=['GET'])
def house():
    token = request.args.get('token')
    res = genrePlaylistDriver(token, 'house')
    response = jsonify({'data': res})
    return response

@app.route('/api/country', methods=['GET'])
def country():
    token = request.args.get('token')
    res = genrePlaylistDriver(token, 'country')
    response = jsonify({'data': res})
    return response

@app.route('/api/alternative', methods=['GET'])
def alternative():
    token = request.args.get('token')
    res = genrePlaylistDriver(token, 'alternative')
    response = jsonify({'data': res})
    return response

@app.route('/api/rock', methods=['GET'])
def rock():
    token = request.args.get('token')
    res = genrePlaylistDriver(token, 'rock')
    response = jsonify({'data': res})
    return response
