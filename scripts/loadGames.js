let allGames = [];

fetch('../scripts/games.json')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok ' + response.statusText);
    }
    return response.json();
  })
  .then(games => {
    allGames = games;
    displayGames(allGames);
  })
  .catch(error => console.error('Error loading games:', error));

function displayGames(games) {
  const gameCountElem = document.getElementById('game-count');
  if (gameCountElem) {
    gameCountElem.textContent = `Games Found: ${games.length}`;
  }

  const gameList = document.getElementById('game-list');
  gameList.innerHTML = '';

  games.forEach(game => {
    const gameCard = document.createElement('div');
    gameCard.className = 'game-card';

    gameCard.innerHTML = `
      <img src="${game.image}" alt="${game.title}" class="game-image" />
      <h3>${game.title}</h3>
      <p>${game.description}</p>
      <div class="game-buttons">
        <button class="play-inside-btn">Play</button>
        <a href="${game.url}" target="_blank" rel="noopener noreferrer" class="external-link">Open in New Tab</a>
      </div>
    `;

    gameList.appendChild(gameCard);

    const playButton = gameCard.querySelector('.play-inside-btn');
    playButton.addEventListener('click', () => {
      openGameInIframe(game.url, game.title);
    });
  });
}


const searchInput = document.getElementById('game-search');
if (searchInput) {
  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase();
    const filteredGames = allGames.filter(game => game.title.toLowerCase().includes(query));
    displayGames(filteredGames);
  });
}


const sortBtn = document.getElementById('sort-alpha-btn');
if (sortBtn) {
  sortBtn.addEventListener('click', () => {
    const sortedGames = [...allGames].sort((a, b) => a.title.localeCompare(b.title));
    displayGames(sortedGames);
  });
}

function openGameInIframe(url, title) {
  let existingFrame = document.getElementById('game-iframe-container');
  if (existingFrame) existingFrame.remove();

  const container = document.createElement('div');
  container.id = 'game-iframe-container';
  container.innerHTML = `
    <div class="iframe-header">
      <span>${title}</span>
      <button id="close-iframe-btn">✖</button>
    </div>
    <iframe src="${url}" allowfullscreen></iframe>
  `;

  document.body.appendChild(container);

  document.getElementById('close-iframe-btn').onclick = () => {
    container.remove();
  };
}
