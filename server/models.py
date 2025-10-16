#!/usr/bin/env python3
"""
🦅 EagleFarm Models
Data models and validators
"""

import re
from server import config


class Flag:
    """Flag model"""
    
    def __init__(self, flag, sploit, team):
        self.flag = flag
        self.sploit = sploit
        self.team = team
    
    def is_valid(self):
        """Check if flag matches the format"""
        pattern = re.compile(config.FLAG_FORMAT)
        return bool(pattern.match(self.flag))
    
    def to_dict(self):
        return {
            'flag': self.flag,
            'sploit': self.sploit,
            'team': self.team
        }


def validate_flag_format(flag_string):
    """Validate flag against configured format"""
    pattern = re.compile(config.FLAG_FORMAT)
    return bool(pattern.match(flag_string))


def extract_flags_from_text(text):
    """Extract all flags from text using regex"""
    pattern = re.compile(config.FLAG_FORMAT)
    return pattern.findall(text)