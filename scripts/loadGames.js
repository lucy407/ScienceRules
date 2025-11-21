let allGames = [];
let allCategories = new Set();

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

fetch('../scripts/games.json')
  .then(res => {
    if (!res.ok) throw new Error('Failed to load games.json');
    return res.json();
  })
  .then(games => {
    allGames = games;
    games.forEach(g => { if (g.category) allCategories.add(g.category); });
    setupSortDropdown();
    const sortedAZ = [...allGames].sort((a, b) => a.title.localeCompare(b.title));
    displayGames(sortedAZ);
  })
  .catch(err => {
    console.error('Error loading games:', err);
    const gameList = document.getElementById('game-list');
    if (gameList) gameList.innerHTML = '<p style="color: #ccc; padding: 20px;">Failed to load games. Please refresh the page.</p>';
  });

function setupSortDropdown() {
  const dropdown = document.getElementById('sort-dropdown');
  if (!dropdown) return;
  dropdown.innerHTML = '';

  const baseOptions = ['A-Z', 'Newest', 'Oldest', 'Favorites'];
  baseOptions.forEach(opt => {
    const option = document.createElement('option');
    option.value = opt;
    option.textContent = opt;
    dropdown.appendChild(option);
  });

  allCategories.forEach(category => {
    const option = document.createElement('option');
    option.value = category;
    option.textContent = category;
    dropdown.appendChild(option);
  });

  dropdown.value = 'A-Z';
  dropdown.addEventListener('change', handleSortChange);
}

function handleSortChange(e) {
  const sortType = e.target.value;
  
  if (!allGames || allGames.length === 0) {
    console.warn('allGames not loaded yet');
    return;
  }
  
  let sorted = [...allGames];

  if (sortType === 'A-Z') {
    sorted.sort((a, b) => a.title.localeCompare(b.title));
  } else if (sortType === 'Newest') {
    sorted = sorted.reverse();
  } else if (sortType === 'Oldest') {
  } else if (sortType === 'Favorites') {
    try {
      const favs = JSON.parse(localStorage.getItem('gameFavorites') || '[]');
      if (favs.length === 0) {
        if (window.showToast) window.showToast('No favorites yet!', 'info');
        sorted = [];
      } else {
        sorted = allGames.filter(g => g && g.id && favs.includes(g.id));
        if (sorted.length === 0) {
          if (window.showToast) window.showToast('No favorites found!', 'info');
        }
      }
    } catch (err) {
      console.error('Error loading favorites:', err);
      sorted = [];
    }
  } else {
    sorted = allGames.filter(g => g.category === sortType);
  }

  displayGames(sorted);
}

function updateFavoritesCount() {
  const favCountElem = document.getElementById('favorites-count');
  if (favCountElem) {
    try {
      const favs = JSON.parse(localStorage.getItem('gameFavorites') || '[]');
      favCountElem.textContent = favs.length;
    } catch {
      favCountElem.textContent = '0';
    }
  }
}

function displayGames(games) {
  const gameCountElem = document.getElementById('game-count');
  if (gameCountElem) gameCountElem.textContent = `${games.length}`;
  
  updateFavoritesCount();

  const gameList = document.getElementById('game-list');
  if (!gameList) return;
  gameList.innerHTML = '';

  games.forEach(game => {
    const card = document.createElement('div');
    card.className = 'game-card';
    const isFav = typeof window !== 'undefined' && window.isFavorite && window.isFavorite(game.id);
    function escapeHtml(text) {
      const div = document.createElement('div');
      div.textContent = text;
      return div.innerHTML;
    }
    
    const title = escapeHtml(game.title);
    const desc = escapeHtml(game.description);
    const category = escapeHtml(game.category);
    const gameId = escapeHtml(game.id);
    const image = escapeHtml(game.image);
    const url = escapeHtml(game.url);
    
    card.innerHTML = `
      <img src="${image}" alt="${title}" class="game-image" loading="lazy" />
      <div class="game-preview">
        <h4>${title}</h4>
        <p>${desc}</p>
      </div>
      <h3>${title}</h3>
      <p>${desc}</p>
      <span class="category">${category}</span>
      <div class="game-buttons">
        <button class="favorite-btn ${isFav ? 'active' : ''}" data-game-id="${gameId}" data-game-title="${title}" aria-label="Toggle favorite">${isFav ? '✕' : '⭐'}</button>
        <button class="play-inside-btn">
          ${game.gooseblock ? 'Open in New Tab' : 'Play'}
        </button>
        <a href="${url}" target="_blank" rel="noopener noreferrer" class="external-link">
          Open in New Tab
        </a>
      </div>
    `;
    gameList.appendChild(card);

    const playButton = card.querySelector('.play-inside-btn');
    if (playButton) {
      playButton.addEventListener('click', () => {
        if (game.gooseblock) {
          window.open(game.url, '_blank', 'noopener,noreferrer');
        } else {
          openGameInIframe(game.url, game.title);
        }
      });
    }
    
    const favButton = card.querySelector('.favorite-btn');
    if (favButton && typeof window !== 'undefined' && window.toggleFavorite) {
      favButton.addEventListener('click', (e) => {
        e.stopPropagation();
        const isNowFav = window.toggleFavorite(game.id, game.title);
        favButton.classList.toggle('active', isNowFav);
        favButton.textContent = isNowFav ? '✕' : '⭐';
        
        favButton.classList.add('favorite-animate');
        setTimeout(() => {
          favButton.classList.remove('favorite-animate');
        }, 600);
        
        updateFavoritesCount();
      });
    }
  });
}

const searchInput = document.getElementById('game-search');
if (searchInput) {
  const debouncedSearch = debounce((e) => {
    const query = e.target.value.toLowerCase();
    const filtered = allGames.filter(g => g.title.toLowerCase().includes(query));
    displayGames(filtered);
  }, 300);
  searchInput.addEventListener('input', debouncedSearch);
}

function openGameInIframe(url, title) {
  let frameContainer = document.getElementById('game-iframe-container');
  if (frameContainer) frameContainer.remove();

  frameContainer = document.createElement('div');
  frameContainer.id = 'game-iframe-container';
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
  
  const safeTitle = escapeHtml(title);
  const safeUrl = escapeHtml(url);
  frameContainer.innerHTML = `
    <div class="iframe-header">
      <span>${safeTitle}</span>
      <button id="close-iframe-btn">✖</button>
    </div>
    <iframe src="${safeUrl}" allowfullscreen></iframe>
  `;

  document.body.appendChild(frameContainer);
  const closeBtn = document.getElementById('close-iframe-btn');
  if (closeBtn) {
    closeBtn.onclick = () => frameContainer.remove();
  }
}

if (typeof window !== 'undefined') {
  window.displayGames = displayGames;
  window.allGames = allGames;
  window.updateFavoritesCount = updateFavoritesCount;
  window.openGameInIframe = openGameInIframe;
}
