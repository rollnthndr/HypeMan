import socket
import select
import string
import sys
import time
import pathlib
from config.config import APP_CONFIG
import logging
from logging import config

# set up the global logger at logging level set in app_settings.ini
logging.config.fileConfig(
    pathlib.Path(APP_CONFIG["app"]["logging_config"]), disable_existing_loggers=True,
)
if APP_CONFIG["app"]["debugging"].lower() == "true":
    logger = logging.getLogger("debug")
else:
    logger = logging.getLogger("info")


SERVERS = [
		    ['JOW East', 'jow2.aggressors.ca'],
		   	['JOW West', 'jow.aggressors.ca'],
		   	['Local', '127.0.0.1']
		]


class ServerInfo:
	def __init__(self, servers):
		self.__retry = 1
		self.__delay = 1
		self.__timeout = 1
		self.__servers = servers

		logger.debug("ServerInfo initialized.")

	def __isOpen(self, ip, port) -> bool:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(self.__timeout)
		try:
			s.connect((ip, int(port)))
			s.shutdown(socket.SHUT_RDWR)
			return True
		except:
			return False
		finally:
			s.close()

	def __checkHost(self, ip, port) -> bool:
		ipup = False
		for i in range(self.__retry):
			if self.__isOpen(ip, port):
				ipup = True
				break
			else:
				time.sleep(self.__delay)
				
		return ipup  

	def __GetServerIP(self, hostname) -> str: 
		try:         
			host_ip = socket.gethostbyname(hostname) 
			return host_ip
		except: 
			return "Unable to get IP address" 


	def check_servers(self):
		logger.info("Checking server info.")

		for servername, hostaddress in self.__servers:
			serverIP = self.__GetServerIP(hostaddress)
			dcsStatus = "DOWN"
			srsStatus = "DOWN"
			LotATCStatus = "DOWN"	
			if self.__checkHost(hostaddress, 10308):
				dcsStatus = "UP"
				
			if self.__checkHost(hostaddress, 5002):
				srsStatus = "UP"
				
			if self.__checkHost(hostaddress, 10310):
				LotATCStatus = "UP"
				
			logger.debug(servername + ", hostname: " + hostaddress + ", ip: " + serverIP + ", DCS: " + dcsStatus + ", SRS: " + srsStatus + ", LotATC: " + LotATCStatus)
		
if __name__ == "__main__":
	

	server_info = ServerInfo(SERVERS)

	server_info.check_servers()

	# for server_name, server_address in SERVERS:
	# 	server_info.doHost(server_name, server_address)
	
