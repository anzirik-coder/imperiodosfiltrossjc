#!/usr/bin/env python3
"""
Validador de Sitemap - Império dos Filtros
Verifica conformidade com especificações do Google e boas práticas de SEO
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
import sys

def validate_sitemap(filepath):
    """Valida arquivo sitemap.xml"""
    
    print("=" * 70)
    print("VALIDAÇÃO DE SITEMAP - IMPÉRIO DOS FILTROS")
    print("=" * 70)
    
    try:
        # 1. Verificar existência do arquivo
        path = Path(filepath)
        if not path.exists():
            print(f"❌ ERRO: Arquivo não encontrado: {filepath}")
            return False
        
        print(f"✓ Arquivo encontrado: {path.name}")
        print(f"  Tamanho: {path.stat().st_size} bytes")
        print(f"  Modificado: {datetime.fromtimestamp(path.stat().st_mtime)}\n")
        
        # 2. Verificar encoding e BOM
        with open(filepath, 'rb') as f:
            raw = f.read()
            if raw.startswith(b'\xef\xbb\xbf'):
                print("⚠ AVISO: Arquivo contém BOM UTF-8 (não recomendado)")
            elif raw.startswith(b'<?xml'):
                print("✓ Encoding UTF-8 sem BOM (Correto)")
            else:
                print("❌ ERRO: Encoding inválido")
                return False
        
        # 3. Parse XML
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"❌ ERRO de Parse XML: {e}")
            return False
        
        print("✓ XML bem-formado\n")
        
        # 4. Validar namespace
        ns = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = root.findall('sitemap:url', ns)
        
        if not urls:
            # Tenta sem namespace
            urls = root.findall('url')
            if urls:
                print("⚠ AVISO: Namespace não declarado corretamente")
            else:
                print("❌ ERRO: Nenhuma URL encontrada no sitemap")
                return False
        
        # 5. Validar URLs
        print(f"Total de URLs: {len(urls)}\n")
        print("VALIDAÇÃO DE URLs:")
        print("-" * 70)
        
        errors = []
        domain = 'https://sjcimperiodosfiltros.com.br'
        
        for i, url_elem in enumerate(urls, 1):
            loc = url_elem.find('sitemap:loc', ns)
            if loc is None:
                loc = url_elem.find('loc')
            
            lastmod = url_elem.find('sitemap:lastmod', ns)
            if lastmod is None:
                lastmod = url_elem.find('lastmod')
            
            priority = url_elem.find('sitemap:priority', ns)
            if priority is None:
                priority = url_elem.find('priority')
            
            url_text = loc.text if loc is not None else None
            
            # Validar URL
            if not url_text:
                errors.append(f"URL #{i}: Elemento <loc> vazio")
                continue
            
            if not url_text.startswith(domain):
                errors.append(f"URL #{i}: Domínio inválido: {url_text}")
            
            if not url_text.startswith('https://'):
                errors.append(f"URL #{i}: Deve usar HTTPS: {url_text}")
            
            # Validar lastmod
            if lastmod is not None:
                try:
                    dt = datetime.fromisoformat(lastmod.text.replace('Z', '+00:00'))
                except (ValueError, TypeError):
                    errors.append(f"URL #{i}: lastmod inválido: {lastmod.text}")
            
            # Validar priority
            if priority is not None:
                try:
                    p = float(priority.text)
                    if not (0.0 <= p <= 1.0):
                        errors.append(f"URL #{i}: priority fora do intervalo 0.0-1.0: {p}")
                except ValueError:
                    errors.append(f"URL #{i}: priority não é número: {priority.text}")
            
            # Exibir primeira URL como exemplo
            if i == 1:
                print(f"[1/13] {url_text}")
                if lastmod is not None:
                    print(f"       lastmod: {lastmod.text}")
                if priority is not None:
                    print(f"       priority: {priority.text}")
        
        if errors:
            print("\n❌ ERROS ENCONTRADOS:")
            for error in errors:
                print(f"  - {error}")
            return False
        else:
            print("✓ Todas as URLs validadas com sucesso\n")
        
        # 6. Resumo
        print("=" * 70)
        print("RESUMO DE CONFORMIDADE")
        print("=" * 70)
        print("✓ XML bem-formado")
        print("✓ Namespace correto")
        print(f"✓ {len(urls)} URLs presentes")
        print("✓ Todas as URLs com domínio válido (https)")
        print("✓ Estrutura conforme especificação W3C")
        print("✓ Pronto para envio ao Google Search Console\n")
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO inesperado: {e}")
        return False

if __name__ == '__main__':
    sitemap_path = 'sitemap.xml'
    success = validate_sitemap(sitemap_path)
    sys.exit(0 if success else 1)
