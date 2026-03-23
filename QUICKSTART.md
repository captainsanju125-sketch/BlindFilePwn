# BlindFilePwn - Quick Start Guide

## Installation

```bash
pip install -r requirements.txt
```

## Basic Usage

```bash
python blindfilepwn.py -u http://target.com
```

## Common Commands

| Task | Command |
|------|---------|
| Basic scan | `python blindfilepwn.py -u http://target.com` |
| Verbose output | `python blindfilepwn.py -u http://target.com -v` |
| Custom endpoint | `python blindfilepwn.py -u http://target.com -e /api/upload` |
| Custom parameter | `python blindfilepwn.py -u http://target.com -p uploadfile` |
| Longer timeout | `python blindfilepwn.py -u http://target.com -t 20` |
| Help | `python blindfilepwn.py --help` |

## What Each Test Does

- **Basic Upload**: Checks if endpoint accepts files
- **Web Shell**: Uploads executable code (PHP/JSP)
- **Path Traversal**: Tests `../` directory escape
- **Null Byte**: Exploits PHP < 5.3.4
- **Double Extension**: Tests `.php.jpg` bypass
- **Timing-Based**: Measures response delays
- **Error-Based**: Analyzes error messages
- **Path Enumeration**: Discovers upload directories

## Success Indicators

- `[SUCCESS]` = Vulnerability found
- `[WARNING]` = Test failed, blocked by filter
- `[ERROR]` = Connection/network issue
- `[INFO]` = Status message

## Example Output

```
[2026-03-23 14:48:24] [SUCCESS] + Upload endpoint responds with 200 OK
[2026-03-23 14:48:26] [SUCCESS] + shell.php uploaded
[2026-03-23 14:48:28] [SUCCESS] + Path traversal accepted: ../shell.php
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Target unreachable | Check URL, verify target is online |
| 403 Forbidden | Try different endpoint: `-e /api/upload` |
| Timeout | Increase timeout: `-t 20` |
| No results | Target may be properly protected |

## Next Steps

1. Review the README.md for detailed documentation
2. Check EXAMPLE_RESULTS.md for output interpretation
3. Use findings for manual exploitation testing
4. Report vulnerabilities responsibly

## Quick Tips

- Run tests in verbose mode to see details: `-v`
- Increase timeout for slow targets: `-t 30`
- Test multiple endpoints if `/upload` doesn't work
- Try different parameter names if `file` doesn't work

---
**For full documentation, see README.md**
