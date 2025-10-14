// ==UserScript==
// @name         friendRequests
// @version      2025-09-08
// @description  prints the array of users who sent a friend request to you
// @match        https://www.roblox.com/users/friends*
// ==/UserScript==

(() => $.ajax({
    url: 'https://friends.roblox.com/v1/my/friends/requests?limit=100&sortOrder=Desc',
    success: (requests) => {
        let ids = [];
        for (const user of requests.data) ids.push(user.id);
        $.ajax({
            url: 'https://users.roblox.com/v1/users',
            method: 'POST',
            data: {"userIds": ids, "excludeBannedUsers": false},
            json: true,
            success: (users) => {
                const verifiedPpl = users.data.filter(user => user.hasVerifiedBadge);
                if (verifiedPpl.length > 0) {
                    alert("verified ppl have sent requests");
                    console.log("verified ppl:", verifiedPpl);
                } else console.log("no verified ppl");
            }
        });
    }
}))();