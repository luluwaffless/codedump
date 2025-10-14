// ==UserScript==
// @name         removeRecommended
// @version      1.0.0
// @description  fuck this shit im out
// @match        https://www.roblox.com/home
// ==/UserScript==

(() => {
    const m = () => {
        const divs = document.querySelectorAll('div[data-testid="home-page-game-grid"]');
        if (divs.length > 0) {
            divs.forEach(div => {
                div.remove();
            });
        } else {
            setTimeout(m, 1000);
        };
    };
    m();
})();