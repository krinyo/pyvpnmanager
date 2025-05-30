import uuid

def generate_vless_string(key, domain="192.168.0.20", port=443):
    return f"vless://{key}@{domain}:{port}?security=xtls&flow=xtls-rprx-direct#VPN-User"