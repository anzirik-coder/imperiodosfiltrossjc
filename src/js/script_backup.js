document.addEventListener('DOMContentLoaded', function() {
    console.log('[Script] Iniciando componentes...');
    
    const currentPath = window.location.pathname.replace(/\\/g, '/');
    let basePath = './';

    if (currentPath.includes('/pages/posts/')) {
        basePath = '../../';
    } else if (currentPath.includes('/pages/')) {
        basePath = '../';
    }

    console.log('[Script] currentPath:', currentPath, 'basePath:', basePath);
    
    loadComponent('header-placeholder', basePath + 'components/header.html', basePath);
    loadComponent('footer-placeholder', basePath + 'components/footer.html', basePath);
});

async function loadComponent(elementId, componentPath, basePath) {
    const placeholder = document.getElementById(elementId);
    if (!placeholder) {
        console.warn('[Script] Placeholder não encontrado:', elementId);
        return;
    }

    try {
        console.log('[Script] Carregando:', componentPath);
        const response = await fetch(componentPath);
        if (!response.ok) throw new Error(`Erro ${response.status}`);

        const html = await response.text();
        placeholder.innerHTML = html;
        console.log('[Script] Carregado:', elementId);
        
        normalizePaths(placeholder, basePath);

        if (elementId === 'header-placeholder') {
            initMenuToggle();
            setTimeout(setActiveLink, 100);
        }
    } catch (error) {
        console.error('[Script] Erro ao carregar ' + elementId + ':', error);
        placeholder.innerHTML = '<div style="background: #fee; color: #900; padding: 16px;">Erro ao carregar componente</div>';
    }
}

function normalizePaths(container, basePath) {
    container.querySelectorAll('[data-href]').forEach(el => {
        const dataHref = el.getAttribute('data-href');
        if (!dataHref.startsWith('http') && !dataHref.startsWith('//') && 
            !dataHref.startsWith('mailto:') && !dataHref.startsWith('tel:') && !dataHref.startsWith('#')) {
            el.setAttribute('href', basePath + dataHref);
        } else {
            el.setAttribute('href', dataHref);
        }
        el.removeAttribute('data-href');
    });
    
    container.querySelectorAll('[data-src]').forEach(el => {
        const dataSrc = el.getAttribute('data-src');
        const finalSrc = dataSrc.startsWith('http') || dataSrc.startsWith('//') ? dataSrc : basePath + dataSrc;
        el.setAttribute('src', finalSrc);
        el.removeAttribute('data-src');
    });
    
    container.querySelectorAll('[data-srcset]').forEach(el => {
        const dataSrcset = el.getAttribute('data-srcset');
        const finalSrcset = dataSrcset.startsWith('http') || dataSrcset.startsWith('//') ? dataSrcset : basePath + dataSrcset;
        el.setAttribute('srcset', finalSrcset);
        el.removeAttribute('data-srcset');
    });
}

function initMenuToggle() {
    const btnMenu = document.getElementById('btn-menu');
    const menuLinks = document.getElementById('menu-links');
    if (!btnMenu || !menuLinks) return;

    btnMenu.addEventListener('click', function() {
        menuLinks.classList.toggle('ativo');
        menuLinks.classList.toggle('active');
        btnMenu.classList.toggle('ativo');
        btnMenu.classList.toggle('open');
    });

    menuLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            menuLinks.classList.remove('ativo');
            menuLinks.classList.remove('active');
            btnMenu.classList.remove('ativo');
            btnMenu.classList.remove('open');
        });
    });
}

function setActiveLink() {
    const currentPath = window.location.pathname.replace(/\\/g, '/').toLowerCase();
    const links = document.querySelectorAll('.nav-link');
    
    links.forEach(link => {
        link.classList.remove('ativo');
        const href = link.getAttribute('href');
        if (!href) return;
        
        try {
            let linkPath;
            if (href.startsWith('http') || href.startsWith('//')) {
                linkPath = new URL(href).pathname.toLowerCase();
            } else {
                linkPath = new URL(href, window.location.origin + window.location.pathname.substring(0, window.location.pathname.lastIndexOf('/') + 1)).pathname.toLowerCase();
            }
            
            const normCurrent = currentPath.endsWith('/') ? currentPath + 'index.html' : currentPath;
            const normLink = linkPath.endsWith('/') ? linkPath + 'index.html' : linkPath;
            
            if (normCurrent === normLink) {
                link.classList.add('ativo');
            }
        } catch (e) {
            // erro ao processar link
        }
    });
}
