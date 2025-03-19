# PassFort  
PassFort password strength tester that follows OWASP guidelines, checks for breaches, generates strong passphrases, and offers protection from keyloggers and screenloggers.  

## Key Features  

### 🔒 Password Strength Tester  
It implements a comprehensive password strength tester following OWASP guidelines, which evaluates passwords through a set of required and optional tests. It supports long passwords of 64 or more characters without enforcing composition rules like mandatory uppercase letters, numbers, or special characters — focusing instead on overall resilience. Passwords longer than 20 characters are identified as passphrases. Based on the results, the password is classified as **strong** or **weak**, with detailed feedback on any issues.  

### 🔍 Breach Detection  
PassFort checks if your password has been compromised in known data breaches. It scans the password against the `rockyou.txt` list of common passwords and leverages the **"Have I Been Pwned"** API to detect if the password appears in a breach, ensuring you avoid unsafe, reused, or compromised credentials.  

### 🔑 Smart Passphrase Generator  
For users who prefer a secure yet memorable alternative to complex passwords, PassFort offers a **passphrase generator**. It takes user-provided keywords and combines them with randomized, readable text from preferred dataset to create strong, unique passphrases that are easier to remember while maintaining high entropy.  

### 🛡️ ScreenLogger and KeyLogger Protection  
To defend against keyloggers and screenloggers, PassFort implements a special input method that allows users to **camouflage their passwords**. This method masks the real password within the entered text, preventing malicious programs from capturing the actual input.  

### ✅ User-Friendly Interface  
PassFort is designed to be lightweight, easy to use, and flexible. It runs smoothly as a standalone script, requiring minimal setup. Clear, concise feedback ensures that users — whether beginners or cybersecurity enthusiasts — understand their password’s strength, potential vulnerabilities, and how to improve it. 

---

✨ **[PassFort](https://www.canva.com/design/DAGheTaPuyo/bA7GasxsNs1RVC-ny9m_Zw/view?utm_content=DAGheTaPuyo&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=ha1fa92879b) empowers users to create and protect strong, uncompromised passwords without the usual hassle, aligning with OWASP’s best practices for modern cybersecurity.**  
