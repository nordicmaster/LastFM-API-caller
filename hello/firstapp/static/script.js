    async function getInfo(artist) {
        console.log(artist);
        if (artist.includes(' '))
            artist = artist.replaceAll(' ', '+');
        const responseInfo = await fetch("https://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist="+artist+"&api_key=57ee3318536b23ee81d6b27e36997cde&format=json");
        var xresInfo = await responseInfo.json();
        //console.log(xresInfo);
        listeners = xresInfo.artist.stats.listeners;
        totalscrobbles = xresInfo.artist.stats.playcount;
        document.getElementById("artists").innerHTML += artist + " has " +
											listeners + " listeners and  " +
											totalscrobbles + " scrobbles<br>";
        console.log(listeners);
        console.log("0-0-0-0");
        console.log(totalscrobbles);
    }
