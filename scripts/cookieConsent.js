function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

function setCookie(name, value, days) {
  const date = new Date();
  date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
  const expires = `expires=${date.toUTCString()}`;
  document.cookie = `${name}=${value};${expires};path=/`;
}

function createCookieConsent() {
  if (getCookie('cookieConsent')) {
    return;
  }

  const overlay = document.createElement('div');
  overlay.id = 'cookie-consent-overlay';
  overlay.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 99999;
    animation: fadeIn 0.3s ease;
  `;

  function getThemeColors() {
    const body = document.body;
    if (body.classList.contains('theme-midnight')) {
      return {
        bg: 'rgb(20, 20, 40)',
        text: 'rgb(255, 255, 255)',
        heading: 'rgb(255, 255, 255)',
        desc: 'rgb(200, 200, 200)',
        accept: '#7b57ff',
        decline: 'rgb(100, 100, 100)'
      };
    } else if (body.classList.contains('theme-dark')) {
      return {
        bg: 'rgb(20, 20, 20)',
        text: 'rgb(255, 255, 255)',
        heading: 'rgb(255, 255, 255)',
        desc: 'rgb(200, 200, 200)',
        accept: '#7b57ff',
        decline: 'rgb(100, 100, 100)'
      };
    } else if (body.classList.contains('theme-vista')) {
      return {
        bg: 'rgba(255, 255, 255, 0.95)',
        text: 'rgb(26, 26, 26)',
        heading: 'rgb(26, 26, 26)',
        desc: 'rgb(99, 99, 99)',
        accept: '#0078d4',
        decline: 'rgb(218, 218, 218)'
      };
    } else if (body.classList.contains('theme-cyberpunk')) {
      return {
        bg: 'rgb(26, 0, 51)',
        text: 'rgb(0, 255, 255)',
        heading: 'rgb(0, 255, 255)',
        desc: 'rgb(150, 255, 255)',
        accept: '#00ffff',
        decline: 'rgb(50, 0, 100)'
      };
    } else if (body.classList.contains('theme-aurora')) {
      return {
        bg: 'rgba(26, 31, 58, 0.95)',
        text: 'rgb(224, 255, 232)',
        heading: 'rgb(0, 255, 136)',
        desc: 'rgb(200, 255, 220)',
        accept: '#00ff88',
        decline: 'rgb(50, 60, 80)'
      };
    } else {
      return {
        bg: 'rgb(255, 255, 255)',
        text: 'rgb(26, 26, 26)',
        heading: 'rgb(26, 26, 26)',
        desc: 'rgb(99, 99, 99)',
        accept: '#7b57ff',
        decline: 'rgb(218, 218, 218)'
      };
    }
  }

  const themeColors = getThemeColors();

  const card = document.createElement('div');
  card.className = 'cookie-consent-card';
  card.style.cssText = `
    width: 300px;
    min-height: 220px;
    background-color: ${themeColors.bg};
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px 30px;
    gap: 13px;
    position: relative;
    overflow: hidden;
    box-shadow: 2px 2px 20px rgba(0, 0, 0, 0.5);
    border-radius: 15px;
    animation: slideUp 0.4s ease;
    backdrop-filter: blur(10px);
  `;

  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.id = 'cookieSvg';
  svg.setAttribute('version', '1.1');
  svg.setAttribute('viewBox', '0 0 122.88 122.25');
  svg.style.cssText = 'width: 50px;';
  const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  path.setAttribute('d', 'M101.77,49.38c2.09,3.1,4.37,5.11,6.86,5.78c2.45,0.66,5.32,0.06,8.7-2.01c1.36-0.84,3.14-0.41,3.97,0.95 c0.28,0.46,0.42,0.96,0.43,1.47c0.13,1.4,0.21,2.82,0.24,4.26c0.03,1.46,0.02,2.91-0.05,4.35h0v0c0,0.13-0.01,0.26-0.03,0.38 c-0.91,16.72-8.47,31.51-20,41.93c-11.55,10.44-27.06,16.49-43.82,15.69v0.01h0c-0.13,0-0.26-0.01-0.38-0.03 c-16.72-0.91-31.51-8.47-41.93-20C5.31,90.61-0.73,75.1,0.07,58.34H0.07v0c0-0.13,0.01-0.26,0.03-0.38 C1,41.22,8.81,26.35,20.57,15.87C32.34,5.37,48.09-0.73,64.85,0.07V0.07h0c1.6,0,2.89,1.29,2.89,2.89c0,0.4-0.08,0.78-0.23,1.12 c-1.17,3.81-1.25,7.34-0.27,10.14c0.89,2.54,2.7,4.51,5.41,5.52c1.44,0.54,2.2,2.1,1.74,3.55l0.01,0 c-1.83,5.89-1.87,11.08-0.52,15.26c0.82,2.53,2.14,4.69,3.88,6.4c1.74,1.72,3.9,3,6.39,3.78c4.04,1.26,8.94,1.18,14.31-0.55 C99.73,47.78,101.08,48.3,101.77,49.38L101.77,49.38z M59.28,57.86c2.77,0,5.01,2.24,5.01,5.01c0,2.77-2.24,5.01-5.01,5.01 c-2.77,0-5.01-2.24-5.01-5.01C54.27,60.1,56.52,57.86,59.28,57.86L59.28,57.86z M37.56,78.49c3.37,0,6.11,2.73,6.11,6.11 s-2.73,6.11-6.11,6.11s-6.11-2.73-6.11-6.11S34.18,78.49,37.56,78.49L37.56,78.49z M50.72,31.75c2.65,0,4.79,2.14,4.79,4.79 c0,2.65-2.14,4.79-4.79,4.79c-2.65,0-4.79-2.14-4.79-4.79C45.93,33.89,48.08,31.75,50.72,31.75L50.72,31.75z M119.3,32.4 c1.98,0,3.58,1.6,3.58,3.58c0,1.98-1.6,3.58-3.58,3.58s-3.58-1.6-3.58-3.58C115.71,34.01,117.32,32.4,119.3,32.4L119.3,32.4z M93.62,22.91c2.98,0,5.39,2.41,5.39,5.39c0,2.98-2.41,5.39-5.39,5.39c-2.98,0-5.39-2.41-5.39-5.39 C88.23,25.33,90.64,22.91,93.62,22.91L93.62,22.91z M97.79,0.59c3.19,0,5.78,2.59,5.78,5.78c0,3.19-2.59,5.78-5.78,5.78 c-3.19,0-5.78-2.59-5.78-5.78C92.02,3.17,94.6,0.59,97.79,0.59L97.79,0.59z M76.73,80.63c4.43,0,8.03,3.59,8.03,8.03 c0,4.43-3.59,8.03-8.03,8.03s-8.03-3.59-8.03-8.03C68.7,84.22,72.29,80.63,76.73,80.63L76.73,80.63z M31.91,46.78 c4.8,0,8.69,3.89,8.69,8.69c0,4.8-3.89,8.69-8.69,8.69s-8.69-3.89-8.69-8.69C23.22,50.68,27.11,46.78,31.91,46.78L31.91,46.78z M107.13,60.74c-3.39-0.91-6.35-3.14-8.95-6.48c-5.78,1.52-11.16,1.41-15.76-0.02c-3.37-1.05-6.32-2.81-8.71-5.18 c-2.39-2.37-4.21-5.32-5.32-8.75c-1.51-4.66-1.69-10.2-0.18-16.32c-3.1-1.8-5.25-4.53-6.42-7.88c-1.06-3.05-1.28-6.59-0.61-10.35 C47.27,5.95,34.3,11.36,24.41,20.18C13.74,29.69,6.66,43.15,5.84,58.29l0,0.05v0h0l-0.01,0.13v0C5.07,73.72,10.55,87.82,20.02,98.3 c9.44,10.44,22.84,17.29,38,18.1l0.05,0h0v0l0.13,0.01h0c15.24,0.77,29.35-4.71,39.83-14.19c10.44-9.44,17.29-22.84,18.1-38l0-0.05 v0h0l0.01-0.13v0c0.07-1.34,0.09-2.64,0.06-3.91C112.98,61.34,109.96,61.51,107.13,60.74L107.13,60.74z M116.15,64.04L116.15,64.04 L116.15,64.04L116.15,64.04z M58.21,116.42L58.21,116.42L58.21,116.42L58.21,116.42z');
  const cookieColor = themeColors.bg === 'rgb(255, 255, 255)' || themeColors.bg === 'rgba(255, 255, 255, 0.95)' ? 'rgb(97, 81, 81)' : themeColors.text;
  path.style.fill = cookieColor;
  const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  g.appendChild(path);
  svg.appendChild(g);

  const heading = document.createElement('p');
  heading.className = 'cookieHeading';
  heading.textContent = 'We use cookies.';
  heading.style.cssText = `font-size: 1.2em; font-weight: 800; color: ${themeColors.heading}; margin: 0;`;

  const description = document.createElement('p');
  description.className = 'cookieDescription';
  description.textContent = 'This website uses cookies to ensure you get the best experience on our site.';
  description.style.cssText = `text-align: center; font-size: 0.7em; font-weight: 600; color: ${themeColors.desc}; margin: 0;`;

  const buttonContainer = document.createElement('div');
  buttonContainer.className = 'buttonContainer';
  buttonContainer.style.cssText = 'display: flex; gap: 20px; flex-direction: row;';

  const acceptButton = document.createElement('button');
  acceptButton.className = 'acceptButton';
  acceptButton.textContent = 'Allow';
  const acceptHover = themeColors.accept === '#7b57ff' ? '#9173ff' : 
                      themeColors.accept === '#0078d4' ? '#106ebe' :
                      themeColors.accept === '#00ffff' ? '#00cccc' :
                      themeColors.accept === '#00ff88' ? '#00cc6a' : themeColors.accept;
  acceptButton.style.cssText = `
    width: 80px;
    height: 30px;
    background-color: ${themeColors.accept};
    transition-duration: .2s;
    border: none;
    color: ${themeColors.accept === '#00ffff' || themeColors.accept === '#00ff88' ? 'rgb(0, 0, 0)' : 'rgb(241, 241, 241)'};
    cursor: pointer;
    font-weight: 600;
    border-radius: 20px;
  `;

  const declineButton = document.createElement('button');
  declineButton.className = 'declineButton';
  declineButton.textContent = 'Decline';
  const declineHover = themeColors.decline === 'rgb(218, 218, 218)' ? '#ebebeb' : 
                       themeColors.decline === 'rgb(100, 100, 100)' ? 'rgb(120, 120, 120)' :
                       themeColors.decline === 'rgb(50, 0, 100)' ? 'rgb(70, 0, 130)' :
                       themeColors.decline === 'rgb(50, 60, 80)' ? 'rgb(70, 80, 100)' : themeColors.decline;
  declineButton.style.cssText = `
    width: 80px;
    height: 30px;
    background-color: ${themeColors.decline};
    transition-duration: .2s;
    color: ${themeColors.decline === 'rgb(218, 218, 218)' ? 'rgb(46, 46, 46)' : themeColors.text};
    border: none;
    cursor: pointer;
    font-weight: 600;
    border-radius: 20px;
  `;

  acceptButton.addEventListener('mouseenter', () => {
    acceptButton.style.backgroundColor = acceptHover;
  });
  acceptButton.addEventListener('mouseleave', () => {
    acceptButton.style.backgroundColor = themeColors.accept;
  });

  declineButton.addEventListener('mouseenter', () => {
    declineButton.style.backgroundColor = declineHover;
  });
  declineButton.addEventListener('mouseleave', () => {
    declineButton.style.backgroundColor = themeColors.decline;
  });

  acceptButton.addEventListener('click', () => {
    setCookie('cookieConsent', 'accepted', 365);
    overlay.style.animation = 'fadeOut 0.3s ease';
    setTimeout(() => {
      overlay.remove();
      document.body.style.overflow = '';
    }, 300);
  });

  declineButton.addEventListener('click', () => {
    setCookie('cookieConsent', 'declined', 365);
    overlay.style.animation = 'fadeOut 0.3s ease';
    setTimeout(() => {
      overlay.remove();
      document.body.style.overflow = '';
    }, 300);
  });

  buttonContainer.appendChild(acceptButton);
  buttonContainer.appendChild(declineButton);

  card.appendChild(svg);
  card.appendChild(heading);
  card.appendChild(description);
  card.appendChild(buttonContainer);

  overlay.appendChild(card);

  const style = document.createElement('style');
  style.id = 'cookie-consent-styles';
  style.textContent = `
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    @keyframes fadeOut {
      from { opacity: 1; }
      to { opacity: 0; }
    }
    @keyframes slideUp {
      from { transform: translateY(20px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }
    body.cookie-consent-active {
      overflow: hidden;
    }
    .cookie-consent-card {
      animation: slideUp 0.4s ease;
    }
  `;
  document.head.appendChild(style);

  document.body.appendChild(overlay);
  document.body.style.overflow = 'hidden';
  document.body.classList.add('cookie-consent-active');
}

function initCookieConsent() {
  if (getCookie('cookieConsent')) {
    return;
  }
  setTimeout(() => {
    if (typeof window.loadTheme === 'function') {
      window.loadTheme();
    }
    setTimeout(createCookieConsent, 300);
  }, 200);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initCookieConsent);
} else {
  initCookieConsent();
}

