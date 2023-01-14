import socket
import requests
import time

UDP_PORT = 2137
API_ADDR = 'http://localhost:8000'

ipByMac = dict()
macByIp = dict()

def startServer():
    devices = getDevices()
    for device in devices:
        mac = device['device_mac']
        ip = device['device_ip']
        ipByMac[mac] = ip
        macByIp[ip] = mac

    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', UDP_PORT))
    localIp = getLocalIp()
    log(f'Listening on {localIp}:{UDP_PORT}')

    sock.settimeout(1)
    while True:
        try:
            msg, (addr, port) = sock.recvfrom(64)
        except TimeoutError:
            # So that the script can be terminated with Ctrl+C
            continue
        except socket.timeout:
            # So that the script can be terminated with Ctrl+C
            continue

        msg = msg.decode('ascii').strip()
        log(msg, addr)

        cmd = msg.split(' ')[0]
        args = msg.split(' ')[1:]

        if cmd == 'FIND_HOST':
            send(f'HOST {localIp}', addr)
        elif cmd == 'ENDPOINT_MAC':
            registerEndpoint(addr, args[0])
        elif cmd == 'CARD':
            onCardRead(addr, args[0])

def getLocalIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    localIp = s.getsockname()[0]
    s.close()
    return localIp

def log(msg, source=None):
    if source is None:
        print(f'\x1b[34;1m{msg}\x1b[0m')
    else:
        print(f'[{source:>15}] {msg}')

def send(msg, ip):
    sock.sendto(msg.encode('ascii'), (ip, UDP_PORT))

def registerEndpoint(remoteIp, mac):
    log(f'Registering endpoint {mac} at {remoteIp}')
    ipByMac[mac] = remoteIp
    macByIp[remoteIp] = mac
    requests.post(f'{API_ADDR}/devices', json={
        'device_mac': mac,
        'device_ip': remoteIp,
        'name': ''
    })

def onCardRead(ip, cardId):
    log(f'Read card {cardId} by {ip}')
    if ip not in macByIp:
        log(f'Reader\'s MAC not found; IP {ip}')
        return
    remoteMac = macByIp[ip]
    doorToOpen = []
    rules = getRules()
    readerFound = False
    for rule in rules:
        if rule['reader_mac'] == remoteMac and rule['card_id'] == cardId:
            doorToOpen.append(rule['door_mac'])
        if rule['reader_mac'] == remoteMac:
            readerFound = True

    if readerFound:
        logRead(cardId, remoteMac, len(doorToOpen) > 0)
    
    for door in doorToOpen:
        if door not in ipByMac:
            log(f'Door\'s IP not found; MAC {door}')
            return
        doorIp = ipByMac[door]
        send('TOGGLE', doorIp)
        log(f'Toggling door at {doorIp}')

def getRules():
    response = requests.get(f'{API_ADDR}/rules')
    parsed = response.json()
    return parsed

def getDevices():
    response = requests.get(f'{API_ADDR}/devices')
    parsed = response.json()
    return parsed

def logRead(cardId, readerMac, success):
    requests.post(f'{API_ADDR}/logs', json={
        'timestamp': int(time.time()),
        'card_id': cardId,
        'reader_mac': readerMac,
        'is_success': 1 if success else 0
    })

startServer()