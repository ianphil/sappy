#!/usr/bin/env python
from os import getenv

import constants


def get_spotify_client_info():
    return {
        constants.SPOTIFY_CLIENT_ID: getenv(constants.SPOTIFY_CLIENT_ID),
        constants.SPOTIFY_CLIENT_SECRET: getenv(constants.SPOTIFY_CLIENT_SECRET),
    }


if __name__ == "__main__":
    spotify_creds = get_spotify_client_info()
    print(
        (
            f"The {constants.SPOTIFY_CLIENT_ID} is "
            f"{spotify_creds[constants.SPOTIFY_CLIENT_ID]}"
        )
    )
