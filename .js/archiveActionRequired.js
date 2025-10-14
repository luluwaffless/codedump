// ==UserScript==
// @name         archiveActionRequired
// @version      2025-03-05
// @description  archives clutter
// @match        https://*.roblox.com/*
// ==/UserScript==

(() => $.ajax({
    url: "https://privatemessages.roblox.com/v1/messages?pageNumber=0&pageSize=20&messageTab=Inbox",
    method: "GET",
    success: (data) => {
        let archive = [];
        for (const message of data.collection) {
            if (message.subject === "[Important] Right to Erasure - Action Requested") archive.push(message.id);
        };
        if (archive.length > 0) {
            $.ajax({
                url: "https://privatemessages.roblox.com/v1/messages/archive",
                method: "POST",
                data: {"messageIds": archive},
                json: true,
                success: (data) => console.log(`archived ${archive.length} message${archive.length > 1 ? 's' : ''}`)
            });
        } else { console.log("nothing to archive") };
    }
}))();