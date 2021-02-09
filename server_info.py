import socket
import time
import config.settings as CFG
from config.logger import logger
from logging import Logger

# Create a logger. Supply a filename, whether or not to 'w'rite or
# 'a'ppend to the log file as well as a debug flag.
log = logger(__name__, CFG.SERVERINFO.FILE_SERVER_LOG, "w", CFG.APP.DEBUG)


class ServerInfo:
    def __init__(
        self,
        servers: list,
        ports: list,
        output_file: str
    ):
        self.__retry = 1
        self.__delay = 1
        self.__timeout = 1
        self.__servers = servers
        self.__ports = ports
        self.__output_file = output_file

        log.debug("ServerInfo initialized.")
        log.debug(f"Server info output file - {self.__output_file}")

    # Returns port availability
    def __isOpen(self, ip: str, port: int) -> bool:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.__timeout)
        port_open = False

        try:
            s.connect((ip, int(port)))
            s.shutdown(socket.SHUT_RDWR)
            port_open = True
        except Exception as e:
            log.debug(f"Error connecting to port {port} at {ip}. Error - {e}")
        finally:
            s.close()
            return port_open

    # Returns whether or not the servers port is open or not.
    def __checkHost(self, ip: str, port: int) -> bool:
        ipup = False
        
        try:
            for i in range(self.__retry):
                if self.__isOpen(ip, port):
                    ipup = True
                    break
                else:
                    time.sleep(self.__delay)
        except Exception as e:
            log.debug(f'Error getting port state.  Error - {e}')
        finally:
            return ipup

    # Returns the IP address of the supplied hostname.
    def __GetServerIP(self, hostname: str) -> str:
        try:
            host_ip = socket.gethostbyname(hostname)
            return host_ip
        except Exception as e:
            log.debug(f"Unable to get IP address\t Error: {e}")
            return ''

    # Check a list of ports on a list of servers and log the the results as
    # well as write the results out to a text file.
    def check_servers(self):

        # Open the output text file to write the results to.
        # This file is used by the other applications.
        with open(self.__output_file, "w") as writer:

            # Loop through the list of servers to check.
            for servername, hostaddress in self.__servers:
                # Get the IP address of the current server
                ip = self.__GetServerIP(hostaddress)

                # This will hold the status of the port being checked
                # on the current server
                port_status = ""

                # Begin building the ouput string that will eventually be
                # written out to the text file. This string contains formatting
                # characters for the discord message.
                status_text = f"**`{servername}:`** {hostaddress}\t**`IP:`** {ip}\t"

                # Loop through the list of ports to check.
                for portname, port in self.__ports:
                    # Check to see if the port is open or not and set
                    # the status flag accordingly.
                    if self.__checkHost(ip, port):
                        port_status = "UP"
                    else:
                        port_status = "~~DOWN~~"

                    # Append the port result to output string.
                    status_text += f" **`{portname}:`** {port_status}\t"

                # log the output string for this server
                log.info(status_text)

                # write the output string to a text file for future use
                writer.write(f"{status_text}\n")

        log.info("Server info check complete.")

if __name__ == "__main__":
    server_info = ServerInfo(
        CFG.SERVERINFO.SERVERS,
        CFG.SERVERINFO.PORTS,
        CFG.SERVERINFO.FILE_DATA
    )

    server_info.check_servers()
