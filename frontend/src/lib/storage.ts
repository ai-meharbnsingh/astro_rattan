/**
 * Cross-browser safe localStorage/sessionStorage wrapper.
 * Handles Safari's private mode, quota exceeded, and other edge cases.
 */

type StorageType = 'local' | 'session';

class SafeStorage {
  private static hasLocalStorage(): boolean {
    try {
      const test = '__test__';
      localStorage.setItem(test, test);
      localStorage.removeItem(test);
      return true;
    } catch {
      return false;
    }
  }

  private static hasSessionStorage(): boolean {
    try {
      const test = '__test__';
      sessionStorage.setItem(test, test);
      sessionStorage.removeItem(test);
      return true;
    } catch {
      return false;
    }
  }

  static setItem(type: StorageType, key: string, value: string): boolean {
    try {
      const storage = type === 'local' ? localStorage : sessionStorage;

      // Check if storage is available
      if (type === 'local' && !this.hasLocalStorage()) return false;
      if (type === 'session' && !this.hasSessionStorage()) return false;

      storage.setItem(key, value);
      return true;
    } catch (e) {
      if (e instanceof DOMException && e.name === 'QuotaExceededError') {
        console.warn(`Storage quota exceeded for ${type}Storage`);
      }
      return false;
    }
  }

  static getItem(type: StorageType, key: string): string | null {
    try {
      const storage = type === 'local' ? localStorage : sessionStorage;

      if (type === 'local' && !this.hasLocalStorage()) return null;
      if (type === 'session' && !this.hasSessionStorage()) return null;

      return storage.getItem(key);
    } catch {
      return null;
    }
  }

  static removeItem(type: StorageType, key: string): boolean {
    try {
      const storage = type === 'local' ? localStorage : sessionStorage;

      if (type === 'local' && !this.hasLocalStorage()) return false;
      if (type === 'session' && !this.hasSessionStorage()) return false;

      storage.removeItem(key);
      return true;
    } catch {
      return false;
    }
  }

  static clear(type: StorageType): boolean {
    try {
      const storage = type === 'local' ? localStorage : sessionStorage;

      if (type === 'local' && !this.hasLocalStorage()) return false;
      if (type === 'session' && !this.hasSessionStorage()) return false;

      storage.clear();
      return true;
    } catch {
      return false;
    }
  }
}

export default SafeStorage;
