def whatismyos():
    from struct import unpack
    try:
        unpack('L', bytes([0] * 4))
        return 'Windows'
    except:
        return 'Linux'


print(whatismyos())
