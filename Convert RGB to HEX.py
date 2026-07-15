import webcolors

def rgb_to_hex(r, g, b):
    return "#{:02X}{:02X}{:02X}".format(r, g, b)

color = input("Enter a color name: ")

try:
    rgb = webcolors.name_to_rgb(color)

    hex_code = rgb_to_hex(rgb.red, rgb.green, rgb.blue)

    print("RGB:", rgb)
    print("HEX:", hex_code)

except ValueError:
    print("Color not found!")