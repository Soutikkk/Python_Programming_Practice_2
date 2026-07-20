import time
import pywifi


def get_signal_quality(signal_strength):
    """Return a human-readable Wi-Fi signal quality."""
    if signal_strength > -50:
        return "Excellent"
    elif signal_strength > -65:
        return "Good"
    elif signal_strength > -75:
        return "Average"
    else:
        return "Weak"


def scan_wifi():
    wifi = pywifi.PyWiFi()
    interfaces = wifi.interfaces()

    if not interfaces:
        print("No Wi-Fi adapter found.")
        return

    iface = interfaces[0]

    print("Scanning for Wi-Fi networks...\n")
    iface.scan()
    time.sleep(3)

    networks = iface.scan_results()

    if not networks:
        print("No Wi-Fi networks found.")
        return

    # Remove duplicate SSIDs (optional)
    seen = set()

    for network in networks:
        if network.ssid in seen:
            continue
        seen.add(network.ssid)

        quality = get_signal_quality(network.signal)

        print(
            f"SSID   : {network.ssid or '<Hidden Network>'}\n"
            f"Signal : {network.signal} dBm\n"
            f"Quality: {quality}\n"
            f"{'-' * 30}"
        )


if __name__ == "__main__":
    scan_wifi()
