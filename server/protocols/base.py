#!/usr/bin/env python3
"""
🦅 EagleFarm Base Protocol
Base class for all flag submission protocols
"""

from abc import ABC, abstractmethod


class BaseProtocol(ABC):
    """Base protocol interface"""
    
    @abstractmethod
    def submit_flag(self, flag, team):
        """
        Submit a flag to the checksystem
        
        Args:
            flag: Flag string
            team: Team name/identifier
        
        Returns:
            dict: {'accepted': bool, 'response': str}
        """
        pass
    
    def submit_flags_batch(self, flags):
        """
        Submit multiple flags (default implementation)
        
        Args:
            flags: List of (flag, team) tuples
        
        Returns:
            list: List of results
        """
        results = []
        for flag, team in flags:
            result = self.submit_flag(flag, team)
            results.append(result)
        return results