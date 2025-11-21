let clockSettings = {
  format24: true,
  showDate: true,
  timezoneOffset: 0,
  customTime: null
};

function loadClockSettings() {
  try {
    const saved = localStorage.getItem('clockSettings');
    if (saved) {
      clockSettings = { ...clockSettings, ...JSON.parse(saved) };
    }
  } catch (e) {
    console.error('Failed to load clock settings:', e);
  }
}

function saveClockSettings() {
  try {
    localStorage.setItem('clockSettings', JSON.stringify(clockSettings));
  } catch (e) {
    console.error('Failed to save clock settings:', e);
  }
}

function formatTime(date) {
  let hours = date.getHours();
  const minutes = date.getMinutes().toString().padStart(2, '0');
  const seconds = date.getSeconds().toString().padStart(2, '0');
  
  if (!clockSettings.format24) {
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12;
    return `${hours.toString().padStart(2, '0')}:${minutes}:${seconds} ${ampm}`;
  }
  
  return `${hours.toString().padStart(2, '0')}:${minutes}:${seconds}`;
}

function formatDate(date) {
  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  
  const dayName = days[date.getDay()];
  const month = months[date.getMonth()];
  const day = date.getDate();
  const year = date.getFullYear();
  
  return `${dayName}, ${month} ${day}, ${year}`;
}

function getCurrentTime() {
  if (clockSettings.customTime) {
    const custom = new Date(clockSettings.customTime);
    const now = new Date();
    const baseTime = new Date(clockSettings.customTime);
    const diff = now.getTime() - baseTime.getTime();
    return new Date(custom.getTime() + diff);
  }
  
  const now = new Date();
  if (clockSettings.timezoneOffset !== 0) {
    return new Date(now.getTime() + (clockSettings.timezoneOffset * 60 * 1000));
  }
  
  return now;
}

function updateClock() {
  const clockElement = document.getElementById('big-clock');
  const dateElement = document.getElementById('clock-date');
  
  if (!clockElement) return;
  
  const currentTime = getCurrentTime();
  clockElement.textContent = formatTime(currentTime);
  
  if (dateElement && clockSettings.showDate) {
    dateElement.textContent = formatDate(currentTime);
  } else if (dateElement) {
    dateElement.textContent = '';
  }
}

function createClock() {
  const clockContainer = document.createElement('div');
  clockContainer.id = 'clock-container';
  clockContainer.innerHTML = `
    <div id="big-clock">00:00:00</div>
    <div id="clock-date"></div>
  `;
  
  const logoContainer = document.querySelector('header > .logo-container');
  if (logoContainer) {
    logoContainer.appendChild(clockContainer);
  } else {
    const header = document.querySelector('header');
    if (header) {
      const newLogoContainer = document.createElement('div');
      newLogoContainer.className = 'logo-container';
      const existingContent = header.innerHTML;
      header.innerHTML = '';
      header.appendChild(document.createElement('div')).innerHTML = existingContent;
      header.querySelector('.logo-container').appendChild(clockContainer);
    } else {
      document.body.insertBefore(clockContainer, document.body.firstChild);
    }
  }
  
  loadClockSettings();
  updateClock();
  setInterval(updateClock, 1000);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', createClock);
} else {
  createClock();
}

if (typeof window !== 'undefined') {
  window.clockSettings = clockSettings;
  window.loadClockSettings = loadClockSettings;
  window.saveClockSettings = saveClockSettings;
  window.updateClock = updateClock;
}

