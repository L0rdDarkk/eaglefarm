#!/usr/bin/env python3
"""
🦅 EagleFarm Flag Submitter
Background thread that submits flags to checksystem
"""

import time
import threading
import logging
from server import config
from server.database import get_queued_flags, update_flag_status
from server.protocols import get_protocol

logger = logging.getLogger(__name__)


class FlagSubmitter:
    """Background flag submission thread"""
    
    def __init__(self):
        self.running = False
        self.thread = None
        self.protocol = None
    
    def start(self):
        """Start the submission thread"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._submission_loop, daemon=True)
        self.thread.start()
        logger.info("🦅 Flag submitter started")
    
    def stop(self):
        """Stop the submission thread"""
        self.running = False
        if self.thread:
            self.thread.join()
        logger.info("Flag submitter stopped")
    
    def _submission_loop(self):
        """Main submission loop"""
        while self.running:
            try:
                # Get protocol
                if not self.protocol:
                    self.protocol = get_protocol(config.SYSTEM_PROTOCOL)
                
                # Get flags to submit
                flags = get_queued_flags(limit=config.SUBMIT_FLAG_LIMIT)
                
                if flags:
                    logger.info(f"Submitting {len(flags)} flags...")
                    
                    for flag_row in flags:
                        try:
                            # Submit flag
                            result = self.protocol.submit_flag(
                                flag_row['flag'],
                                flag_row['team']
                            )
                            
                            # Update status
                            if result['accepted']:
                                update_flag_status(
                                    flag_row['id'],
                                    'ACCEPTED',
                                    result.get('response', 'OK')
                                )
                            else:
                                update_flag_status(
                                    flag_row['id'],
                                    'REJECTED',
                                    result.get('response', 'Error')
                                )
                        
                        except Exception as e:
                            logger.error(f"Error submitting flag: {e}")
                            update_flag_status(
                                flag_row['id'],
                                'REJECTED',
                                str(e)
                            )
                
                # Sleep
                time.sleep(config.SUBMIT_PERIOD)
            
            except Exception as e:
                logger.error(f"Error in submission loop: {e}")
                time.sleep(config.SUBMIT_PERIOD)