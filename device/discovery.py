from adafruit_logging import Logger
import asyncio
from socketpool import SocketPool
import select

logger: Logger = None

class DiscoveryResponder:
    def handle_client(self):
        data = bytearray(128)
        size, address = self.sock.recvfrom_into(data)
        dataascii = data.decode('ascii')
        logger.debug(f'Disc rcv {dataascii}')
        if 'alpacadiscovery1' in dataascii:
            self.sock.sendto(self.alpaca_response.encode(), address)
    
    def __init__(self, ADDR, PORT):
        self.device_address = ('', 32227)
        self.alpaca_response  = "{\"AlpacaPort\": " + str(PORT) + "}"
            
        
    async def run(self, socket_pool: SocketPool):
        self.sock = socket_pool.socket(socket_pool.AF_INET, socket_pool.SOCK_DGRAM)
        self.sock.setsockopt(SocketPool.SOL_SOCKET, SocketPool.SO_REUSEADDR, 1)
        self.sock.bind(self.device_address)
        
        poller = select.poll()
        poller.register(self.sock, select.POLLIN)
        
        while True:
            evts = poller.poll(0)
            for _sock, evt in evts:
                logger.debug('Evt received')
                if evt and select.POLLIN:
                    logger.debug('Broadcast received')
                    self.handle_client()
                    
            await asyncio.sleep(0.1)
