#!/usr/bin/env python3
"""
Validador de Sitemap - Testa conformidade antes de fazer commit
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
import sys

def validate_sitemap():
    """Valida arquivo sitemap.xml gerado"""
    
    ROOT_DIR = Path(__file__).parent.parent.parent
    SITEMAP_FILE = ROOT_DIR / "sitemap.xml"
    
    print("🔍 Validando sitemap.xml...\n")
    
    if not SITEMAP_FILE.exists():
        print("❌ ERRO: sitemap.xml não encontrado!")
        return False
    
    try:
        tree = ET.parse(SITEMAP_FILE)
        root = tree.getroot()
        
        # Verificar namespace
        ns = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = root.findall('sitemap:url', ns)
        
        if not urls:
            urls = root.findall('url')
        
        print(f"✓ XML bem-formado")
        print(f"✓ Total de URLs: {len(urls)}\n")
        
        # Validar cada URL
        errors = []
        for i, url_elem in enumerate(urls, 1):
            loc = url_elem.find('sitemap:loc', ns)
            if loc is None:
                loc = url_elem.find('loc')
            
            if loc is None or not loc.text:
                errors.append(f"URL #{i}: <loc> vazio")
                continue
            
            url_text = loc.text.strip()
            
            # Validações
            if not url_text.startswith("https://"):
                errors.append(f"URL #{i}: Deve usar HTTPS: {url_text}")
            
            if not url_text.startswith("https://sjcimperiodosfiltros.com.br"):
                errors.append(f"URL #{i}: Domínio inválido: {url_text}")
        
        if errors:
            print("❌ ERROS ENCONTRADOS:")
            for error in errors:
                print(f"  - {error}")
            return False
        else:
            print("✅ Todas as URLs validadas com sucesso!")
            print("✓ Pronto para fazer commit\n")
            return True
            
    except ET.ParseError as e:
        print(f"❌ ERRO de Parse XML: {e}")
        return False
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

if __name__ == "__main__":
    success = validate_sitemap()
    sys.exit(0 if success else 1)
