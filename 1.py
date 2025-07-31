from flask import Flask, request, render_template_string

app = Flask(__name__)

# Template for the HTML editor
editor_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Live HTML Editor</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background-color: #1e1e2f;
            color: #ffffff;
        }
        .container {
            display: flex;
            height: 100vh;
        }
        .editor {
            width: 50%;
            padding: 20px;
            background-color: #2a2a40;
            border-right: 2px solid #6a0dad;
        }
        .editor textarea {
            width: 100%;
            height: 100%;
            background-color: #1e1e2f;
            color: #ffffff;
            border: 2px solid #6a0dad;
            border-radius: 8px;
            padding: 10px;
            font-size: 16px;
            resize: none;
            outline: none;
        }
        .preview {
            width: 50%;
            padding: 20px;
            background-color: #1e1e2f;
            overflow-y: auto;
        }
        .preview h2 {
            color: #6a0dad;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="editor">
            <textarea id="htmlCode" placeholder="Write your HTML here..."></textarea>
        </div>
        <div class="preview">
            <h2>Preview:</h2>
            <div id="previewContent" style="border: 2px dashed #6a0dad; padding: 10px; border-radius: 8px;">
                <!-- Preview content will appear here -->
            </div>
        </div>
    </div>
    <script>
        const textArea = document.getElementById('htmlCode');
        const preview = document.getElementById('previewContent');

        textArea.addEventListener('input', () => {
            preview.innerHTML = textArea.value;
        });
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def editor():
    html_code = ""
    preview_html = ""
    if request.method == 'POST':
        html_code = request.form.get('html_code', '')
        preview_html = html_code  # Render the submitted HTML code
    return render_template_string(editor_template, html_code=html_code, preview_html=preview_html)

if __name__ == '__main__':
    app.run(debug=True)