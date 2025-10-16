#!/usr/bin/env python3
"""
🦅 EagleFarm - ECSC HTTP Protocol
European Cybersecurity Challenge
"""

import requests
from server.protocols.base import BaseProtocol
from server import config


class ECSCHTTPProtocol(BaseProtocol):
    """ECSC HTTP flag submission protocol"""
    
    def submit_flag(self, flag, team):
        """Submit flag via HTTP to ECSC checksystem"""
        try:
            # ECSC typically uses HTTP PUT/POST with team token
            headers = {
                'X-Team-Token': config.TEAM_TOKEN,
                'Content-Type': 'application/json'
            }
            
            # Send as JSON array
            response = requests.put(
                config.SYSTEM_URL,
                json=[flag],
                headers=headers,
                timeout=10
            )
            
            # Parse response
            # ECSC usually returns 200 for accepted flags
            accepted = response.status_code == 200
            
            # Try to get detailed response
            try:
                result = response.json()
                response_text = str(result)
            except:
                response_text = response.text[:100]
            
            return {
                'accepted': accepted,
                'response': response_text
            }
        
        except Exception as e:
            return {
                'accepted': False,
                'response': f'Error: {str(e)}'
            }