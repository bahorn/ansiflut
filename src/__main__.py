import pydle
import sys

class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.canvas = [
            [4 for y in range(self.width)] for x in range(self.height)
        ]

    def dims(self):
        return (self.width, self.height)

    def set(self, x, y, c):
        if c not in range(0, 16):
            return False
        if x < 0 or x > self.width:
            return False
        if y < 0 or y > self.height:
            return False
        self.canvas[y][x] = c
        return True

    def get(self, x, y):
        if x < 0 or x > self.width:
            return 0
        if y < 0 or y > self.height:
            return 0
        return self.canvas[y][x]

help_msg = """SIZE - Returns dimensions as SIZE <w> <h>.
PX - Returns the canvas
PX <x> <y> <c> - Sets the pixel at x,y to c, where c is an ANSI color code"""

# Simple echo bot.
class ANSIFlut(pydle.Client):
    canvas = Canvas(40, 10)
    
    async def on_connect(self):
        await self.join('#ansiflut')

    async def on_message(self, target, source, message):
        # don't respond to our own messages, as this leads to a positive feedback loop
        if source != self.nickname:
            cmd = message.split(' ')
            if cmd[0] == 'PX':
                if len(cmd) == 1:
                    # return the canvas
                    width, height = self.canvas.dims()
                    for y in range(height):
                        line = [
                            bytes(
                                [
                                    0x03,
                                ]
                            ).decode('utf-8') +
                            '{}\u2588'.format(self.canvas.get(x, y))
                            for x in range(width)
                        ]
                        await self.message(
                            target,
                            ''.join(line)
                        )
                            
                elif len(cmd) == 4:
                    # set a pixel
                    print(cmd)
                    try:
                        x = int(cmd[1])
                        y = int(cmd[2])
                        c = int(cmd[3])
                        if not self.canvas.set(x, y, c):
                            await self.message(
                                target,
                                'invalid message, try HELP'
                            )
                    except:
                        print('oof')
                        await self.message(
                            target,
                            'invalid message, try HELP'
                        )

                else:
                    await self.message(
                        target,
                        'invalid message, try HELP'
                    )
            elif cmd[0] == "SIZE":
                width, height = self.canvas.dims()
                await self.message(
                    target,
                    'SIZE {} {}'.format(width, height)
                )
            elif cmd[0] == "HELP":
                await self.message(
                    target,
                    help_msg
                )

if __name__ == "__main__":
    client = ANSIFlut('ansiflut', realname='ansiflut', username='ansiflut')
    client.run(sys.argv[1], tls=True, password=sys.argv[2])
