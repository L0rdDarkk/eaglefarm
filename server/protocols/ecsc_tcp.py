#!/usr/bin/env python3
"""
🦅 EagleFarm - FAUST CTF HTTP Protocol
"""

import requests
from server.protocols.base import BaseProtocol
from server import config


class FAUSTHTTPProtocol(BaseProtocol):
    """FAUST CTF HTTP flag submission protocol"""
    
    def submit_flag(self, flag, team):
        """Submit flag via HTTP to FAUST checksystem"""
        try:
            # FAUST uses POST with team token in header
            headers = {
                'X-Team-Token': config.TEAM_TOKEN
            }
            
            # Send flags as array
            response = requests.post(
                config.SYSTEM_URL,
                json=[flag],
                headers=headers,
                timeout=10
            )
            
            # Parse response
            accepted = response.status_code in [200, 201]
            
            # Get response details
            try:
                result = response.json()
                # FAUST returns status per flag
                if isinstance(result, list) and len(result) > 0:
                    flag_result = result[0]
                    response_text = flag_result.get('msg', str(flag_result))
                else:
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