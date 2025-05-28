from adafruit_httpserver import Request, Response

class srvsetup:
    def on_get(request: Request):
        return Response(request, '<!DOCTYPE html><html><body><h2>Server setup is in config.toml</h2></body></html>', content_type='text/html')

class devsetup:
    def on_get(request: Request, devnum: int):
        return Response(request, '<!DOCTYPE html><html><body><h2>Device setup is in config.toml</h2></body></html>', content_type='text/html')

