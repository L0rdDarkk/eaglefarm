#!/usr/bin/env python3
"""
🦅 EagleFarm Configuration
Team Albania CTF Settings

EDIT THIS FILE before the competition starts!
"""

# ============================================================================
# TEAM CONFIGURATION
# ============================================================================

TEAM_NAME = "Team Albania 🇦🇱"

# Teams - Get from CTF organizers during competition
TEAMS = {
    'Team #1': '10.60.1.2',
    'Team #2': '10.60.2.2',
    'Team #3': '10.60.3.2',
    # Add more teams here...
}

# Flag format (regex) - Get from organizers
# Examples:
#   RuCTF: r'[A-Z0-9]{31}='
#   ECSC: r'ECSC\{[a-zA-Z0-9_]{32}\}'
FLAG_FORMAT = r'[A-Z0-9]{31}='


# ============================================================================
# CHECKSYSTEM CONFIGURATION
# ============================================================================

# Protocol: 'ructf_http', 'ructf_tcp', 'forcad_tcp'
SYSTEM_PROTOCOL = 'ructf_tcp'

# Checksystem address
SYSTEM_HOST = '10.10.10.10'
SYSTEM_PORT = 31337

# For HTTP protocols
SYSTEM_URL = 'http://10.10.10.10/flags'
TEAM_TOKEN = 'your_team_token'


# ============================================================================
# SUBMISSION SETTINGS
# ============================================================================

SUBMIT_PERIOD = 5           # Submit every N seconds
SUBMIT_FLAG_LIMIT = 50      # Max flags per submission
FLAG_LIFETIME = 5 * 60      # 5 minutes


# ============================================================================
# SERVER SETTINGS
# ============================================================================

SERVER_PASSWORD = '1234'    # Change this!
DEBUG = False
DATABASE_PATH = 'data/flags.db'


# ============================================================================
# FUNCTIONS
# ============================================================================

def get_public_config():
    """Config safe to send to clients"""
    return {
        'TEAMS': TEAMS,
        'FLAG_FORMAT': FLAG_FORMAT,
        'TEAM_NAME': TEAM_NAME
    }