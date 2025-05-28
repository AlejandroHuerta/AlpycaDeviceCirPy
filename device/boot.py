import board
import digitalio
import storage

switch = digitalio.DigitalInOut(board.D6)

switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.DOWN

print(f'The storage switch GPIO6 is {switch.value}')

# If the switch pin is connected to ground CircuitPython can write to the drive
# storage.remount("/", readonly=switch.value)
