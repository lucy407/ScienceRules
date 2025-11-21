const themes = {
  default: {
    name: 'Classic',
    type: 'normal',
    colors: {
      primary: '#5ac8fa',
      background: 'linear-gradient(145deg, #0c0d11, #181b23)',
      cardBg: '#1a1c22',
      text: '#e0e0e0',
      headerBg: 'rgba(20, 20, 25, 0.85)',
      navBg: '#16171b'
    }
  },
  dark: {
    name: 'Void Black',
    type: 'normal',
    colors: {
      primary: '#ffffff',
      background: 'linear-gradient(145deg, #000000, #1a1a1a)',
      cardBg: '#0d0d0d',
      text: '#ffffff',
      headerBg: 'rgba(0, 0, 0, 0.9)',
      navBg: '#0a0a0a'
    }
  },
  purple: {
    name: 'Mystic Purple',
    type: 'normal',
    colors: {
      primary: '#a855f7',
      background: 'linear-gradient(145deg, #1a0b2e, #2d1b4e)',
      cardBg: '#2a1f3d',
      text: '#e9d5ff',
      headerBg: 'rgba(26, 11, 46, 0.85)',
      navBg: 'rgba(26, 11, 46, 0.9)'
    }
  },
  green: {
    name: 'Emerald Forest',
    type: 'normal',
    colors: {
      primary: '#10b981',
      background: 'linear-gradient(145deg, #064e3b, #065f46)',
      cardBg: '#0d4f3f',
      text: '#d1fae5',
      headerBg: 'rgba(6, 78, 59, 0.85)',
      navBg: 'rgba(6, 78, 59, 0.9)'
    }
  },
  red: {
    name: 'Crimson Night',
    type: 'normal',
    colors: {
      primary: '#ef4444',
      background: 'linear-gradient(145deg, #7f1d1d, #991b1b)',
      cardBg: '#991b1b',
      text: '#fee2e2',
      headerBg: 'rgba(127, 29, 29, 0.85)',
      navBg: 'rgba(127, 29, 29, 0.9)'
    }
  },
  vista: {
    name: 'Windows 7 Aero',
    type: 'animated',
    colors: {
      primary: '#0078d4',
      background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 25%, #7e8ba3 50%, #2a5298 75%, #1e3c72 100%)',
      cardBg: 'rgba(255, 255, 255, 0.15)',
      text: '#ffffff',
      headerBg: 'rgba(30, 60, 114, 0.4)',
      navBg: 'rgba(42, 82, 152, 0.6)',
      animation: 'vistaGradient 10s ease infinite'
    }
  },
  midnight: {
    name: 'Midnight Starlight',
    type: 'animated',
    colors: {
      primary: '#ffffff',
      background: '#000000',
      cardBg: 'rgba(20, 20, 40, 0.8)',
      text: '#ffffff',
      headerBg: 'rgba(0, 0, 0, 0.9)',
      navBg: 'rgba(0, 0, 0, 0.8)',
      animation: 'starfield 20s linear infinite'
    }
  },
  cyberpunk: {
    name: 'Neon Cyberpunk',
    type: 'animated',
    colors: {
      primary: '#00ffff',
      background: 'linear-gradient(135deg, #000000 0%, #1a0033 50%, #000000 100%)',
      cardBg: 'rgba(26, 0, 51, 0.9)',
      text: '#00ffff',
      headerBg: 'rgba(0, 0, 0, 0.9)',
      navBg: 'rgba(26, 0, 51, 0.8)',
      animation: 'cyberPulse 3s ease-in-out infinite'
    }
  },
  aurora: {
    name: 'Northern Lights',
    type: 'animated',
    colors: {
      primary: '#00ff88',
      background: 'linear-gradient(135deg, #0a0e27 0%, #1a1f3a 25%, #2d1b4e 50%, #1a1f3a 75%, #0a0e27 100%)',
      cardBg: 'rgba(26, 31, 58, 0.8)',
      text: '#e0ffe8',
      headerBg: 'rgba(10, 14, 39, 0.9)',
      navBg: 'rgba(26, 31, 58, 0.7)',
      animation: 'aurora 12s ease infinite'
    }
  }
};

let currentTheme = 'default';

function loadTheme() {
  try {
    const saved = localStorage.getItem('siteTheme');
    if (saved && themes[saved]) {
      currentTheme = saved;
    }
  } catch (e) {
    console.error('Failed to load theme:', e);
  }
  applyTheme(currentTheme);
}

function saveTheme(themeName) {
  try {
    localStorage.setItem('siteTheme', themeName);
    currentTheme = themeName;
  } catch (e) {
    console.error('Failed to save theme:', e);
  }
}

function createStarfield() {
  const existing = document.getElementById('starfield-canvas');
  if (existing) existing.remove();
  
  if (!document.body.classList.contains('theme-midnight')) {
    return;
  }
  
  const canvas = document.createElement('canvas');
  canvas.id = 'starfield-canvas';
  canvas.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    z-index: 0;
  `;
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  
  document.body.insertBefore(canvas, document.body.firstChild);
  
  const ctx = canvas.getContext('2d');
  const stars = [];
  const starCount = 200;
  
  for (let i = 0; i < starCount; i++) {
    stars.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      radius: Math.random() * 1.5 + 0.5,
      opacity: Math.random() * 0.8 + 0.2,
      speed: Math.random() * 0.5 + 0.1
    });
  }
  
  let animationId = null;
  
  function animate() {
    if (!document.body.classList.contains('theme-midnight') || !canvas.parentNode) {
      if (animationId) cancelAnimationFrame(animationId);
      canvas.remove();
      return;
    }
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    stars.forEach(star => {
      star.y += star.speed;
      if (star.y > canvas.height) {
        star.y = 0;
        star.x = Math.random() * canvas.width;
      }
      
      star.opacity += (Math.random() > 0.5 ? 0.02 : -0.02);
      if (star.opacity > 1) star.opacity = 1;
      if (star.opacity < 0.2) star.opacity = 0.2;
      
      ctx.beginPath();
      ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255, 255, 255, ${star.opacity})`;
      ctx.fill();
    });
    
    animationId = requestAnimationFrame(animate);
  }
  
  animate();
  
  const resizeHandler = () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  };
  window.addEventListener('resize', resizeHandler);
}

function applyTheme(themeName) {
  if (!themes[themeName]) return;
  
  const theme = themes[themeName];
  const root = document.documentElement;
  
  root.style.setProperty('--theme-primary', theme.colors.primary);
  root.style.setProperty('--theme-bg', theme.colors.background);
  root.style.setProperty('--theme-card-bg', theme.colors.cardBg);
  root.style.setProperty('--theme-text', theme.colors.text);
  root.style.setProperty('--theme-header-bg', theme.colors.headerBg);
  
  const existingAnimation = document.getElementById('theme-animation');
  if (existingAnimation) existingAnimation.remove();
  
  const existingStarfield = document.getElementById('starfield-canvas');
  if (existingStarfield) {
    if (themeName !== 'midnight') {
      existingStarfield.remove();
    }
  }
  
  if (theme.type === 'animated') {
    const style = document.createElement('style');
    style.id = 'theme-animation';
    
    if (themeName === 'vista') {
      style.textContent = `
        @keyframes vistaGradient {
          0% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
          100% { background-position: 0% 50%; }
        }
        @keyframes vistaShine {
          0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
          100% { transform: translateX(200%) translateY(200%) rotate(45deg); }
        }
        body.theme-vista {
          background: linear-gradient(135deg, #1e3c72 0%, #2a5298 25%, #7e8ba3 50%, #2a5298 75%, #1e3c72 100%);
          background-size: 400% 400%;
          animation: vistaGradient 10s ease infinite;
        }
        body.theme-vista::before {
          content: '';
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.1) 50%, transparent 70%);
          animation: vistaShine 8s linear infinite;
          pointer-events: none;
          z-index: 0;
        }
        body.theme-vista > * {
          position: relative;
          z-index: 1;
        }
        body.theme-vista .game-card,
        body.theme-vista .carousel-image-container,
        body.theme-vista .movie {
          backdrop-filter: blur(20px) saturate(180%);
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2);
          border: 1px solid rgba(255, 255, 255, 0.1);
        }
        body.theme-vista nav {
          background: rgba(42, 82, 152, 0.6) !important;
          backdrop-filter: blur(20px) saturate(180%);
          box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        body.theme-vista nav a:hover {
          background: rgba(0, 120, 212, 0.4) !important;
          box-shadow: 0 0 15px rgba(0, 120, 212, 0.5);
        }
      `;
    } else if (themeName === 'midnight') {
      style.textContent = `
        @keyframes starfield {
          0% { opacity: 1; }
          50% { opacity: 0.8; }
          100% { opacity: 1; }
        }
        body.theme-midnight {
          background: #000000 !important;
          position: relative;
        }
        body.theme-midnight::before {
          content: '';
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.15) 0%, transparent 50%),
                      radial-gradient(circle at 80% 80%, rgba(255, 119, 198, 0.15) 0%, transparent 50%);
          pointer-events: none;
          z-index: 0;
          animation: starfield 4s ease-in-out infinite;
        }
        body.theme-midnight > * {
          position: relative;
          z-index: 1;
        }
        body.theme-midnight nav {
          background: rgba(0, 0, 0, 0.7) !important;
          backdrop-filter: blur(10px);
          box-shadow: 0 2px 10px rgba(255, 255, 255, 0.1);
        }
        body.theme-midnight nav a {
          color: #ffffff !important;
        }
        body.theme-midnight nav a:hover {
          background: rgba(255, 255, 255, 0.2) !important;
          box-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
          color: #ffffff !important;
        }
        #starfield-canvas {
          z-index: 0 !important;
        }
      `;
      document.head.appendChild(style);
    } else if (themeName === 'cyberpunk') {
      style.textContent = `
        @keyframes cyberPulse {
          0%, 100% { 
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.5),
                        0 0 40px rgba(0, 255, 255, 0.3),
                        inset 0 0 20px rgba(0, 255, 255, 0.1);
          }
          50% { 
            box-shadow: 0 0 40px rgba(0, 255, 255, 0.8),
                        0 0 80px rgba(0, 255, 255, 0.6),
                        inset 0 0 40px rgba(0, 255, 255, 0.2);
          }
        }
        @keyframes cyberGradient {
          0% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
          100% { background-position: 0% 50%; }
        }
        @keyframes cyberScan {
          0% { transform: translateY(-100%); opacity: 0; }
          50% { opacity: 0.3; }
          100% { transform: translateY(100vh); opacity: 0; }
        }
        body.theme-cyberpunk {
          background: linear-gradient(135deg, #000000 0%, #1a0033 50%, #000000 100%);
          background-size: 200% 200%;
          animation: cyberGradient 10s ease infinite;
          position: relative;
        }
        body.theme-cyberpunk::before {
          content: '';
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 2px;
          background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.5), transparent);
          animation: cyberScan 4s linear infinite;
          pointer-events: none;
          z-index: 0;
        }
        body.theme-cyberpunk > * {
          position: relative;
          z-index: 1;
        }
        body.theme-cyberpunk nav {
          background: rgba(26, 0, 51, 0.8) !important;
          backdrop-filter: blur(10px);
          box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
        }
        body.theme-cyberpunk nav a:hover,
        body.theme-cyberpunk .game-card:hover,
        body.theme-cyberpunk button:hover {
          animation: cyberPulse 3s ease-in-out infinite;
        }
        body.theme-cyberpunk nav a:hover {
          background: rgba(0, 255, 255, 0.3) !important;
          box-shadow: 0 0 20px rgba(0, 255, 255, 0.6);
        }
      `;
    } else if (themeName === 'aurora') {
      style.textContent = `
        @keyframes aurora {
          0% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
          100% { background-position: 0% 50%; }
        }
        @keyframes auroraWave {
          0%, 100% { transform: translateY(0) scale(1); opacity: 0.6; }
          50% { transform: translateY(-20px) scale(1.1); opacity: 0.9; }
        }
        body.theme-aurora {
          background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 25%, #2d1b4e 50%, #1a1f3a 75%, #0a0e27 100%);
          background-size: 400% 400%;
          animation: aurora 12s ease infinite;
        }
        body.theme-aurora::before {
          content: '';
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: 
            radial-gradient(ellipse at 20% 30%, rgba(0, 255, 136, 0.2) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 70%, rgba(0, 200, 255, 0.2) 0%, transparent 50%);
          pointer-events: none;
          z-index: 0;
          animation: auroraWave 8s ease-in-out infinite;
        }
        body.theme-aurora::after {
          content: '';
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: 
            radial-gradient(ellipse at 50% 50%, rgba(0, 255, 136, 0.1) 0%, transparent 70%);
          pointer-events: none;
          z-index: 0;
          animation: auroraWave 10s ease-in-out infinite reverse;
        }
        body.theme-aurora > * {
          position: relative;
          z-index: 1;
        }
        body.theme-aurora nav {
          background: rgba(26, 31, 58, 0.7) !important;
          backdrop-filter: blur(10px);
          box-shadow: 0 2px 10px rgba(0, 255, 136, 0.2);
        }
        body.theme-aurora nav a:hover {
          background: rgba(0, 255, 136, 0.3) !important;
          box-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
        }
      `;
    }
    
    document.head.appendChild(style);
  } else {
    const existing = document.getElementById('starfield-canvas');
    if (existing) existing.remove();
  }
  
  document.body.className = document.body.className.replace(/theme-\w+/g, '');
  document.body.classList.add(`theme-${themeName}`);
  
  if (themeName === 'midnight') {
    setTimeout(() => {
      createStarfield();
    }, 150);
  }
  
  const style = document.createElement('style');
  style.id = 'theme-styles';
  const existingStyle = document.getElementById('theme-styles');
  if (existingStyle) existingStyle.remove();
  
  const navBg = theme.colors.navBg || theme.colors.headerBg;
  
  style.textContent = `
    body.theme-${themeName} {
      background: ${theme.colors.background} !important;
      color: ${theme.colors.text} !important;
    }
    body.theme-${themeName} header {
      background: ${theme.colors.headerBg} !important;
    }
    body.theme-${themeName} nav {
      background: ${navBg} !important;
    }
    body.theme-${themeName} nav a {
      color: ${theme.colors.text} !important;
    }
    body.theme-${themeName} .game-card,
    body.theme-${themeName} .carousel-image-container,
    body.theme-${themeName} .movie {
      background: ${theme.colors.cardBg} !important;
    }
    body.theme-${themeName} h1,
    body.theme-${themeName} .carousel-section h2,
    body.theme-${themeName} .game-card h3,
    body.theme-${themeName} .movie h3 {
      color: ${theme.colors.primary} !important;
    }
    body.theme-${themeName} nav a:hover,
    body.theme-${themeName} .favorite-btn,
    body.theme-${themeName} button {
      background: ${theme.colors.primary} !important;
      color: ${theme.colors.primary === '#ffffff' ? '#000' : '#fff'} !important;
    }
    body.theme-${themeName} #big-clock {
      color: ${theme.colors.primary} !important;
    }
  `;
  
  document.head.appendChild(style);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', loadTheme);
} else {
  loadTheme();
}

if (typeof window !== 'undefined') {
  window.themes = themes;
  window.currentTheme = currentTheme;
  window.applyTheme = applyTheme;
  window.saveTheme = saveTheme;
  window.loadTheme = loadTheme;
}
