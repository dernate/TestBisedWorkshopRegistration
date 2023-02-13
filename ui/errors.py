#!/usr/bin/env python3


class ErrWebTest:
    def __init__(self, error: bool = False, errortext: str = ""):
        self.error = error
        self.errortext = errortext
