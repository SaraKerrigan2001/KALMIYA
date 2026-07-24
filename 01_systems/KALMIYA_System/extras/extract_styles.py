import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

styles_to_extract = {}
counter = 1

# Find all occurrences of style="..." inside HTML tags
# We only want to match style="something", taking care of spaces
pattern = r'(<[^>]+?)\s+style="([^"]+)"([^>]*>)'

def replacer(match):
    global counter
    before_style = match.group(1)
    style_val = match.group(2)
    after_style = match.group(3)
    
    # Ignore if it's inside a script or style block, though `<` matching usually prevents it unless it's a string literal in JS.
    # We will assume all <tag style="..."> are actual HTML tags.
    
    if style_val not in styles_to_extract:
        class_name = f"mod-style-{counter}"
        styles_to_extract[style_val] = class_name
        counter += 1
    else:
        class_name = styles_to_extract[style_val]
        
    # Reconstruct tag
    # Check if there is already a class attribute in before_style or after_style
    class_pattern = r'class="([^"]+)"'
    
    # We'll merge before and after to find class
    tag_inner = before_style + after_style
    class_match = re.search(class_pattern, tag_inner)
    
    if class_match:
        existing_classes = class_match.group(1)
        new_classes = f"{existing_classes} {class_name}"
        # remove old class attribute
        tag_inner = re.sub(class_pattern, f'class="{new_classes}"', tag_inner, count=1)
        return tag_inner
    else:
        # no existing class
        return f'{before_style} class="{class_name}"{after_style}'

new_content = re.sub(pattern, replacer, content)

# Now we need to append the extracted styles to the <style> block
css_rules = []
for style_val, class_name in styles_to_extract.items():
    css_rules.append(f".{class_name} {{ {style_val} }}")

css_block = "\n        /* Extracted Inline Styles */\n        " + "\n        ".join(css_rules) + "\n    </style>"

new_content = new_content.replace("</style>", css_block)

with open('templates/index_clean.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Extracted {len(styles_to_extract)} unique styles.")
