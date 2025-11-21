function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  document.body.appendChild(toast);
  
  setTimeout(() => toast.classList.add('show'), 10);
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

if (typeof window !== 'undefined') {
  window.showToast = showToast;
}

function createScrollToTop() {
  const btn = document.createElement('button');
  btn.id = 'scroll-to-top';
  btn.innerHTML = '↑';
  btn.setAttribute('aria-label', 'Scroll to top');
  document.body.appendChild(btn);
  
  window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  });
  
  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

function setupKeyboardShortcuts() {
  document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    
    if (e.key === '/' && !e.ctrlKey && !e.metaKey) {
      e.preventDefault();
      const searchInput = document.getElementById('game-search') || document.getElementById('search-input');
      if (searchInput) {
        searchInput.focus();
        showToast('Search focused!', 'info');
      }
    }
    
    if (e.key === 'Escape') {
      const iframe = document.getElementById('game-iframe-container');
      if (iframe) iframe.remove();
      const searchInput = document.getElementById('game-search') || document.getElementById('search-input');
      if (searchInput) searchInput.blur();
    }
    
    if (e.key === 'h' && !e.ctrlKey && !e.metaKey) {
      const homeLink = document.querySelector('nav a[href*="index.html"]');
      if (homeLink) homeLink.click();
    }
    
    if (e.key === 'g' && !e.ctrlKey && !e.metaKey) {
      const gamesLink = document.querySelector('nav a[href*="games.html"]');
      if (gamesLink) gamesLink.click();
    }
  });
}

function getFavorites() {
  try {
    const favs = localStorage.getItem('gameFavorites');
    return favs ? JSON.parse(favs) : [];
  } catch {
    return [];
  }
}

function saveFavorites(favs) {
  try {
    localStorage.setItem('gameFavorites', JSON.stringify(favs));
  } catch (e) {
    console.error('Failed to save favorites:', e);
  }
}

function toggleFavorite(gameId, gameTitle) {
  const favs = getFavorites();
  const index = favs.indexOf(gameId);
  
  if (index > -1) {
    favs.splice(index, 1);
    showToast(`Removed ${gameTitle} from favorites`, 'info');
  } else {
    favs.push(gameId);
    showToast(`Added ${gameTitle} to favorites`, 'success');
  }
  
  saveFavorites(favs);
  return favs.includes(gameId);
}

function isFavorite(gameId) {
  return getFavorites().includes(gameId);
}

function pickRandomGame(games) {
  if (!games || games.length === 0) return null;
  return games[Math.floor(Math.random() * games.length)];
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    createScrollToTop();
    setupKeyboardShortcuts();
  });
} else {
  createScrollToTop();
  setupKeyboardShortcuts();
}

