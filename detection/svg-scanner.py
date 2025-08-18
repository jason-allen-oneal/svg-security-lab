#!/usr/bin/env python3
"""
SVG Security Scanner - Educational Tool

This script scans SVG files for potential security vulnerabilities and malicious content.
It's designed for educational purposes to help understand SVG-based attack vectors.

⚠️ WARNING: This tool is for educational purposes only. Use responsibly.

Author: SVG Security Lab
License: MIT
"""

import re
import sys
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Tuple
import base64
import urllib.parse

class SVGSecurityScanner:
    """Scanner for detecting malicious content in SVG files."""
    
    def __init__(self):
        self.threats = {
            'script_tags': {
                'pattern': r'<script[^>]*>.*?</script>',
                'severity': 'HIGH',
                'description': 'Script tags can execute arbitrary JavaScript'
            },
            'event_handlers': {
                'pattern': r'on\w+\s*=\s*["\'][^"\']*["\']',
                'severity': 'HIGH',
                'description': 'Event handlers can execute JavaScript'
            },
            'foreign_object': {
                'pattern': r'<foreignObject[^>]*>.*?</foreignObject>',
                'severity': 'MEDIUM',
                'description': 'ForeignObject can contain HTML with scripts'
            },
            'external_scripts': {
                'pattern': r'<script[^>]*href\s*=\s*["\'][^"\']*["\']',
                'severity': 'HIGH',
                'description': 'External script references can load malicious code'
            },
            'use_elements': {
                'pattern': r'<use[^>]*href\s*=\s*["\'][^"\']*["\']',
                'severity': 'MEDIUM',
                'description': 'Use elements can reference external content'
            },
            'eval_function': {
                'pattern': r'\beval\s*\(',
                'severity': 'HIGH',
                'description': 'eval() function can execute dynamic code'
            },
            'base64_encoded': {
                'pattern': r'[A-Za-z0-9+/]{20,}={0,2}',
                'severity': 'LOW',
                'description': 'Base64 encoded content may hide malicious code'
            },
            'hex_encoded': {
                'pattern': r'\\x[0-9a-fA-F]{2}',
                'severity': 'MEDIUM',
                'description': 'Hex encoded strings may hide malicious content'
            },
            'data_urls': {
                'pattern': r'data:[^;]+;base64,',
                'severity': 'MEDIUM',
                'description': 'Data URLs can contain encoded malicious content'
            },
            'javascript_protocol': {
                'pattern': r'javascript:',
                'severity': 'HIGH',
                'description': 'javascript: protocol can execute code'
            },
            'iframe_references': {
                'pattern': r'<iframe[^>]*>',
                'severity': 'MEDIUM',
                'description': 'Iframe elements can load external content'
            },
            'object_references': {
                'pattern': r'<object[^>]*>',
                'severity': 'MEDIUM',
                'description': 'Object elements can load external content'
            }
        }
        
        self.obfuscation_patterns = {
            'string_concatenation': r'["\'][^"\']*["\']\s*\+\s*["\'][^"\']*["\']',
            'variable_obfuscation': r'_\w+\s*=\s*["\'][^"\']*["\']',
            'function_obfuscation': r'Function\s*\(',
            'dynamic_evaluation': r'window\[[^\]]+\]',
        }
    
    def scan_file(self, file_path: str) -> Dict:
        """Scan a single SVG file for security threats."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return self.scan_content(content, file_path)
        except Exception as e:
            return {
                'file': file_path,
                'error': str(e),
                'threats': [],
                'risk_score': 0
            }
    
    def scan_content(self, content: str, file_path: str = "unknown") -> Dict:
        """Scan SVG content for security threats."""
        threats = []
        risk_score = 0
        
        # Normalize content for better pattern matching
        normalized_content = content.lower()
        
        # Check for each threat pattern
        for threat_name, threat_info in self.threats.items():
            pattern = threat_info['pattern']
            matches = re.finditer(pattern, content, re.IGNORECASE | re.DOTALL)
            
            for match in matches:
                threat = {
                    'type': threat_name,
                    'severity': threat_info['severity'],
                    'description': threat_info['description'],
                    'line': self._get_line_number(content, match.start()),
                    'column': match.start() - content.rfind('\n', 0, match.start()),
                    'match': match.group(0)[:100] + ('...' if len(match.group(0)) > 100 else ''),
                    'position': match.start()
                }
                threats.append(threat)
                
                # Calculate risk score
                if threat_info['severity'] == 'HIGH':
                    risk_score += 10
                elif threat_info['severity'] == 'MEDIUM':
                    risk_score += 5
                else:
                    risk_score += 2
        
        # Check for obfuscation patterns
        obfuscation_detected = self._detect_obfuscation(content)
        if obfuscation_detected:
            threats.append({
                'type': 'obfuscation',
                'severity': 'MEDIUM',
                'description': 'Code obfuscation detected - may hide malicious content',
                'line': 'Unknown',
                'column': 'Unknown',
                'match': 'Obfuscation patterns detected',
                'position': 'Unknown'
            })
            risk_score += 5
        
        # Check for potential data exfiltration
        exfiltration_patterns = self._detect_data_exfiltration(content)
        if exfiltration_patterns:
            threats.append({
                'type': 'data_exfiltration',
                'severity': 'HIGH',
                'description': 'Potential data exfiltration patterns detected',
                'line': 'Unknown',
                'column': 'Unknown',
                'match': 'Data exfiltration patterns',
                'position': 'Unknown'
            })
            risk_score += 8
        
        return {
            'file': file_path,
            'threats': threats,
            'risk_score': min(risk_score, 100),  # Cap at 100
            'total_threats': len(threats),
            'severity_breakdown': self._get_severity_breakdown(threats)
        }
    
    def _detect_obfuscation(self, content: str) -> bool:
        """Detect code obfuscation patterns."""
        for pattern_name, pattern in self.obfuscation_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False
    
    def _detect_data_exfiltration(self, content: str) -> bool:
        """Detect potential data exfiltration patterns."""
        exfiltration_patterns = [
            r'document\.cookie',
            r'localStorage',
            r'sessionStorage',
            r'navigator\.userAgent',
            r'window\.location',
            r'fetch\s*\(',
            r'XMLHttpRequest',
            r'sendBeacon',
            r'new\s+Image\s*\(',
            r'img\.src\s*=',
        ]
        
        for pattern in exfiltration_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False
    
    def _get_line_number(self, content: str, position: int) -> int:
        """Get line number for a given position in content."""
        return content[:position].count('\n') + 1
    
    def _get_severity_breakdown(self, threats: List[Dict]) -> Dict:
        """Get breakdown of threats by severity."""
        breakdown = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        for threat in threats:
            breakdown[threat['severity']] += 1
        return breakdown
    
    def scan_directory(self, directory_path: str) -> List[Dict]:
        """Scan all SVG files in a directory."""
        results = []
        directory = Path(directory_path)
        
        if not directory.exists():
            print(f"Error: Directory {directory_path} does not exist")
            return results
        
        svg_files = list(directory.rglob("*.svg"))
        
        if not svg_files:
            print(f"No SVG files found in {directory_path}")
            return results
        
        print(f"Found {len(svg_files)} SVG files to scan...")
        
        for svg_file in svg_files:
            print(f"Scanning {svg_file}...")
            result = self.scan_file(str(svg_file))
            results.append(result)
        
        return results
    
    def generate_report(self, results: List[Dict], output_file: str = None) -> str:
        """Generate a comprehensive security report."""
        report = []
        report.append("=" * 80)
        report.append("SVG SECURITY SCAN REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Summary
        total_files = len(results)
        files_with_threats = sum(1 for r in results if r.get('threats'))
        total_threats = sum(r.get('total_threats', 0) for r in results)
        
        report.append("SUMMARY:")
        report.append(f"  Total files scanned: {total_files}")
        report.append(f"  Files with threats: {files_with_threats}")
        report.append(f"  Total threats found: {total_threats}")
        report.append("")
        
        # Detailed results
        for result in results:
            if result.get('error'):
                report.append(f"❌ ERROR in {result['file']}: {result['error']}")
                continue
            
            if not result.get('threats'):
                report.append(f"✅ {result['file']}: No threats detected")
                continue
            
            report.append(f"🚨 {result['file']}: {result['total_threats']} threats (Risk Score: {result['risk_score']})")
            
            for threat in result['threats']:
                severity_icon = {
                    'HIGH': '🔴',
                    'MEDIUM': '🟡',
                    'LOW': '🟢'
                }.get(threat['severity'], '⚪')
                
                report.append(f"  {severity_icon} {threat['severity']}: {threat['description']}")
                if threat.get('line') != 'Unknown':
                    report.append(f"    Line {threat['line']}, Column {threat['column']}")
                report.append(f"    Match: {threat['match']}")
                report.append("")
        
        report_text = "\n".join(report)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_text)
            print(f"Report saved to {output_file}")
        
        return report_text

def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description="SVG Security Scanner - Educational Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python svg-scanner.py file.svg
  python svg-scanner.py -d /path/to/svg/files
  python svg-scanner.py -d /path/to/svg/files -o report.txt
        """
    )
    
    parser.add_argument('input', nargs='?', help='SVG file or directory to scan')
    parser.add_argument('-d', '--directory', help='Scan directory for SVG files')
    parser.add_argument('-o', '--output', help='Output report to file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if not args.input and not args.directory:
        parser.print_help()
        return
    
    scanner = SVGSecurityScanner()
    
    try:
        if args.directory:
            results = scanner.scan_directory(args.directory)
        else:
            results = [scanner.scan_file(args.input)]
        
        report = scanner.generate_report(results, args.output)
        print(report)
        
    except KeyboardInterrupt:
        print("\nScan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
