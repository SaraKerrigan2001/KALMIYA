import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract <style>...</style> block
match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
if match:
    style_content = match.group(1)
    
    # write to static/style.css
    with open('static/style.css', 'w', encoding='utf-8') as sf:
        sf.write(style_content.strip())
        
    # replace in HTML
    new_content = content.replace(match.group(0), '<link rel="stylesheet" href="/static/style.css">')
    
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Styles extracted to static/style.css")
else:
    print("No <style> block found.")
