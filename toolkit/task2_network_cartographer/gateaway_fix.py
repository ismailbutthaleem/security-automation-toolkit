import socket
import subprocess
import time

TARGET = "172.16.19.101"
PORT = 21
SSH_USER = "vagrant"


def ftp_command_response(target: str, port: int, command: str):
    """Connect to the Ftp port, send a single command, return the response.
    Used to verify behaviour before and after the remediation
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:

        sock.settimeout(5)
        sock.connect((target, port))
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
    return response.startswith("350")


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
        banner: str = sock.recv(1024).decode("utf-8", errors="ignore").strip()
        print(f"    [*] FTP banner: {banner}")
        return "ProFTPD" in banner
    except Exception as e:
        print(f"    [-] FTP unreachable: {e}")
        return False
    finally:
        sock.close()


def test_ftp_reachable(target: str, port: int) -> bool:
    """
    Attempt FTP connection. Returns True if reachable, False if blocked.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.settimeout(3)
        sock.connect((target, port))
        time.sleep(0.1)
        banner: str = sock.recv(1024).decode("utf-8", errors="ignore").strip()
        print(f"    [*] FTP banner: {banner}")
        return True
    except Exception:
        return False
    finally:
        sock.close()


def test_cpfr(target: str, port: int) -> bool:
    """
    Test whether SITE CPFR returns 350 (vulnerable) or fails (remediated).
    Returns True if vulnerable, False if blocked or unreachable.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.settimeout(3)
        sock.connect((target, port))
        time.sleep(0.1)
        sock.recv(1024)  # discard banner
        sock.send(b"SITE CPFR /etc/passwd\r\n")
        time.sleep(0.1)
        response: str = sock.recv(1024).decode("utf-8", errors="ignore").strip()
        print(f"    [*] SITE CPFR response: {response}")
        return response.startswith("350")
    except Exception as e:
        print(f"    [*] Connection failed: {e}")
        return False
    finally:
        sock.close()


def apply_iptables_block(target: str) -> bool:
    """
    Uses INPUT chain DROP rule — immediate effect, no restart required.
    """
    print("    [*] Applying iptables block via SSH...")

    cmd: str = (
        f"ssh -o StrictHostKeyChecking=no "
        f"-o ConnectTimeout=10 "
        f"{SSH_USER}@{target} "
        f'"sudo iptables -I INPUT 1 -p tcp --dport {PORT} -j DROP"'
    )

    result: subprocess.CompletedProcess[str] = subprocess.run(
        cmd, shell=True, capture_output=True, text=True
    )

    if result.returncode != 0:
        print(f"    [-] iptables command failed: {result.stderr.strip()}")
        return False

    return True


def verify_rule_present(target: str) -> bool:
    """
    Confirm the iptables DROP rule is present on the target.
    """
    cmd: str = (
        f"ssh -o StrictHostKeyChecking=no "
        f"-o ConnectTimeout=10 "
        f"{SSH_USER}@{target} "
        f"\"sudo iptables -L INPUT -n | grep 'dpt:{PORT}'\""
    )

    result: subprocess.CompletedProcess[str] = subprocess.run(
        cmd, shell=True, capture_output=True, text=True
    )

    if result.returncode == 0 and result.stdout.strip():
        print(f"    [*] Rule confirmed: {result.stdout.strip()}")
        return True

    return False


def main() -> None:
    print("[*] fix_proftpd.py — CVE-2015-3306 Remediation")
    print(f"[*] Target: {TARGET}:{PORT}")
    print()

    # Step 1: Confirm vulnerability is present before fixing
    print("[1] Pre-fix verification — confirming vulnerability...")
    if not test_cpfr(TARGET, PORT):
        print("    [*] SITE CPFR returned non-350. May already be fixed.")
    else:
        print("    [!] Vulnerable — mod_copy responds to CPFR")
    print()

    # Step 2: Apply iptables block
    print("[2] Applying remediation...")
    if not apply_iptables_block(TARGET):
        print("    [-] Remediation failed. Check SSH access and sudo permissions.")
        return
    print("    [+] Firewall rule inserted.")
    print()

    # Step 3: Verify the rule exists
    print("[3] Verifying firewall rule is present...")
    if verify_rule_present(TARGET):
        print("    [+] DROP rule confirmed in INPUT chain.")
    else:
        print("    [-] Could not confirm firewall rule.")
        return
    print()

    # Step 4: Verify FTP is blocked
    print("[4] Verifying FTP is blocked...")
    if test_ftp_reachable(TARGET, PORT):
        print("    [-] FTP still reachable. Remediation failed.")
        return
    else:
        print("    [+] FTP no longer reachable on port 21.")
        print()
        print("[+] Remediation complete.")
        print("    Vulnerability exposure reduced: FTP access blocked externally")
        print("    Service state: Port 21 filtered by firewall")


if __name__ == "__main__":
    main()
