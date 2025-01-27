import board
import neopixel

pixels = neopixel.NeoPixel(board.D21, 9, pixel_order=neopixel.RGB)

pixels.fill((255, 0, 0))
pixels.show()