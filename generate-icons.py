#!/usr/bin/env python3
"""Generates BJJ Flow app icons as PNG files (no dependencies)."""
import struct, zlib, math

def build_png(size, pixels):
    def chunk(name, data):
        crc = zlib.crc32(name + data) & 0xffffffff
        return struct.pack('>I', len(data)) + name + data + struct.pack('>I', crc)

    raw = b''
    for y in range(size):
        raw += b'\x00'
        for x in range(size):
            raw += bytes(pixels[y * size + x])

    ihdr = struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0)
    return (
        b'\x89PNG\r\n\x1a\n'
        + chunk(b'IHDR', ihdr)
        + chunk(b'IDAT', zlib.compress(raw, 9))
        + chunk(b'IEND', b'')
    )

def render_icon(size):
    BG   = (15, 17, 23)
    GOLD = (201, 168, 76)

    cx, cy  = (size - 1) / 2.0, (size - 1) / 2.0
    outer_r = size * 0.43
    inner_r = size * 0.31
    sqrt3   = math.sqrt(3)

    def in_flat_hex(px, py, r):
        x, y = abs(px - cx), abs(py - cy)
        return y <= r * sqrt3 / 2 and sqrt3 * x + y <= r * sqrt3

    SS = 4
    pixels = []
    for y in range(size):
        for x in range(size):
            hits = sum(
                1 for sy in range(SS) for sx in range(SS)
                if in_flat_hex(x + (sx + .5) / SS, y + (sy + .5) / SS, outer_r)
                and not in_flat_hex(x + (sx + .5) / SS, y + (sy + .5) / SS, inner_r)
            )
            t = hits / (SS * SS)
            pixels.append(tuple(int(BG[i] * (1 - t) + GOLD[i] * t) for i in range(3)))

    return build_png(size, pixels)

for size, fname in [(512, 'icon-512.png'), (192, 'icon-192.png'), (180, 'apple-touch-icon.png')]:
    data = render_icon(size)
    with open(fname, 'wb') as f:
        f.write(data)
    print(f'  {fname}  ({size}x{size}, {len(data):,} bytes)')

print('Done.')
