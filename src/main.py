#!/usr/bin/env python
from utils import Sorter
from music import MusicProvider
from storage import LocalJsonFile
from analytics import AnalyticsProvider


if __name__ == "__main__":
    storage_provider = LocalJsonFile()

    # Get artists and track from the 80s with track thats in Aritist's list of top
    # 10 played tracks on Spotify
    music = MusicProvider()
    artists = music.search_artist_by_genre("glam metal", year="1980-1989")
    artists_with_top_10_tracks = music.get_artists_top_ten_tracks(artists)
    artists_with_top_80s_track = music.get_artists_top_track_from_years(
        artists_with_top_10_tracks, year_range=(1980, 1989)
    )
    top_80s_songs_with_lyrics = music.get_lyrics_for_song(artists_with_top_80s_track)

    # Get sentiment for each track
    analytics = AnalyticsProvider()
    scores = [song for song in analytics.get_sentiment(top_80s_songs_with_lyrics)]

    # Sort [rank] by sentiment
    sorter = Sorter()
    sorted_list = sorter.by_happy(scores)

    [
        print(f'{idx + 1}. {song["artist"]} - {song["songTitle"]}')
        for idx, song in enumerate(sorted_list)
    ]

    storage_provider.create(sorted_list)
