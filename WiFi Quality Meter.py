import pywifi
import time

wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]

iface.scan()
time.sleep(3)

for network in iface.scan_results():

    if network.signal > -50:
        quality = "Excellent"

    elif network.signal > -65:
        quality = "Good"

    elif network.signal > -75:
        quality = "Average"

    else:
        quality = "Weak"

    print(f"{network.ssid} -> {quality}")