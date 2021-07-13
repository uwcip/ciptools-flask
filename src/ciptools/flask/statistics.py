from flask import Flask
from statsd import StatsClient


class StatsD(object):
    def __init__(self, app: Flask = None, config: dict = None):
        self.app = None
        self.statsd = None

        if app is not None:
            self.init_app(app, config)

    def init_app(self, app: Flask = None, config: dict = None):
        self.app = app

        if config is None:
            config = {}

        config.setdefault("STATSD_HOST", "localhost")
        config.setdefault("STATSD_PORT", 8125)
        config.setdefault("STATSD_PREFIX", None)

        self.statsd = StatsClient(
            host=config["STATSD_HOST"],
            port=config["STATSD_PORT"],
            prefix=config["STATSD_PREFIX"],
        )

    def timer(self, *args, **kwargs):
        return self.statsd.timer(*args, **kwargs)

    def timing(self, *args, **kwargs):
        return self.statsd.timing(*args, **kwargs)

    def incr(self, *args, **kwargs):
        return self.statsd.incr(*args, **kwargs)

    def decr(self, *args, **kwargs):
        return self.statsd.decr(*args, **kwargs)

    def gauge(self, *args, **kwargs):
        return self.statsd.gauge(*args, **kwargs)
