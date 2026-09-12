import os
import sys

# Ensure KALMIYA_System root is in path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from core.module_manager import manager

def generate_docs():
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(base_dir)), "06_docs", "modules")
    os.makedirs(docs_dir, exist_ok=True)
    
    info = manager.get_loaded_modules_info()
    
    index_content = "# KALMIYA Modules Documentation\n\n"
    index_content += "This documentation is auto-generated.\n\n"
    
    for module_name, functions in info.items():
        doc_path = os.path.join(docs_dir, f"{module_name}.md")
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(f"---\n")
            f.write(f"title: {module_name} Module\n")
            f.write(f"tags: [kalmiya, module, auto-generated]\n")
            f.write(f"---\n\n")
            f.write(f"# 🧩 {module_name}\n\n")
            f.write("## Funciones disponibles:\n")
            for func in functions:
                f.write(f"- `{func}`\n")
            
            f.write("\n## Uso:\n")
            f.write("Puedes pedirle a KALMIYA que ejecute estas funciones directamente en el chat.\n")
            
        index_content += f"- [[{module_name}]]\n"
        print(f"Generated doc for {module_name}")
        
    index_path = os.path.join(docs_dir, "INDEX.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_content)
        
    print(f"Generated {len(info)} documents in {docs_dir}")

if __name__ == "__main__":
    generate_docs()
