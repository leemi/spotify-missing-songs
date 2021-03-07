#!/usr/bin/env python3

import io
from urllib import request
import json
import re

def search_wayback(track_id):
    url = "https://archive.org/wayback/available?url=https://open.spotify.com/track/" + track_id

    req = request.Request(url)
    r = request.urlopen(req).read()
    search_result = json.loads(r.decode('utf-8'))

    try:
        closest_url = search_result["archived_snapshots"]["closest"]["url"]
    except:
        return "??? - No Snapshot"

    req = request.Request(closest_url)
    r = request.urlopen(req).read()
    spotify_page = r.decode('utf-8')

    try:
        search = re.search(r'<title>(.*) (on|\|) Spotify</title>', spotify_page)
        return search.groups()[0]
    except:
        pass

    return "???"

def search_missing():
    with io.open("playlists.txt", mode="r", encoding="utf-8") as infile:
        with io.open("songs-missing.txt", mode="w", encoding="utf-8") as outfile:
            for line in infile:
                if line.startswith("\t\t\t"):
                    spotify_id = line.replace("\t\t\tspotify:track:", "").strip()
                    print(spotify_id, end="")
                    result = search_wayback(spotify_id)
                    print("\t" + result)
                    outfile.write(spotify_id + "\t" + result + "\n")

def main():
    search_missing()

if __name__ == "__main__":
    main()
