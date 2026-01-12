// static/config.js
const isGitHubPages = window.location.hostname.includes('github.io');
const BASE_PATH = isGitHubPages ? '/VoyageAI-Explorer' : '';

// Export configuration
window.AppConfig = {
  basePath: BASE_PATH,
  isProduction: isGitHubPages,
  getAssetPath: (path) => {
    // Remove leading slash if present
    const cleanPath = path.startsWith('/') ? path.slice(1) : path;
    return `${BASE_PATH}/${cleanPath}`.replace(/\/+/g, '/');
  }
};

console.log('App Config:', window.AppConfig);
