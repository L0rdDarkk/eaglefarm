#!/usr/bin/env python3
"""
🦅 EagleFarm Protocols
Flag submission protocols for different checksystems
"""

from server import config


def get_protocol(protocol_name):
    """Get protocol instance by name"""
    
    if protocol_name == 'ructf_tcp':
        from server.protocols.ructf_tcp import RuCTFTCPProtocol
        return RuCTFTCPProtocol()
    
    elif protocol_name == 'ructf_http':
        from server.protocols.ructf_http import RuCTFHTTPProtocol
        return RuCTFHTTPProtocol()
    
    elif protocol_name == 'forcad_tcp':
        from server.protocols.forcad_tcp import ForcADTCPProtocol
        return ForcADTCPProtocol()
    
    elif protocol_name == 'ecsc_http':
        from server.protocols.ecsc_http import ECSCHTTPProtocol
        return ECSCHTTPProtocol()
    
    elif protocol_name == 'ecsc_tcp':
        from server.protocols.ecsc_tcp import ECSCTCPProtocol
        return ECSCTCPProtocol()
    
    elif protocol_name == 'faust_http':
        from server.protocols.faust_http import FAUSTHTTPProtocol
        return FAUSTHTTPProtocol()
    
    elif protocol_name == 'faust_tcp':
        from server.protocols.faust_tcp import FAUSTTCPProtocol
        return FAUSTTCPProtocol()
    
    else:
        raise ValueError(f"Unknown protocol: {protocol_name}")