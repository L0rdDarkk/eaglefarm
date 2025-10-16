#!/usr/bin/env python3
"""
🦅 EagleFarm - Main Flask Application
Team Albania Attack/Defense CTF Platform
"""

import os
import logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime

from server.database import init_db, get_db, get_stats
from server.api import api_bp
from server.submitter import FlagSubmitter
from server import config

# Configure logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/eaglefarm.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize database
init_db()

# Register API blueprint
app.register_blueprint(api_bp, url_prefix='/api')

# Initialize flag submitter
flag_submitter = FlagSubmitter()


@app.route('/')
def index():
    """Main dashboard"""
    stats = get_stats()
    return render_template('index.html', 
                         stats=stats,
                         team_name=config.TEAM_NAME,
                         num_teams=len(config.TEAMS))


@app.route('/flags')
def flags_view():
    """View all flags"""
    db = get_db()
    
    # Get filters
    status = request.args.get('status', '')
    sploit = request.args.get('sploit', '')
    
    query = 'SELECT * FROM flags WHERE 1=1'
    params = []
    
    if status:
        query += ' AND status = ?'
        params.append(status)
    if sploit:
        query += ' AND sploit = ?'
        params.append(sploit)
    
    query += ' ORDER BY time DESC LIMIT 500'
    
    flags = db.execute(query, params).fetchall()
    
    return render_template('flags.html', flags=flags)


@app.route('/exploits')
def exploits_view():
    """Exploit statistics"""
    db = get_db()
    
    exploits = db.execute('''
        SELECT 
            sploit,
            COUNT(*) as total,
            SUM(CASE WHEN status = "ACCEPTED" THEN 1 ELSE 0 END) as accepted,
            SUM(CASE WHEN status = "REJECTED" THEN 1 ELSE 0 END) as rejected,
            SUM(CASE WHEN status = "QUEUED" THEN 1 ELSE 0 END) as queued
        FROM flags
        GROUP BY sploit
        ORDER BY accepted DESC
    ''').fetchall()
    
    return render_template('exploits.html', exploits=exploits)


@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'eaglefarm',
        'team': 'albania',
        'timestamp': datetime.utcnow().isoformat()
    })


if __name__ == '__main__':
    logger.info('🦅 Starting EagleFarm Server...')
    logger.info(f'Team: {config.TEAM_NAME}')
    logger.info(f'Teams configured: {len(config.TEAMS)}')
    
    # Start flag submitter
    flag_submitter.start()
    
    app.run(host='0.0.0.0', port=5000, debug=config.DEBUG)