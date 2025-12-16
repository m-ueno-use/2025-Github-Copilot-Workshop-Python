(function () {
  'use strict';

  // mm:ss に変換
  function formatAsMMSS(totalSeconds) {
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
  }

  class Timer {
    constructor(durationSeconds, onTick, onComplete) {
      this.initial = Number.isFinite(durationSeconds) ? Math.max(0, durationSeconds) : 25 * 60;
      this.remaining = this.initial;
      this.onTick = typeof onTick === 'function' ? onTick : () => {};
      this.onComplete = typeof onComplete === 'function' ? onComplete : () => {};
      this._interval = null;
      this._running = false;
    }

    start() {
      if (this._running) return;
      if (this.remaining <= 0) this.remaining = this.initial;

      this._running = true;
      const startBtn = document.getElementById('start-btn');
      if (startBtn) startBtn.disabled = true;

      this._interval = setInterval(() => {
        this.remaining -= 1;
        this.onTick(this.remaining);

        if (this.remaining <= 0) {
          this.stop(true);
        }
      }, 1000);
    }

    stop(triggerComplete = false) {
      if (this._interval) {
        clearInterval(this._interval);
        this._interval = null;
      }
      this._running = false;
      const startBtn = document.getElementById('start-btn');
      if (startBtn) startBtn.disabled = false;

      if (triggerComplete) {
        this.remaining = 0;
        this.onTick(this.remaining);
        this.onComplete();
      }
    }

    reset() {
      this.stop(false);
      this.remaining = this.initial;
      this.onTick(this.remaining);
      const status = document.getElementById('status-label');
      if (status) status.textContent = '作業中';
    }
  }

  // グローバル公開（index.htmlから使用）
  window.Timer = Timer;
  window.formatAsMMSS = formatAsMMSS;
})();
