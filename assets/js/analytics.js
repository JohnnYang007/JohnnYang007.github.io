(function () {
  'use strict';

  // One endpoint for both Jekyll pages and standalone simulation pages.
  var endpoint = 'https://johnnyang-007.goatcounter.com/count';
  if (!endpoint || window.location.hostname !== 'johnnyang007.github.io' || window.self !== window.top) {
    return;
  }
  try {
    if (window.location.hash !== '#toggle-goatcounter' && window.localStorage.getItem('skipgc') === 't') {
      return;
    }
  } catch (_error) {
    // A browser may block storage; page content must still load normally.
  }

  var script = document.createElement('script');
  script.async = true;
  script.src = 'https://gc.zgo.at/count.js';
  script.dataset.goatcounter = endpoint;
  script.dataset.goatcounterSettings = '{"no_events":true}';
  document.head.appendChild(script);
})();
