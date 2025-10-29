import logging as log

log.basicConfig(
    level = log.DEBUG,
    format = "%(levelname)s | @ %(asctime)s | %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S",
    handlers = [
        log.FileHandler("app.log"),
        log.StreamHandler()
    ]
)

