import socket
import numpy as np
from skimage.measure import regionprops, label
import matplotlib.pyplot as plt

host = "84.237.21.36"
port = 5152


def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    beat = b"nope"

    plt.ion()
    plt.figure()

    while beat != b"yep":
        sock.send(b"get")
        bts = recvall(sock, 40002)

        beat = b"nope"

        im1 = np.frombuffer(bts[2:40002], dtype="uint8").reshape(bts[0], bts[1])

        binary = im1 > 0
        labeled = label(binary)
        regions = regionprops(labeled)
        if len(regions) == 2 and regions[0].eccentricity == 0 and regions[1].eccentricity == 0:
            cy1, cx1 = regions[0].centroid
            cy2, cx2 = regions[1].centroid
            result = np.sqrt((cx2 - cx1)**2 + (cy2 - cy1)**2)

            sock.send(f"{result:.1f}".encode())
            print(sock.recv(10))
            sock.send(b"beat")
            beat = sock.recv(10)
            plt.clf()
            plt.imshow(im1)
            plt.pause(1)
