import toml
import adafruit_logging as logging

_dict = {}
with open("config.toml", "r") as f:
    _dict = toml.load(f)

def get_toml(sect: str, item: str):
    setting = ''
    s = None
    try:
        setting = _dict[sect][item]
    except:
        setting = ''
    return setting

def get_log_level():
    logLevelString = get_toml('logging', 'log_level')
    for level in logging.LEVELS:
        if (level[1] == logLevelString):
            return level[0]
        
    return 0

class Config:
    # ---------------
    # Network Section
    # ---------------
    ip_address: str = get_toml('network', 'ip_address')
    port: int = get_toml('network', 'port')
    wifi_ssid: str = get_toml('network', 'wifi_ssid')
    wifi_password: str = get_toml('network', 'wifi_password')
    ap_ssid: str = get_toml('network', 'ap_ssid')
    ap_password: str = get_toml('network', 'ap_password')
    # --------------
    # Server Section
    # --------------
    location: str = get_toml('server', 'location')
    verbose_driver_exceptions: bool = get_toml('server', 'verbose_driver_exceptions')
    # --------------
    # Device Section
    # --------------
    can_reverse: bool = get_toml('device', 'can_reverse')
    step_size: float = get_toml('device', 'step_size')
    steps_per_sec: int = get_toml('device', 'steps_per_sec')
    sync_write_connected: bool = get_toml('device', 'sync_write_connected')
    # ---------------
    # Logging Section
    # ---------------
    
    
    
    log_level: int = get_log_level()
    log_to_stdout: str = get_toml('logging', 'log_to_stdout')
    max_size_mb: int = get_toml('logging', 'max_size_mb')
    num_keep_logs: int = get_toml('logging', 'num_keep_logs')
