/**
 * Browser compatibility utilities for handling differences across
 * Chrome, Safari, Firefox, and Edge (especially mobile variants).
 */

export const BrowserCompat = {
  /**
   * Check if running on iOS (Safari or Chrome on iOS)
   */
  isIOS(): boolean {
    return /iPad|iPhone|iPod/.test(navigator.userAgent);
  },

  /**
   * Check if running on Safari (including mobile Safari)
   */
  isSafari(): boolean {
    return /Safari/.test(navigator.userAgent) && !/Chrome/.test(navigator.userAgent);
  },

  /**
   * Check if in private browsing mode (Safari private, Incognito, etc.)
   */
  isPrivateMode(): Promise<boolean> {
    return new Promise((resolve) => {
      try {
        const test = '__priv_test__';
        const storage = localStorage;
        storage.setItem(test, test);
        storage.removeItem(test);
        resolve(false); // Not in private mode
      } catch {
        resolve(true); // Likely in private mode
      }
    });
  },

  /**
   * Safely handle geolocation with timeout fallback
   */
  getGeolocation(timeout = 5000): Promise<GeolocationCoordinates> {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error('Geolocation not supported'));
        return;
      }

      const watchId = navigator.geolocation.getCurrentPosition(
        (pos) => resolve(pos.coords),
        (err) => reject(err),
        { timeout, enableHighAccuracy: false }
      );

      // Additional timeout as fallback
      setTimeout(() => {
        reject(new Error('Geolocation timeout'));
      }, timeout + 1000);
    });
  },

  /**
   * Safely handle clipboard API (Safari < 15.4 doesn't support it)
   */
  async copyToClipboard(text: string): Promise<boolean> {
    try {
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(text);
        return true;
      }
      // Fallback for older browsers
      const textarea = document.createElement('textarea');
      textarea.value = text;
      textarea.style.position = 'fixed';
      textarea.style.opacity = '0';
      document.body.appendChild(textarea);
      textarea.select();
      const success = document.execCommand('copy');
      document.body.removeChild(textarea);
      return success;
    } catch {
      return false;
    }
  },

  /**
   * Check if localStorage is available and writable
   */
  isStorageAvailable(type: 'localStorage' | 'sessionStorage' = 'localStorage'): boolean {
    try {
      const storage = type === 'localStorage' ? localStorage : sessionStorage;
      const test = '__storage_test__';
      storage.setItem(test, test);
      storage.removeItem(test);
      return true;
    } catch {
      return false;
    }
  },

  /**
   * Get user agent info for debugging
   */
  getUserAgentInfo() {
    const ua = navigator.userAgent;
    return {
      isChrome: /Chrome/.test(ua),
      isSafari: /Safari/.test(ua) && !/Chrome/.test(ua),
      isFirefox: /Firefox/.test(ua),
      isEdge: /Edg/.test(ua),
      isIOS: /iPad|iPhone|iPod/.test(ua),
      isAndroid: /Android/.test(ua),
      isMobile: /Mobi|Android|iPhone/.test(ua),
      isPrivateMode: false, // Determined async via isPrivateMode()
    };
  },

  /**
   * Handle fetch with timeout and retry logic for Safari compatibility
   */
  async fetchWithRetry(
    url: string,
    options: RequestInit = {},
    retries = 3,
    timeout = 10000
  ): Promise<Response> {
    for (let i = 0; i < retries; i++) {
      try {
        const controller = new AbortController();
        const id = setTimeout(() => controller.abort(), timeout);

        const response = await fetch(url, {
          ...options,
          signal: controller.signal,
        });

        clearTimeout(id);
        return response;
      } catch (err) {
        if (i === retries - 1) throw err;
        // Exponential backoff
        await new Promise((r) => setTimeout(r, Math.pow(2, i) * 500));
      }
    }
    throw new Error('All retries failed');
  },
};
