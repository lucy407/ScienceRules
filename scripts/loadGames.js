let allGames = [];
let allCategories = new Set();

fetch('../scripts/games.json')
  .then(res => {
    if (!res.ok) throw new Error('Failed to load games.json');
    return res.json();
  })
  .then(games => {
    allGames = games;
    games.forEach(g => { if (g.category) allCategories.add(g.category); });
    setupSortDropdown();
    displayGames(allGames);
  })
  .catch(err => console.error('Error loading games:', err));

function setupSortDropdown() {
  const dropdown = document.getElementById('sort-dropdown');
  dropdown.innerHTML = '';

  const baseOptions = ['A-Z', 'Newest', 'Oldest'];
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
  let sorted = [...allGames];

  if (sortType === 'A-Z') {
    sorted.sort((a, b) => a.title.localeCompare(b.title));
  } else if (sortType === 'Newest') {
    sorted = sorted.reverse();
  } else if (sortType === 'Oldest') {
  } else {
    sorted = allGames.filter(g => g.category === sortType);
  }

  displayGames(sorted);
}

function displayGames(games) {
  const gameCountElem = document.getElementById('game-count');
  gameCountElem.textContent = `${games.length}`;

  const gameList = document.getElementById('game-list');
  gameList.innerHTML = '';

  games.forEach(game => {
    const card = document.createElement('div');
    card.className = 'game-card';
    card.innerHTML = `
      <img src="${game.image}" alt="${game.title}" class="game-image" />
      <h3>${game.title}</h3>
      <p>${game.description}</p>
      <div class="game-buttons">
        <button class="play-inside-btn">Play</button>
        <a href="${game.url}" target="_blank" rel="noopener noreferrer" class="external-link">Open in New Tab</a>
      </div>
    `;
    gameList.appendChild(card);

    card.querySelector('.play-inside-btn').addEventListener('click', () => {
      openGameInIframe(game.url, game.title);
    });
  });
}

const searchInput = document.getElementById('game-search');
if (searchInput) {
  searchInput.addEventListener('input', e => {
    const query = e.target.value.toLowerCase();
    const filtered = allGames.filter(g => g.title.toLowerCase().includes(query));
    displayGames(filtered);
  });
}

function openGameInIframe(url, title) {
  let frameContainer = document.getElementById('game-iframe-container');
  if (frameContainer) frameContainer.remove();

  frameContainer = document.createElement('div');
  frameContainer.id = 'game-iframe-container';
  frameContainer.innerHTML = `
    <div class="iframe-header">
      <span>${title}</span>
      <button id="close-iframe-btn">✖</button>
    </div>
    <iframe src="${url}" allowfullscreen></iframe>
  `;

  document.body.appendChild(frameContainer);
  document.getElementById('close-iframe-btn').onclick = () => frameContainer.remove();
}
