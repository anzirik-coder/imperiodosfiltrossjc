document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname.replace(/\\/g, '/');
    let basePath = './';

    if (currentPath.includes('/pages/posts/')) {
        basePath = '../../';
    } else if (currentPath.includes('/pages/')) {
        basePath = '../';
    }

    loadComponent('header-placeholder', basePath + 'components/header.html', basePath);
    loadComponent('footer-placeholder', basePath + 'components/footer.html', basePath);
    optimizeImages();
    
    // Inicializar banner de cookies
    initCookieBanner();
});

var COMPONENT_CACHE_VERSION = '2026-04-22-1';

async function loadComponent(elementId, componentPath, basePath) {
    const placeholder = document.getElementById(elementId);
    if (!placeholder) return;

    try {
        const html = await fetchComponentWithCache(componentPath);
        placeholder.innerHTML = html;
        normalizePaths(placeholder, basePath);

        if (elementId === 'header-placeholder') {
            initMenuToggle();
            setTimeout(setActiveLink, 50);
        }
    } catch (error) {
        console.error('Erro ao carregar ' + elementId + ':', error);
        placeholder.innerHTML = '<p>Erro ao carregar componente</p>';
    }
}

async function fetchComponentWithCache(componentPath) {
    const cacheKey = 'component-cache:' + COMPONENT_CACHE_VERSION + ':' + componentPath;
    const cached = sessionStorage.getItem(cacheKey);

    if (cached) {
        return cached;
    }

    const response = await fetch(componentPath);
    if (!response.ok) throw new Error('Erro ' + response.status);

    const html = await response.text();
    sessionStorage.setItem(cacheKey, html);
    return html;
}

function optimizeImages() {
    window.requestAnimationFrame(function() {
        document.querySelectorAll('img').forEach(function(img, index) {
            if (!img.hasAttribute('decoding')) {
                img.setAttribute('decoding', 'async');
            }
            if (!img.hasAttribute('loading')) {
                img.setAttribute('loading', index < 2 ? 'eager' : 'lazy');
            }
        });
    });
}

function normalizePaths(container, basePath) {
    container.querySelectorAll('[data-href]').forEach(function(el) {
        const dataHref = el.getAttribute('data-href');
        if (!dataHref) return;
        const isAbsolute = dataHref.startsWith('http') || dataHref.startsWith('//') || dataHref.startsWith('mailto:') || dataHref.startsWith('tel:');
        el.setAttribute('href', isAbsolute ? dataHref : (basePath + dataHref));
        el.removeAttribute('data-href');
    });
    
    container.querySelectorAll('[data-src]').forEach(function(el) {
        const dataSrc = el.getAttribute('data-src');
        if (!dataSrc) return;
        const isAbsolute = dataSrc.startsWith('http') || dataSrc.startsWith('//');
        el.setAttribute('src', isAbsolute ? dataSrc : (basePath + dataSrc));
        el.removeAttribute('data-src');
    });
    
    container.querySelectorAll('[data-srcset]').forEach(function(el) {
        const dataSrcset = el.getAttribute('data-srcset');
        if (!dataSrcset) return;
        const isAbsolute = dataSrcset.startsWith('http') || dataSrcset.startsWith('//');
        el.setAttribute('srcset', isAbsolute ? dataSrcset : (basePath + dataSrcset));
        el.removeAttribute('data-srcset');
    });
}

function initMenuToggle() {
    const btnMenu = document.getElementById('btn-menu');
    const menuLinks = document.getElementById('menu-links');
    if (!btnMenu || !menuLinks) return;

    function syncMenuState() {
        const isOpen = menuLinks.classList.contains('ativo');
        btnMenu.setAttribute('aria-expanded', String(isOpen));
        document.body.classList.toggle('menu-mobile-aberto', isOpen);
    }

    btnMenu.addEventListener('click', function() {
        menuLinks.classList.toggle('ativo');
        btnMenu.classList.toggle('ativo');
        syncMenuState();
    });

    menuLinks.querySelectorAll('a').forEach(function(link) {
        link.addEventListener('click', function() {
            menuLinks.classList.remove('ativo');
            btnMenu.classList.remove('ativo');
            syncMenuState();
        });
    });

    window.addEventListener('resize', function() {
        if (window.innerWidth > 992 && menuLinks.classList.contains('ativo')) {
            menuLinks.classList.remove('ativo');
            btnMenu.classList.remove('ativo');
            syncMenuState();
        }
    });

    syncMenuState();
}

function setActiveLink() {
    var links = document.querySelectorAll('.nav-link');
    var current = window.location.pathname.toLowerCase();
    
    links.forEach(function(link) {
        link.classList.remove('ativo');
        var href = link.getAttribute('href');
        if (!href) return;
        
        var linkPath = href.replace(/\\/g, '/').toLowerCase();
        
        if (linkPath === current || linkPath === current + '/' || linkPath === current + 'index.html' || linkPath.endsWith(current.replace(/^.*\//, ''))) {
            link.classList.add('ativo');
        }
    });
}

// Função para controlar o banner de cookies (LGPD)
function initCookieBanner() {
    const banner = document.getElementById('lgpd-banner');
    const btnAceitar = document.getElementById('lgpd-aceitar');
    
    if (!banner || !btnAceitar) return;
    
    // Verificar se o usuário já aceitou os cookies
    if (localStorage.getItem('lgpd-accepted') === 'true') {
        banner.style.display = 'none';
        return;
    }
    
    // Mostrar banner
    banner.style.display = 'block';
    
    // Evento do botão aceitar
    btnAceitar.addEventListener('click', function() {
        // Salvar no localStorage
        localStorage.setItem('lgpd-accepted', 'true');
        
        // Ocultar banner com animação
        banner.style.transition = 'opacity 0.3s ease-out';
        banner.style.opacity = '0';
        
        setTimeout(function() {
            banner.style.display = 'none';
        }, 300);
    });
}