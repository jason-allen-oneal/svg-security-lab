# SVG Security Defense Guide

> **⚠️ WARNING: This document is for educational purposes only. Use these techniques responsibly to protect systems, not to harm them.**

## Overview

This guide provides comprehensive strategies for defending against SVG-based attacks. It covers multiple layers of defense, from input validation to runtime protection.

## Defense Strategy Overview

### Defense in Depth
The most effective approach is to implement multiple layers of defense:

1. **Input Validation** - Validate SVG content before processing
2. **Content Sanitization** - Remove dangerous elements and attributes
3. **Runtime Protection** - Use CSP and other runtime defenses
4. **Monitoring** - Detect and respond to attacks

## 1. Content Security Policy (CSP)

### Basic CSP Implementation

```html
<!-- Block all script execution -->
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; script-src 'none'; object-src 'none';">
```

### Advanced CSP for SVG Protection

```html
<!-- Comprehensive SVG protection -->
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'none'; 
               object-src 'none'; 
               style-src 'self' 'unsafe-inline'; 
               img-src 'self' data: blob:;
               connect-src 'none';
               frame-src 'none';">
```

### CSP Directives Explained

- **`script-src 'none'`**: Blocks all JavaScript execution
- **`object-src 'none'`**: Blocks object and embed elements
- **`connect-src 'none'`**: Blocks network requests
- **`frame-src 'none'`**: Blocks iframe loading

### CSP Report-Only Mode

```html
<!-- Test CSP without blocking content -->
<meta http-equiv="Content-Security-Policy-Report-Only" 
      content="script-src 'none'; report-uri /csp-report">
```

## 2. DOMPurify Sanitization

### Basic DOMPurify Usage

```javascript
// Basic SVG sanitization
const cleanSVG = DOMPurify.sanitize(svgContent);
```

### Custom DOMPurify Configuration

```javascript
// Strict SVG configuration
const cleanSVG = DOMPurify.sanitize(svgContent, {
  ALLOWED_TAGS: ['svg', 'rect', 'circle', 'text', 'path', 'line', 'polygon'],
  ALLOWED_ATTR: [
    'width', 'height', 'fill', 'stroke', 'stroke-width',
    'cx', 'cy', 'r', 'x', 'y', 'text-anchor', 'font-size',
    'font-family', 'd', 'points', 'viewBox'
  ],
  FORBID_TAGS: ['script', 'foreignObject', 'iframe', 'object', 'embed'],
  FORBID_ATTR: [
    'onload', 'onclick', 'onerror', 'onmouseover', 'onmouseout',
    'onfocus', 'onblur', 'onchange', 'onsubmit'
  ],
  KEEP_CONTENT: false,
  RETURN_DOM: false,
  RETURN_DOM_FRAGMENT: false
});
```

### DOMPurify with Custom Hooks

```javascript
// Add custom sanitization logic
DOMPurify.addHook('beforeSanitizeElements', function(current, hook, node) {
  // Remove any element with 'on' attributes
  if (node.hasAttribute && node.hasAttribute('on')) {
    return 'REMOVE_ELEMENT';
  }
  
  // Remove foreignObject elements
  if (node.tagName === 'foreignObject') {
    return 'REMOVE_ELEMENT';
  }
  
  return current;
});

const cleanSVG = DOMPurify.sanitize(svgContent);
```

## 3. Trusted Types

### Basic Trusted Types Setup

```javascript
// Enable Trusted Types enforcement
if (window.trustedTypes && window.trustedTypes.createPolicy) {
  window.trustedTypes.createPolicy('default', {
    createHTML: (string) => DOMPurify.sanitize(string),
    createScript: (string) => string,
    createScriptURL: (string) => string
  });
}
```

### Custom SVG Policy

```javascript
// Create a policy specifically for SVG content
const svgPolicy = trustedTypes.createPolicy('svg-policy', {
  createHTML: (string) => {
    // Remove script tags and event handlers
    return string
      .replace(/<script[^>]*>.*?<\/script>/gi, '')
      .replace(/on\w+\s*=\s*["'][^"']*["']/gi, '')
      .replace(/<foreignObject[^>]*>.*?<\/foreignObject>/gi, '');
  }
});

// Use the policy
element.innerHTML = svgPolicy.createHTML(untrustedSVG);
```

### CSP Integration with Trusted Types

```html
<!-- CSP header to enable Trusted Types -->
<meta http-equiv="Content-Security-Policy" 
      content="require-trusted-types-for 'script';
               trusted-types 'svg-policy' 'default';">
```

## 4. Input Validation

### File Type Validation

```javascript
// Validate file type
function validateSVGFile(file) {
  // Check MIME type
  if (file.type !== 'image/svg+xml') {
    throw new Error('Invalid file type');
  }
  
  // Check file extension
  if (!file.name.toLowerCase().endsWith('.svg')) {
    throw new Error('Invalid file extension');
  }
  
  // Check file size (limit to 1MB)
  if (file.size > 1024 * 1024) {
    throw new Error('File too large');
  }
  
  return true;
}
```

### Content Structure Validation

```javascript
// Validate SVG content structure
function validateSVGContent(content) {
  // Check for SVG root element
  if (!content.includes('<svg')) {
    throw new Error('Invalid SVG: missing root element');
  }
  
  // Check for dangerous elements
  const dangerousElements = ['script', 'foreignObject', 'iframe', 'object'];
  for (const element of dangerousElements) {
    if (content.includes(`<${element}`)) {
      throw new Error(`Invalid SVG: contains ${element} element`);
    }
  }
  
  // Check for event handlers
  const eventHandlerPattern = /on\w+\s*=\s*["'][^"']*["']/gi;
  if (eventHandlerPattern.test(content)) {
    throw new Error('Invalid SVG: contains event handlers');
  }
  
  return true;
}
```

## 5. Sandboxing

### Iframe Sandboxing

```html
<!-- Sandbox SVG in iframe -->
<iframe src="untrusted.svg" 
        sandbox="allow-same-origin"
        style="border: none; width: 100%; height: 300px;">
</iframe>
```

### Sandbox Attributes Explained

- **`allow-same-origin`**: Allows same-origin access
- **`allow-scripts`**: Allows script execution (use carefully)
- **`allow-forms`**: Allows form submission
- **`allow-popups`**: Allows popup windows

### Worker-based Sandboxing

```javascript
// Use Web Workers for SVG processing
const worker = new Worker('svg-processor.js');

worker.postMessage({
  type: 'process',
  svg: svgContent
});

worker.onmessage = function(e) {
  if (e.data.type === 'result') {
    const processedSVG = e.data.svg;
    // Use processed SVG safely
  }
};
```

## 6. Monitoring and Detection

### CSP Violation Monitoring

```javascript
// Monitor CSP violations
document.addEventListener('securitypolicyviolation', function(e) {
  console.log('CSP Violation:', {
    blockedURI: e.blockedURI,
    violatedDirective: e.violatedDirective,
    sourceFile: e.sourceFile,
    lineNumber: e.lineNumber
  });
  
  // Send to monitoring service
  sendViolationReport(e);
});
```

### Runtime Attack Detection

```javascript
// Monitor for suspicious behavior
const originalFetch = window.fetch;
window.fetch = function(...args) {
  // Log all fetch requests
  console.log('Fetch request:', args);
  
  // Block suspicious requests
  if (args[0].includes('attacker.com')) {
    console.warn('Blocked suspicious request');
    return Promise.reject(new Error('Request blocked'));
  }
  
  return originalFetch.apply(this, args);
};
```

## 7. Server-Side Protection

### File Upload Validation

```python
# Python example for server-side validation
import re
import xml.etree.ElementTree as ET

def validate_svg_upload(file_content):
    # Check for dangerous elements
    dangerous_patterns = [
        r'<script[^>]*>.*?</script>',
        r'<foreignObject[^>]*>.*?</foreignObject>',
        r'on\w+\s*=\s*["\'][^"\']*["\']',
        r'javascript:',
        r'data:text/html'
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, file_content, re.IGNORECASE | re.DOTALL):
            raise ValueError(f'Dangerous content detected: {pattern}')
    
    # Validate XML structure
    try:
        ET.fromstring(file_content)
    except ET.ParseError:
        raise ValueError('Invalid XML structure')
    
    return True
```

### Content-Type Headers

```python
# Set proper content type headers
response.headers['Content-Type'] = 'image/svg+xml'
response.headers['X-Content-Type-Options'] = 'nosniff'
response.headers['Content-Security-Policy'] = "script-src 'none'"
```

## 8. Best Practices Checklist

### Development Phase
- [ ] Implement input validation for all SVG uploads
- [ ] Use DOMPurify or similar sanitization library
- [ ] Configure strict CSP headers
- [ ] Enable Trusted Types where supported
- [ ] Test with known malicious SVG files

### Deployment Phase
- [ ] Enable CSP in production
- [ ] Set up CSP violation monitoring
- [ ] Configure proper content-type headers
- [ ] Implement rate limiting for file uploads
- [ ] Set up logging for security events

### Maintenance Phase
- [ ] Regularly update security libraries
- [ ] Monitor for new attack vectors
- [ ] Review and update CSP policies
- [ ] Conduct security audits
- [ ] Keep documentation updated

## 9. Testing Your Defenses

### Test Cases

```javascript
// Test cases for SVG security
const testCases = [
  {
    name: 'Script Injection',
    svg: '<svg><script>alert("XSS")</script></svg>',
    shouldBlock: true
  },
  {
    name: 'Event Handler',
    svg: '<svg><rect onload="alert(\'XSS\')"/></svg>',
    shouldBlock: true
  },
  {
    name: 'Foreign Object',
    svg: '<svg><foreignObject><script>alert("XSS")</script></foreignObject></svg>',
    shouldBlock: true
  },
  {
    name: 'Safe SVG',
    svg: '<svg><rect width="100" height="100" fill="red"/></svg>',
    shouldBlock: false
  }
];

// Run tests
testCases.forEach(test => {
  try {
    const result = processSVG(test.svg);
    console.log(`${test.name}: ${test.shouldBlock ? 'BLOCKED' : 'ALLOWED'}`);
  } catch (error) {
    console.log(`${test.name}: ${test.shouldBlock ? 'CORRECTLY BLOCKED' : 'INCORRECTLY BLOCKED'}`);
  }
});
```

## 10. Resources and Tools

### Security Libraries
- **DOMPurify**: HTML/SVG sanitization
- **js-xss**: XSS prevention library
- **sanitize-html**: Node.js HTML sanitization

### Testing Tools
- **SVG Security Scanner**: Custom scanning tool
- **OWASP ZAP**: Web application security scanner
- **Burp Suite**: Web application security testing

### Documentation
- [OWASP SVG Security](https://owasp.org/www-community/attacks/SVG_attack)
- [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
- [Trusted Types](https://web.dev/trusted-types/)
- [DOMPurify Documentation](https://github.com/cure53/DOMPurify)

---

**Remember: Security is an ongoing process. Stay vigilant, keep learning, and always test your defenses.**
