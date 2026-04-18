# RESOLUÇÃO DO SITEMAP - GitHub Pages + Registro.br

## 🔍 Diagnóstico
O GitHub Pages deve servir automaticamente `sitemap.xml` com Content-Type: application/xml

## ✅ Passos para Resolver

### 1. GARANTIR ARQUIVOS NO REPOSITÓRIO
Certifique-se que estes arquivos estão no repositório GitHub:
- `sitemap.xml` ✓
- `robots.txt` ✓
- `CNAME` (com seu domínio) ✓
- `_config.yml` ✓

### 2. FORÇAR REBUILD NO GITHUB PAGES
- Vá ao seu repositório no GitHub
- Clique em **Settings** (Configurações)
- Sidebar esquerda: **Pages**
- Em "Build and deployment", mude a source para outra branch e volte para main/master
- Isso força o rebuild

### 3. VERIFICAR LOCALLY (OPCIONAL)
```powershell
# No diretório do projeto, teste localmente
curl -I http://localhost/sitemap.xml
```

### 4. LIMPAR CACHE DO GOOGLE
No Google Search Console:
1. **Remover o sitemap atual**
   - Vá em Indexação > Sitemaps
   - Clique nos 3 pontos next ao seu sitemap
   - Selecione "Remover"
   - Aguarde 30 segundos

2. **Reenviar o sitemap**
   - Clique em "Novo sitemap"
   - Cole: `https://sjcimperiodosfiltros.com.br/sitemap.xml`
   - Clique em "Enviar"

### 5. VALIDAR URL INDIVIDUAL (OPCIONAL)
Se ainda quiser validar URLs individuais:
- Vá em Indexação > Inspeção de URL
- Cole: `https://sjcimperiodosfiltros.com.br/pages/blog.html`
- O Google testará aquela URL específica

## 📝 Configuração GitHub Pages (_config.yml)

O arquivo `_config.yml` já foi criado no seu projeto com:
- Inclusão de sitemap.xml e robots.txt
- Metadados do site
- Configuração Jekyll correta

## ⏱️ Timeline
- **Imediato**: Fazer commit e push dos arquivos
- **2-5 min**: GitHub Pages rebuilda
- **5-30 min**: Google reconhece o novo Content-Type
- **24-48h**: Indexação completa das URLs

## 🆘 Se Still Não Funcionar

Se o Google continuar rejeitando, use este workaround:
1. Crie arquivo `sitemap.html` com redirecionamento (em último caso)
2. Ou configure webhook para atualizar automaticamente

## ✓ CHECKLIST FINAL
- [ ] Todos os 13 arquivos HTML existem
- [ ] sitemap.xml está no repositório
- [ ] _config.yml criado/commitado
- [ ] robots.txt aponta para https://
- [ ] CNAME tem seu domínio correto
- [ ] Git push foi feito
- [ ] Aguardou rebuild (2-5 min)
- [ ] Removeu e reenviou sitemap no Search Console
