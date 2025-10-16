#!/usr/bin/env python3
"""
🦅 EagleFarm - RuCTF HTTP Protocol
"""

import requests
from server.protocols.base import BaseProtocol
from server import config


class RuCTFHTTPProtocol(BaseProtocol):
    """RuCTF HTTP flag submission protocol"""
    
    def submit_flag(self, flag, team):
        """Submit flag via HTTP"""
        try:
            # Prepare request
            headers = {
                'X-Team-Token': config.TEAM_TOKEN
            }
            
            data = {
                'flag': flag
            }
            
            # Submit
            response = requests.put(
                config.SYSTEM_URL,
                json=[flag],
                headers=headers,
                timeout=10
            )
            
            # Parse response
            accepted = response.status_code == 200
            
            return {
                'accepted': accepted,
                'response': response.text[:100]
            }
        
        except Exception as e:
            return {
                'accepted': False,
                'response': f'Error: {str(e)}'
            }