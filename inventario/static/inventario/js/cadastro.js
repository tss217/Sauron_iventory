// ==========================================================
// 1. Abas: cada grupo [data-tabs] funciona sozinho
// ==========================================================
document.querySelectorAll('[data-tabs]').forEach((root) => {
  const tabs = Array.from(root.querySelectorAll('[role="tab"]'));
  const panels = Array.from(root.querySelectorAll('[role="tabpanel"]'));

  function activate(tab) {
    tabs.forEach((item) => {
      const selected = item === tab;
      item.classList.toggle('is-active', selected);
      item.setAttribute('aria-selected', String(selected));
      item.tabIndex = selected ? 0 : -1;
    });

    panels.forEach((panel) => {
      panel.hidden = panel.id !== tab.getAttribute('aria-controls');
    });
  }

  tabs.forEach((tab) => {
    tab.addEventListener('click', () => activate(tab));

    tab.addEventListener('keydown', (event) => {
      if (event.key !== 'ArrowRight' && event.key !== 'ArrowLeft') return;

      event.preventDefault();
      const index = tabs.indexOf(tab);
      const step = event.key === 'ArrowRight' ? 1 : -1;
      const next = tabs[(index + step + tabs.length) % tabs.length];

      next.focus();
      activate(next);
    });
  });

  const abaInicial = root.dataset.activeTab;
  if (abaInicial) {
    const alvo = tabs.find((tab) => tab.dataset.tab === abaInicial);
    if (alvo) activate(alvo);
  }
});

// ==========================================================
// 2. Busca nas tabelas de consulta
// ==========================================================
const normalize = (text) =>
  text
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase();

document.querySelectorAll('[data-filter]').forEach((input) => {
  const panel = input.closest('[role="tabpanel"]');
  if (!panel) return;

  const rows = Array.from(panel.querySelectorAll('[data-row]'));
  const noResults = panel.querySelector('[data-no-results]');
  const count = panel.querySelector('[data-count]');

  input.addEventListener('input', () => {
    const term = normalize(input.value.trim());
    let visible = 0;

    rows.forEach((row) => {
      const match = normalize(row.textContent).includes(term);
      row.hidden = !match;
      if (match) visible += 1;
    });

    if (noResults) {
      noResults.hidden = visible > 0 || rows.length === 0 || term === '';
    }

    if (count) {
      count.textContent = `${visible} registro${visible === 1 ? '' : 's'}`;
    }
  });
});