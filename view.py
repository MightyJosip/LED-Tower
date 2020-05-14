import pyaudio
import struct
import math
import pygame
import numpy as np


# https://stackoverflow.com/questions/26573556/record-speakers-output-with-pyaudio


BLACK = pygame.Color('lightgray')
WHITE = (0, 0, 0)
color_values = [254, 254, 254, 254, 254, 253, 253, 252, 252, 251, 250, 249, 248, 247, 245, 243, 240, 237, 234, 230, 225,
                219, 212, 205, 196, 186, 176, 165, 153, 140, 128, 115, 102, 90, 79, 69, 59, 50, 43, 36, 30, 25, 21, 18,
                15, 12, 10, 8, 7, 6, 5, 4, 3, 3, 2, 2, 1, 1, 1, 1]
FPS = 60

ledice = 60
ispunjeno = 0

pygame.init()
pygame.key.set_repeat(500, 250)

size = (200, 1000)
screen = pygame.display.set_mode(size)

def sigmoid(x):
    return 1/(1 + pow(x/(1-x), -2.5)) if x != 1 and x/(1-x) != 0 else 1


pygame.display.set_caption("LED Tower")


def rms(data):
    count = len(data)/2
    format = "%dh" % (count)
    shorts = struct.unpack(format, data)
    sum_squares = 0.0
    for sample in shorts:
        n = sample * (1.0/32768)
        sum_squares += n*n
    try:
        rezultat = math.sqrt(sum_squares / count)
    except ZeroDivisionError:
        rezultat = 0
    return rezultat


def select_input_device():
    rezultat = False
    num_of_devices = p.get_device_count()
    output_device = p.get_default_output_device_info()
    for i in range(0, num_of_devices):
        device = p.get_device_info_by_index(i)
        is_wasap = (p.get_host_api_info_by_index(device["hostApi"])["name"]).find("WASAPI") != -1
        if is_wasap and output_device['name'] in device['name']:
            rezultat = p.get_device_info_by_index(i)['index']
    return rezultat


def draw_text(surf, text, size_of_text, x, y):
    font = pygame.font.Font(pygame.font.match_font('arial'), size_of_text)
    text_surface: pygame.Surface = font.render(text, True, WHITE)
    text_rect: pygame.Rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


device_info = {}
p = pyaudio.PyAudio()

device_index = select_input_device()
try:
    device_info = p.get_device_info_by_index(device_index)
except IOError:
    default_device = -1

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = device_info["maxOutputChannels"]
RATE = int(device_info["defaultSampleRate"])
DEVICE_INDEX = device_index


MULTIPLIER = 3.5

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=DEVICE_INDEX,
                as_loopback=True)


clock = pygame.time.Clock()

done = False
ticks = 0
max_amp = 0

def invert(a, b):
    return (b, a)

while not done:
    pygame.display.set_caption(str(clock.get_fps()))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                MULTIPLIER = round(MULTIPLIER + 0.1, 1)
            elif event.key == pygame.K_DOWN:
                MULTIPLIER = round(MULTIPLIER - 0.1, 1)
    data = stream.read(CHUNK)

    screen.fill(BLACK)

    percent = rms(data)*MULTIPLIER
    if percent > 1:
        percent = 1
    ispunjeno = int(round(ledice * percent))


    # COLOR PART:

    for i in range(ledice):
        pygame.draw.circle(screen, WHITE, (100, 10 + 16 * i), 8, 1)
    for i in range(ispunjeno):
        pygame.draw.circle(screen, (color_values[ledice-i-1], color_values[i], 0),
                           (100, (10 + 16 * (ledice - 1)) - 16 * i), 8)

    '''for i in range(ledice):
        pygame.draw.circle(screen, WHITE, (100, 10 + 16 * i), 8, 1)
    for i in range(ispunjeno // 4):
        pygame.draw.circle(screen, (color_values[(ledice-i*4-1)], color_values[i*4], 0),
                           (100, (10 + 16 * (ledice - 15)) + 16 * i), 8)
        pygame.draw.circle(screen, (color_values[(ledice-i*4-1)], color_values[i*4], 0),
                           (100, (10 + 16 * (ledice - 16)) - 16 * i), 8)

        pygame.draw.circle(screen, (color_values[(ledice-i*4-1)], color_values[i*4], 0),
                           (100, (10 + 16 * (ledice - 45)) + 16 * i), 8)
        pygame.draw.circle(screen, (color_values[(ledice-i*4-1)], color_values[i*4], 0),
                           (100, (10 + 16 * (ledice - 46)) - 16 * i), 8)'''
    '''for i in range(ledice):
        pygame.draw.circle(screen, WHITE, invert(35, 10 + 16 * i), 8, 1)
    for i in range(ispunjeno // 4):
        pygame.draw.circle(screen, (color_values[(ledice-i*4-1)], color_values[i*4], 0),
                           invert(35, (10 + 16 * (ledice - 15)) + 16 * i), 8)
        pygame.draw.circle(screen, (color_values[(ledice-i*4-1)], color_values[i*4], 0),
                           invert(35, (10 + 16 * (ledice - 16)) - 16 * i), 8)

        pygame.draw.circle(screen, (color_values[(ledice-i*4-1)], color_values[i*4], 0),
                           invert(35, (10 + 16 * (ledice - 45)) + 16 * i), 8)
        pygame.draw.circle(screen, (color_values[(ledice-i*4-1)], color_values[i*4], 0),
                           invert(35, (10 + 16 * (ledice - 46)) - 16 * i), 8)'''


    #pygame.draw.rect(screen, (255, 0, 0), (0, (1-percent) * size[1] + 1, 200, size[1] - (1-percent) * 800 + 1), 0)
    #pygame.draw.rect()

    '''max_amp = max(int(max_amp - 0.33 * (max_amp - int(1000 * percent))), int(1000 * percent))
    for i in range(int(1000 * percent)):
        s = sigmoid(i/1000)
        pygame.draw.line(screen, (255 * s, 255 * (1 - s), 0), (0, 1000-i), (200, 1000 - i), 1)
    for j in range(10):
        s = sigmoid((max_amp + j) / 1000) if max_amp + j < 1000 else 1
        pygame.draw.line(screen, (255 * s, 255 * (1 - s), 0), (0, 1000 - max_amp + j), (200, 1000 - max_amp + j), 1)'''
    draw_text(screen, str(MULTIPLIER), 18, 20, 5)

    pygame.display.flip()

    clock.tick(FPS)

stream.stop_stream()
stream.close()

p.terminate()

