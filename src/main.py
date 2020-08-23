#!/usr/bin/env python
from music import MusicProvider
from storage import LocalJsonFile
from analytics import AnalyticsProvider


if __name__ == "__main__":
    gather_data = False
    get_scores = True

    storage_provider = LocalJsonFile()

    if gather_data:

        # Get artists and track from the 80s with track thats in Aritist's list of top
        # 10 played tracks on Spotify
        music = MusicProvider()
        artists = music.search_artist_by_genre("glam metal", year="1980-1989")
        artists_with_top_10_tracks = music.get_artists_top_ten_tracks(artists)
        artists_with_top_80s_track = music.get_artists_top_track_from_years(
            artists_with_top_10_tracks, year_range=(1980, 1989)
        )

        # Get Top track lyrics
        artist_list = [
            artist for artist in music.get_lyrics_for_song(artists_with_top_80s_track)
        ]

        storage_provider.upsert(artist_list)

    # Get sentiment for each track
    if get_scores:
        song_list = storage_provider.read()
        analytics = AnalyticsProvider()
        scores = [song for song in analytics.get_sentiment(song_list)]

        storage_provider.create(scores)

    # Sort [rank] by sentiment
    scored_song_list = storage_provider.read()

    sorted_list = sorted(
        scored_song_list,
        key=lambda x: (x["score"]["positive"], x["score"]["negative"]),
        reverse=True,
    )

    storage_provider.create(sorted_list)
