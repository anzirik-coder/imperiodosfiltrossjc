#!/usr/bin/env python3
"""
Gerador Automático de Sitemap
Varre arquivos HTML e gera sitemap.xml conforme especificação W3C
"""

import os
import glob
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

# Configurações
DOMAIN = "https://sjcimperiodosfiltros.com.br"
ROOT_DIR = Path(__file__).parent.parent.parent
OUTPUT_FILE = ROOT_DIR / "sitemap.xml"

# Prioridades por tipo de página
PRIORITIES = {
    "index.html": "1.00",
    "pages/troca_de_oleo_sjc.html": "0.80",
    "pages/filtros_sjc.html": "0.80",
    "pages/blog.html": "0.70",
    "pages/sobre.html": "0.60",
    "pages/contato.html": "0.60",
    "politica.html": "0.40",
    "pages/posts/": "0.60",
}

def get_priority(filepath):
    """Retorna prioridade baseada no caminho do arquivo"""
    relative = str(filepath).replace(str(ROOT_DIR) + os.sep, "").replace("\\", "/")
    
    for key, priority in PRIORITIES.items():
        if relative.endswith(key) or relative.startswith(key):
            return priority
    
    return "0.50"  # Padrão

def find_html_files():
    """Encontra todos os arquivos HTML publicados"""
    files = []
    
    # Raiz
    for html in glob.glob(str(ROOT_DIR / "*.html")):
        path = Path(html)
        if path.name not in [".gitignore"]:
            files.append(path)
    
    # Diretório pages recursivo
    if (ROOT_DIR / "pages").exists():
        for html in glob.glob(str(ROOT_DIR / "pages" / "**" / "*.html"), recursive=True):
            files.append(Path(html))
    
    return sorted(set(files))

def get_last_modified(filepath):
    """Retorna a data de modificação do arquivo"""
    mtime = os.path.getmtime(filepath)
    dt = datetime.utcfromtimestamp(mtime)
    return dt.isoformat() + "+00:00"

def generate_sitemap():
    """Gera arquivo sitemap.xml"""
    
    print("🔍 Procurando arquivos HTML...")
    files = find_html_files()
    
    if not files:
        print("❌ Nenhum arquivo HTML encontrado!")
        return False
    
    print(f"✓ Encontrados {len(files)} arquivos\n")
    
    # Criar raiz do XML
    urlset = ET.Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    urlset.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    urlset.set("xsi:schemaLocation", 
               "http://www.sitemaps.org/schemas/sitemap/0.9 "
               "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd")
    
    # Adicionar cada URL
    for filepath in files:
        relative = str(filepath).replace(str(ROOT_DIR) + os.sep, "").replace("\\", "/")
        
        # Construir URL
        if relative == "index.html":
            url = DOMAIN
        else:
            url = urljoin(DOMAIN + "/", relative)
        
        # Criar elemento URL
        url_elem = ET.SubElement(urlset, "url")
        
        loc = ET.SubElement(url_elem, "loc")
        loc.text = url.rstrip("/")
        
        lastmod = ET.SubElement(url_elem, "lastmod")
        lastmod.text = get_last_modified(filepath)
        
        priority = ET.SubElement(url_elem, "priority")
        priority.text = get_priority(filepath)
        
        print(f"  ✓ {url}")
    
    # Formatar XML com indentação
    rough_string = ET.tostring(urlset, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    
    # Remover linhas vazias extras
    pretty_xml = "\n".join([line for line in pretty_xml.split("\n") if line.strip()])
    
    # Adicionar declaração XML correta
    final_xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + pretty_xml.split('\n', 1)[1]
    
    # Salvar arquivo
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_xml)
    
    print(f"\n✅ Sitemap gerado: {OUTPUT_FILE}")
    print(f"📊 Total de URLs: {len(files)}")
    
    return True

if __name__ == "__main__":
    try:
        success = generate_sitemap()
        exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Erro ao gerar sitemap: {e}")
        exit(1)
