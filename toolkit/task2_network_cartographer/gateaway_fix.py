
import subprocess
import socket
import time

TARGET = "172.16.19.101"
PORT= 21

def ftp_command_response(target: str, port:int, command: str):
    """ Connect to the Ftp port, send a single command, return the response.
    Used to verify behaviour before and after the remediation
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:

        sock.settimeout(5)
        sock.connect(target,port)
        time.sleep(0.1)
        sock.recv(1024)
        sock.send(f"{command}\r\n".encode()) 
        return sock.recv(1024).decode("utf-8", errors="ignore").strip()
    except Exception as e:
        return f"Error: {e}"
    finally:
        sock.close()
   