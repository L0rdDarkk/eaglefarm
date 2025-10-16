#!/usr/bin/env python3
"""
🦅 EagleFarm API
Compatible with DestructiveFarm's start_sploit.py client
"""

from flask import Blueprint, request, jsonify
import logging
from server import config
from server.database import add_flags, get_stats

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)


@api_bp.route('/get_config', methods=['GET'])
def get_config():
    """
    API endpoint for clients to get configuration
    Compatible with DestructiveFarm client
    """
    return jsonify(config.get_public_config())


@api_bp.route('/post_flags', methods=['POST'])
def post_flags():
    """
    API endpoint for clients to submit flags
    Compatible with DestructiveFarm client
    
    Expected format:
    [
        {"flag": "FLAG123", "sploit": "exploit.py", "team": "Team #1"},
        ...
    ]
    """
    try:
        flags_data = request.get_json()
        
        if not isinstance(flags_data, list):
            return jsonify({'error': 'Expected list of flags'}), 400
        
        # Validate data
        for item in flags_data:
            if not all(k in item for k in ['flag', 'sploit', 'team']):
                return jsonify({'error': 'Missing required fields'}), 400
        
        # Add to database
        added = add_flags(flags_data)
        
        logger.info(f"Received {len(flags_data)} flags, added {added} new flags")
        
        return jsonify({
            'status': 'ok',
            'received': len(flags_data),
            'added': added
        })
    
    except Exception as e:
        logger.error(f"Error posting flags: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/stats', methods=['GET'])
def stats():
    """Get current statistics"""
    try:
        stats_data = get_stats()
        return jsonify(stats_data)
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': str(e)}), 500