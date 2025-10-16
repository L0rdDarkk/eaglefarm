#!/usr/bin/env python3
"""
🦅 EagleFarm - ForcAD TCP Protocol
"""

import socket
from server.protocols.base import BaseProtocol
from server import config


class ForcADTCPProtocol(BaseProtocol):
    """ForcAD TCP flag submission protocol"""
    
    def submit_flag(self, flag, team):
        """Submit flag via TCP with team token"""
        try:
            # Connect to checksystem
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((config.SYSTEM_HOST, config.SYSTEM_PORT))
            
            # Send team token first
            sock.sendall(f"{config.TEAM_TOKEN}\n".encode())
            
            # Send flag
            sock.sendall(f"{flag}\n".encode())
            
            # Receive response
            response = sock.recv(1024).decode().strip()
            sock.close()
            
            # Parse response
            accepted = 'accepted' in response.lower() or 'ok' in response.lower()
            
            return {
                'accepted': accepted,
                'response': response
            }
        
        except Exception as e:
            return {
                'accepted': False,
                'response': f'Error: {str(e)}'
            }