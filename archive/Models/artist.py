class Artist:
    def __init__(self):
        self.artist_id = None
        self.album_list = None
        self.name = None
        self.type = "Artist"
        self.spotify_id = None
        self.spotify_url = None
        self.spotify_external_url = None
        self.spotify_image_url = None
        self.spotify_popularity = None
        self.spotify_followers = None
        self.spotify_genres = None

    def ctor_from_dict(self, **entries):
        self.__dict__.update(entries)
