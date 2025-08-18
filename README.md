# SVG Security Lab 🛡️

> **⚠️ WARNING: This repository contains educational content about SVG security vulnerabilities. All payloads are synthetic and designed for learning purposes only. Do not use these techniques against real systems without explicit authorization.**

A comprehensive educational laboratory for understanding SVG security vulnerabilities, attack vectors, and defense mechanisms. This lab provides hands-on experience with SVG-based attacks in a controlled, educational environment.

## 🎯 Learning Objectives

By completing this lab, you will understand:

- **SVG Attack Vectors**: How malicious SVG files can execute code
- **XSS via SVG**: Cross-site scripting attacks through SVG files
- **Data Exfiltration**: How SVG files can steal sensitive information
- **Obfuscation Techniques**: Methods attackers use to hide malicious code
- **Defense Mechanisms**: CSP, Trusted Types, DOMPurify, and other protections
- **Detection Methods**: How to identify and prevent SVG-based attacks

## 🏗️ Lab Structure

```
svg-security-lab/
├── attacks/                 # Synthetic attack examples
│   ├── basic-xss.svg       # Simple XSS demonstration
│   ├── cookie-theft.svg    # Cookie exfiltration example
│   ├── obfuscated.svg      # Obfuscated payload example
│   └── data-exfil.svg      # Data exfiltration techniques
├── defenses/               # Defense implementations
│   ├── csp-demo.html       # Content Security Policy examples
│   ├── trusted-types.html  # Trusted Types implementation
│   ├── dompurify-demo.html # DOMPurify sanitization
│   └── sandbox-demo.html   # Sandboxing techniques
├── detection/              # Detection and analysis tools
│   ├── svg-scanner.py      # Static analysis tool
│   └── payload-detector.js # Runtime detection
├── educational/            # Learning materials
│   ├── attack-vectors.md   # Detailed attack explanations
│   ├── defense-guide.md    # Comprehensive defense guide
│   └── best-practices.md   # Security best practices
├── demos/                  # Interactive demonstrations
│   ├── vulnerable.html     # Vulnerable demo page
│   ├── protected.html      # Protected demo page
│   └── comparison.html     # Side-by-side comparison
└── tools/                  # Utility scripts
    ├── server.py           # Local test server
    └── payload-generator.py # Synthetic payload creator
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Modern web browser
- Basic understanding of web security concepts

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd svg-security-lab

# Start the local server
python tools/server.py

# Open your browser to http://localhost:8000
```

## 📚 Learning Path

### 1. Understanding SVG Vulnerabilities
Start with the basic attack vectors in the `attacks/` directory:
- **basic-xss.svg**: Simple XSS demonstration
- **cookie-theft.svg**: Data exfiltration example
- **obfuscated.svg**: Obfuscation techniques

### 2. Exploring Defense Mechanisms
Study the defense implementations in `defenses/`:
- **Content Security Policy (CSP)**: Restrict script execution
- **Trusted Types**: Prevent DOM-based XSS
- **DOMPurify**: Sanitize untrusted content
- **Sandboxing**: Isolate untrusted content

### 3. Hands-on Practice
Use the interactive demos in `demos/`:
- Compare vulnerable vs. protected implementations
- Test detection tools
- Practice implementing defenses

## 🛡️ Security Features

### Synthetic Payloads Only
All attack examples use synthetic, non-harmful payloads:
- No real data exfiltration
- No actual malicious code execution
- Safe for educational environments

### Controlled Environment
- Local server only
- No external network requests
- Isolated testing environment

### Comprehensive Warnings
- Clear educational purpose statements
- Usage guidelines and restrictions
- Legal and ethical considerations

## 🔧 Defense Mechanisms Covered

### 1. Content Security Policy (CSP)
```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; script-src 'none';">
```

### 2. Trusted Types
```javascript
// Prevent DOM-based XSS
if (window.trustedTypes && window.trustedTypes.createPolicy) {
  window.trustedTypes.createPolicy('default', {
    createHTML: (string) => DOMPurify.sanitize(string)
  });
}
```

### 3. DOMPurify Sanitization
```javascript
// Sanitize SVG content before rendering
const cleanSVG = DOMPurify.sanitize(svgContent, {
  ALLOWED_TAGS: ['svg', 'rect', 'circle', 'text'],
  ALLOWED_ATTR: ['width', 'height', 'fill', 'stroke']
});
```

### 4. Sandboxing
```html
<iframe src="untrusted.svg" sandbox="allow-scripts"></iframe>
```

## 📖 Educational Resources

### Attack Vectors
- **Script Injection**: `<script>` tags in SVG
- **Event Handlers**: `onload`, `onclick` attributes
- **Foreign Objects**: `<foreignObject>` elements
- **External References**: `<use>` and `<image>` elements

### Detection Methods
- **Static Analysis**: Pattern matching and code scanning
- **Dynamic Analysis**: Runtime behavior monitoring
- **File Validation**: Content type verification
- **Behavioral Analysis**: Anomaly detection

### Best Practices
- **Input Validation**: Validate all SVG content
- **Output Encoding**: Properly encode rendered content
- **Principle of Least Privilege**: Minimal required permissions
- **Regular Audits**: Continuous security monitoring

## ⚖️ Legal and Ethical Considerations

### Educational Use Only
This lab is designed exclusively for:
- Security research and education
- Penetration testing training
- Defensive security development
- Academic study

### Prohibited Uses
- Attacking real systems without authorization
- Malicious exploitation of vulnerabilities
- Distribution of actual malware
- Any illegal activities

### Responsible Disclosure
If you discover real vulnerabilities:
1. Report to the affected organization
2. Follow responsible disclosure practices
3. Do not exploit without permission
4. Respect disclosure timelines

## 🤝 Contributing

We welcome contributions that enhance the educational value:

- **New Attack Vectors**: Additional synthetic examples
- **Defense Mechanisms**: Improved protection techniques
- **Detection Tools**: Better analysis capabilities
- **Documentation**: Enhanced learning materials
- **Educational Content**: Tutorials and guides

### Contribution Guidelines
1. All payloads must be synthetic and safe
2. Include comprehensive documentation
3. Follow security best practices
4. Add appropriate warnings and disclaimers

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**This software is provided for educational purposes only. The authors are not responsible for any misuse of this software. Users must comply with all applicable laws and obtain proper authorization before testing these techniques on any system they do not own or have explicit permission to test.**

## 🔗 Additional Resources

- [OWASP SVG Security](https://owasp.org/www-community/attacks/SVG_attack)
- [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
- [Trusted Types](https://web.dev/trusted-types/)
- [DOMPurify](https://github.com/cure53/DOMPurify)

---

**Remember: Security knowledge is power. Use it responsibly to protect, not to harm.** 