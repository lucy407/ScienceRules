const servers = [
  'https://player.videasy.net/movie/',
  'https://multiembed.mov/?tmdb=1&video_id=',
  'https://vidlink.pro/',
  'https://vidsrc.rip/embed/movie/',
  'https://moviesapi.to/movie/',
  'https://moviesapi.club/movie/',
  'https://player.smashy.stream/movie/',
  'https://iframe.pstream.mov/media/tmdb-movie-',
  'https://vidsrc.xyz/embed/movie?tmdb=',
  'https://vidsrc.icu/embed/movie/'
];

const API_KEY = '93297ba3ed6357c086bc0c033b4bf7aa';

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

async function getMovieDetails(tmdbId, type = 'movie') {
  try {
    const response = await fetch(`https://api.themoviedb.org/3/${type}/${tmdbId}?api_key=${API_KEY}`);
    if (!response.ok) throw new Error('Failed to fetch movie details');
    return await response.json();
  } catch (err) {
    console.error('Error fetching movie details:', err);
    return null;
  }
}

async function fetchMovieLinks(tmdbId) {
  const movieDetails = await getMovieDetails(tmdbId);
  if (!movieDetails) return null;
  
  const title = movieDetails.title || movieDetails.name;
  const year = (movieDetails.release_date || movieDetails.first_air_date || '????').split('-')[0];

  const links = servers.map(server => {
    if (server.includes('tmdb=')) return server + tmdbId;
    if (server.includes('tmdb-movie-')) return server + tmdbId;
    return server + encodeURIComponent(`${title} ${year}`);
  });

  return { movieDetails, links };
}

function clearMovies() {
  const list = document.getElementById('movie-list');
  if (list) list.innerHTML = '';
  const count = document.getElementById('result-count');
  if (count) count.textContent = '';
}

async function displayMovies(ids, totalResults, type = 'movie') {
  const movieListElement = document.getElementById('movie-list');
  if (!movieListElement) return;
  clearMovies();

  const promises = ids.map(tmdbId => fetchMovieLinks(tmdbId));
  const results = await Promise.allSettled(promises);

  results.forEach((result, index) => {
    if (result.status === 'fulfilled' && result.value) {
      const { movieDetails, links } = result.value;

      const movieDiv = document.createElement('div');
      movieDiv.classList.add('movie');

      const poster = document.createElement('img');
      poster.src = movieDetails.poster_path ? `https://image.tmdb.org/t/p/w500${movieDetails.poster_path}` : '';
      poster.alt = movieDetails.title || movieDetails.name;
      poster.loading = 'lazy';
      movieDiv.appendChild(poster);

      const contentDiv = document.createElement('div');
      contentDiv.classList.add('movie-content');

      const title = document.createElement('h3');
      title.textContent = movieDetails.title || movieDetails.name;
      contentDiv.appendChild(title);

      const year = document.createElement('p');
      year.classList.add('year');
      const date = movieDetails.release_date || movieDetails.first_air_date;
      year.textContent = `Release Year: ${date ? date.split('-')[0] : 'Unknown'}`;
      contentDiv.appendChild(year);

      const overview = document.createElement('div');
      overview.classList.add('read-more-content');
      overview.textContent = movieDetails.overview || 'No description available.';
      contentDiv.appendChild(overview);

      const readMore = document.createElement('span');
      readMore.classList.add('read-more-toggle');
      readMore.textContent = 'Read more..';
      readMore.addEventListener('click', () => {
        overview.classList.toggle('expanded');
        readMore.textContent = overview.classList.contains('expanded') ? 'Read less..' : 'Read more..';
      });
      contentDiv.appendChild(readMore);

      const linksDiv = document.createElement('div');
      linksDiv.classList.add('links');
      links.forEach((link, i) => {
        const a = document.createElement('a');
        a.href = link;
        a.target = '_blank';
        a.rel = 'noopener noreferrer';
        a.textContent = `Server ${i + 1}`;
        linksDiv.appendChild(a);
      });
      contentDiv.appendChild(linksDiv);

      movieDiv.appendChild(contentDiv);
      movieListElement.appendChild(movieDiv);
    }
  });

  const resultCount = document.getElementById('result-count');
  if (resultCount) resultCount.textContent = `Found ${totalResults} results`;
}

async function fetchPageResults(url) {
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch results');
    const data = await res.json();
    const ids = data.results.map(m => m.id);
    return { ids, total: data.total_results };
  } catch (err) {
    console.error('Error fetching page results:', err);
    return { ids: [], total: 0 };
  }
}

async function fetchPopular(type = 'movie') {
  return fetchPageResults(`https://api.themoviedb.org/3/${type}/popular?api_key=${API_KEY}&page=1`);
}

async function searchMovies(query, type = 'movie') {
  return fetchPageResults(`https://api.themoviedb.org/3/search/${type}?query=${encodeURIComponent(query)}&api_key=${API_KEY}&page=1`);
}

document.addEventListener('DOMContentLoaded', async () => {
  let currentType = 'movie';
  let { ids, total } = await fetchPopular(currentType);
  await displayMovies(ids, total, currentType);

  const searchInput = document.getElementById('search-input');
  if (searchInput) {
    const debouncedSearch = debounce(async () => {
      const query = searchInput.value.trim();
      if (query) {
        const { ids, total } = await searchMovies(query, currentType);
        await displayMovies(ids, total, currentType);
      } else {
        const { ids, total } = await fetchPopular(currentType);
        await displayMovies(ids, total, currentType);
      }
    }, 300);
    searchInput.addEventListener('input', debouncedSearch);
  }

  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const type = btn.dataset.type;
      currentType = type === 'popular' ? 'movie' : type;
      const { ids, total } = await fetchPopular(currentType);
      await displayMovies(ids, total, currentType);
    });
  });
});
