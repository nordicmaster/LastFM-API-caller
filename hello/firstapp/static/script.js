    async function getInfo(artist) {
        if (artist.includes(' '))
            artist = artist.replaceAll(' ', '+');
        const responseInfo = await fetch("https://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist="+artist+"&api_key=57ee3318536b23ee81d6b27e36997cde&format=json");
        var xresInfo = await responseInfo.json();
        listeners = xresInfo.artist.stats.listeners;
        totalscrobbles = xresInfo.artist.stats.playcount;
        document.getElementById("artists").innerHTML += "<span class=\"fixwidth\">"+
                                            artist + "</span> has <span class=\"fixwidth2\">" +
											listeners + "</span> listeners and <span class=\"fixwidth3\">" +
											totalscrobbles + "</span> scrobbles. Ratio=" +
											totalscrobbles/listeners + "<br>";
    }

    function clearBase() {
        //request to host

    }