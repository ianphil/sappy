#!/usr/bin/env python


class Sorter:
    def by_happy(self, scored_artists):
        return sorted(
            scored_artists,
            key=lambda x: (x["score"]["positive"], x["score"]["negative"]),
            reverse=True,
        )

    def by_sad(self, scored_artists):
        return sorted(
            scored_artists,
            key=lambda x: (x["score"]["positive"], x["score"]["negative"]),
            reverse=False,
        )
