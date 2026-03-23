# BlindFilePwn - Blind File Upload Vulnerability Exploitation Tool

A comprehensive Python-based tool designed for security researchers and penetration testers to identify and exploit **blind file upload vulnerabilities** in real-world web applications.

## Overview

Blind file upload vulnerabilities occur when an application accepts file uploads without providing feedback about whether the upload was successful, where the file was stored, or if it was executed.

BlindFilePwn automates the detection and exploitation of these vulnerabilities using proven techniques.

## Features

### 8 Exploitation Techniques

1. **Basic Upload Detection** - Tests if endpoint accepts files
2. **Web Shell Upload** - PHP, JSP, ASPX execution
3. **Path Traversal** - Directory escape (`../../../`)
4. **Null Byte Injection** - PHP < 5.3.4 exploitation
5. **Double Extension** - Extension confusion bypass
6. **Timing-Based Detection** - Response time analysis
7. **Error-Based Detection** - Error message analysis
8. **Path Enumeration** - Upload directory discovery

## Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/BlindFilePwn.git
cd BlindFilePwn

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Scan
```bash
python blindfilepwn.py -u http://target.com
```

### With Options
```bash
python blindfilepwn.py -u http://target.com -e /api/upload -p uploadfile -v -t 20
```

### Options

- `-u, --url`: Target URL (required)
- `-e, --endpoint`: Upload endpoint (default: /upload)
- `-p, --param`: File parameter name (default: file)
- `-t, --timeout`: Request timeout seconds (default: 10)
- `-v, --verbose`: Enable verbose output

## Examples

### Example 1: Basic Scan
```bash
python blindfilepwn.py -u http://vulnerable.local
```

### Example 2: Custom Endpoint
```bash
python blindfilepwn.py -u http://target.com -e /api/document/upload -p document
```

### Example 3: Verbose with Timeout
```bash
python blindfilepwn.py -u http://slow-server.com -v -t 30
```

## Real-World Applications

- Penetration testing
- Security vulnerability assessment
- Bug bounty hunting
- Compliance and security auditing
- Proof of concept development

## How It Works

1. Tests target connectivity
2. Attempts basic file upload
3. Tests web shell uploads (PHP, JSP, ASPX)
4. Tests path traversal techniques
5. Tests null byte injection
6. Tests double extension bypass
7. Analyzes timing patterns
8. Analyzes error messages
9. Discovers upload directories
10. Generates vulnerability report

## Output Examples

### Vulnerable Application
```
[SUCCESS] + Upload endpoint responds with 200 OK
[SUCCESS] + shell.php uploaded
[SUCCESS] + Path traversal accepted: ../shell.php
Assessment: CRITICAL RISK
```

### Protected Application
```
[WARNING] - shell.php upload failed (403 Forbidden)
[WARNING] - Path traversal rejected
Assessment: MEDIUM RISK
```

## Mitigation

Protect against these vulnerabilities:

1. Whitelist file extensions
2. Store uploads outside web root
3. Rename files with random identifiers
4. Validate file content (not just extension)
5. Disable script execution in upload directory
6. Implement proper access controls
7. Use antivirus scanning
8. Monitor upload activity
9. Set proper file permissions
10. Use Content Security Policy headers

## Legal Notice

**IMPORTANT**: Only use this tool on systems you own or have explicit written permission to test.

- Authorized penetration testing: OK
- Bug bounty programs: OK (with permission)
- Security research: OK (own systems only)
- Unauthorized testing: NOT OK
- Illegal activity: NOT OK

**Disclaimer**: This tool is provided "as is" for authorized security testing only. Users are responsible for compliance with all applicable laws and regulations.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

- Full documentation: See this README
- Quick reference: QUICKSTART.md
- Example outputs: EXAMPLE_RESULTS.md
- Project overview: PROJECT_SUMMARY.md

## Resources

### OWASP
- [Unrestricted File Upload](https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload)
- [Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal)

### CWE
- [CWE-434: Unrestricted Upload](https://cwe.mitre.org/data/definitions/434.html)
- [CWE-22: Path Traversal](https://cwe.mitre.org/data/definitions/22.html)

## License

MIT License - See LICENSE file for details

## Version

- **Version**: 1.0
- **Status**: Production Ready
- **Last Updated**: March 2026

---

**Start scanning**: `python blindfilepwn.py -u http://target.com`

For authorized security testing purposes only.
