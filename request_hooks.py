from flask import request


def add_missing_slash() -> None:
    print(request.url)
    if request.url[-1] == '/':
        print(request.url[:-1])
