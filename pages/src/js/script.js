document.addEventListener("DOMContentLoaded", function() {
    console.log("Império dos Filtros Online! 🚀");
    loadFooter();
});

function loadFooter() {
    const placeholder = document.getElementById('footer-placeholder');
    if (!placeholder) return;

    const isInPagesFolder = window.location.pathname.includes('/pages/');
    const footerPath = isInPagesFolder ? '../footer.html' : 'footer.html';

    fetch(footerPath)
        .then(res => res.text())
        .then(data => {
            placeholder.innerHTML = data;
        })
        .catch(err => console.error("Erro ao carregar rodapé:", err));
}
