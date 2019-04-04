import base64
import concurrent.futures
import glob
import gzip
import json
from collections import defaultdict
from copy import deepcopy
import logging
from lxml import html
import os

DATA_BASEPATH = '/home/dante0shy/PycharmProjects/homwor_gmy/data'
OUTPUT_BASEPATH = '/home/dante0shy/PycharmProjects/homwor_gmy/processed_data'
if not os.path.exists(OUTPUT_BASEPATH):
    os.mkdir(OUTPUT_BASEPATH)
# Load JSON templates for all object types
with open(os.path.join(os.path.dirname(__file__),'Model',"base_song_flat.json"), "r") as f:
    base_song_flat = json.load(f)
with open(os.path.join(os.path.dirname(__file__),'Model',"base_artist.json"), "r") as f:
    base_artist = json.load(f)
with open(os.path.join(os.path.dirname(__file__),'Model',"base_album.json"), "r") as f:
    base_album = json.load(f)
with open(os.path.join(os.path.dirname(__file__),'Model',"base_simple_song.json"), "r") as f:
    base_simple_song = json.load(f)

# Parallelism coordinator
executor = concurrent.futures.ProcessPoolExecutor()


# Turn each album from HTML to album object
def handle_album(htmlcontent, album_name, artistobj):
    albobj = deepcopy(base_album)
    albobj['title'] = album_name
    albumhtml = html.fromstring(htmlcontent)
    songs_in_album = [dict(x.attrib) for x in albumhtml.cssselect("ol li a")]
    for s in songs_in_album:
        if 'href' not in s.keys() or (artistobj['unique_name'] not in s['href'] or 'redlink' in s['href']):
            continue
        s['href'] = s['href'].replace("/wiki/", "")
        albobj['songs'].append(s)
    albumplainlinks = albumhtml.cssselect('.plainlinks table a')
    for link in albumplainlinks:
        if dict(link.attrib)['title'].startswith("Category:Albums"):
            albobj['year'] = int(link.text)
        elif dict(link.attrib)['title'].startswith("Category:Genre"):
            albobj['genre'] = link.text

    return albobj


# Turn each song from HTML to song object
def handle_song(htmlcontent, currsong, artistobj):
    htmlobj = html.fromstring(htmlcontent)
    songobj = deepcopy(base_simple_song)
    songobj['href'] = currsong
    songobj['title'] = htmlobj.cssselect('div[id="song-header-container"] div b')[0].text.strip()
    lyrics = html.tostring(htmlobj.cssselect(".lyricbox")[0]).decode()
    lyrics = lyrics.replace('<div class="lyricbox">', '').replace('</div>', ""). \
        replace('<div class="lyricsbreak">', '').replace("<br>", '\n')
    songobj["lyrics"] = lyrics
    return songobj


# Each page may be either a song or an album. Handle accordingly by characteristics.
def handle_song_or_album(artistobj, song_or_album):
    artist = artistobj['unique_name'] if artistobj['unique_name'][0] !='/' else artistobj['unique_name'][1:]
    with open(os.path.join(DATA_BASEPATH, "%s:%s" % (artist, song_or_album))) as f:
        fcontent = f.read()
    htmlcontent = gzip.decompress(base64.b64decode(fcontent))
    if "song is a cover of" in htmlcontent.decode():
        return
    if "'lyricbox'" in htmlcontent.decode():
        kind = 'song'
        return kind, handle_song(htmlcontent, song_or_album, artistobj)
    else:
        kind = 'album'
        return kind, handle_album(htmlcontent, song_or_album, artistobj)


# Get all data from disk and persist it in a JSON listing all files, since it is an expensive operation.
def get_data_dict():
    res_dict = defaultdict(lambda: [])
    try:
        with open(os.path.join(os.path.dirname(__file__),'Model',"allfiles.json"), 'r') as f:
            retval = json.load(f)
    except:
        logging.exception("Failed reading allfiles.json, reverting to scan files")
        allfiles = glob.glob(os.path.join(DATA_BASEPATH, '*'))
        for fp in allfiles:
            if fp.count(":") > 1:
                continue
            fp = fp.replace(DATA_BASEPATH+'/', "")
            band_and_song_or_album = fp.split(":")
            band = band_and_song_or_album[0]

            if len(band_and_song_or_album) > 1:
                res_dict[band].extend(band_and_song_or_album[1:])

        with open(os.path.join(os.path.dirname(__file__),'Model',"allfiles.json"), 'w') as f:
            json.dump(dict(res_dict), f, indent=True)
        retval = dict(res_dict)
    return retval


# Create a mapping between a song and the album that contains it.
def build_album_reverse_index(entities):
    idx = {}
    for _, album in [x for x in entities if x[0] == 'album']:
        songsinalbum = album['songs']
        del album['songs']
        for song in songsinalbum:
            idx[song['href']] = album
    return idx


# Parse all data of a single band to a single JSON file on disk.
def handle_band(artist_songs_and_albums):
    artist = artist_songs_and_albums[0]
    songs_and_albums = artist_songs_and_albums[1]
    artist_obj = deepcopy(base_artist)
    del artist_obj['albums']
    artist_obj['unique_name'] = artist
    entities = []
    for song_or_album in songs_and_albums:
        creation = handle_song_or_album(artist_obj, song_or_album)
        if creation is not None:
            entities.append(creation)
    album_revidx = build_album_reverse_index(entities)
    flat_songs = []
    for _, song in [x for x in entities if x[0] == 'song']:
        try:
            album_of_song = album_revidx["%s:%s" % (artist, song['href'].split('&&')[0])]
        except:
            continue
        flatobj = deepcopy(base_song_flat)
        flatobj.update(song)
        flatobj['album'].update(album_of_song)
        flatobj['artist'].update(artist_obj)
        flat_songs.append(flatobj)
    if len(flat_songs) > 0:
        with open(os.path.join(OUTPUT_BASEPATH, artist+'.json'), 'w') as f:
            # f.write(.encode())
            json.dump(flat_songs, f)
    print(artist)


if __name__ == '__main__':
    allfiles = get_data_dict()
    if '' in allfiles.keys():
        allfiles.pop('')
    pardata = [(artist, songs_and_albums) for artist, songs_and_albums in allfiles.items()]
    # list(executor.map(handle_band, pardata))
    list(map(handle_band, pardata))
