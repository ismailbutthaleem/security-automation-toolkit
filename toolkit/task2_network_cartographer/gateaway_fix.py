
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
        sock.connect((target,port))
        time.sleep(0.1)
        sock.recv(1024)
        sock.send(f"{command}\r\n".encode()) 
        return sock.recv(1024).decode("utf-8", errors="ignore").strip()
    except Exception as e:
        return f"Error: {e}"
    finally:
        sock.close()
   
   def verify_vulnerable(target: str, port: int) -> bool:
    """
    Check whether mod_copy responds to SITE CPFR.
    Returns True if vulnerable (350 response), False if remediated (500).
    """
    response: str = ftp_command_response(target, port, "SITE CPFR /etc/passwd")
    print(f"    [*] SITE CPFR response: {response}")
    return response.startswith('350')


def verify_ftp_alive(target: str, port: int) -> bool:
    """
    Confirm FTP service is still responding after remediation.
    Returns True if banner received, False otherwise.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.settimeout(5)
        sock.connect((target, port))
        time.sleep(0.1)
        banner: str = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        print(f"    [*] FTP banner: {banner}")
        return 'ProFTPD' in banner
    except Exception as e:
        print(f"    [-] FTP unreachable: {e}")
        return False
    finally:
        sock.close()