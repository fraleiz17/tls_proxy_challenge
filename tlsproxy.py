"""
This script will create threads, one to listen TCP requests, and one to listen UDP requests.
It will send both kind of requests to Cloudflare over TLS
"""

from io import open_code
import socket
import threading
import ssl
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def send_tcp(query, req_type):
    """Creates connection to Cloudflare"""
    try:
        server = ('1.1.1.1', 853)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_socket = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1_2)
        # ssl_socket = ssl.create_default_context().wrap_socket(sock, server_hostname=server )
        ssl_socket.connect(server)
        if req_type == 'udp':
            logger.info('Processing UDP request...')
            ssl_socket.send(b"\x00" + bytes(chr(len(query)), encoding='utf-8') + query)
        else:
            logger.info('Processing TCP request...')
            ssl_socket.send(query)
        data = ssl_socket.recv(1024)
        return data
    except socket.error as se:
        logger.error('Error reaching backend server... ', str(se))


def udp_listen(conn):
    """Listen for connection from UDP"""
    while True:
        data, addr = conn.recvfrom(1024)
        if len(data) != 0:
            logger.info("UDP recv: %s" % data)
        ret = send_tcp(data, 'udp')
        if ret:
            udp_answer = ret[2:]
            conn.sendto(udp_answer, addr)
        else:
            logger.error("Not a valid DNS query...")


def tcp_listen(sock):
    """Listen for connection from TCP"""
    while True:
        open_con, _ = sock.accept()
        try:
            data = open_con.recv(1024)
            req = send_tcp(data, 'tcp')
            logger.info("TCP recv: %s" % data)
            if req:
                open_con.send(req)
                open_con.close()
            else:
                logger.error("Not a valid DNS query...")
            if len(data) == 0:
                break
        except TypeError:
            pass
        try:
            open_con.close()
        except TypeError:
            pass


def main():
    """This main function will create the sockets to listen UDP and TCP requests"""
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address_tcp = ('0.0.0.0', 1010)
        server_address_udp = ('0.0.0.0', 1010)
        tcp_socket.bind(server_address_tcp)
        udp_socket.bind(server_address_udp)
        tcp_socket.listen(20)
        t1 = threading.Thread(target=tcp_listen, args=(tcp_socket,))
        t2 = threading.Thread(target=udp_listen, args=(udp_socket,))
        logger.info('Listening requests...')
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    except socket.error as e:
        logger.error(str(e))
        tcp_socket.close()
        udp_socket.close()


if __name__ == '__main__':
    try:
        logger.info('Initializing....')
        main()
    except socket.error as e:
        logger.info('Something failed')
        logger.error(str(e))
