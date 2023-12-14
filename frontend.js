// Below is the possibility for using api call to get the data
// fetch('https://mrundle05.github.io/bills-technical-assessment/api/data')
//     .then(response => response.json())
//     .then(data => {
//         console.log(data);
//         document.getElementById('data-display').innerHTML = `<p>${data.message}</p>`;
//     })
//     .catch(error => console.error('Error:', error));

//Instead for now, just open the csv directly then do data manipulation
d3.csv("./TEN2018SeasonData.csv").then(function(data) {
    console.log(data);
    // Convert "pff_PLAYID" and "pff_GAMEID" values to numbers for numeric sorting
    data.forEach(function(d) {
        d.pff_PLAYID = +d.pff_PLAYID;
        d.pff_GAMEID = +d.pff_GAMEID;
    });

    // Sort the data by "pff_GAMEID" and then by "pff_PLAYID" within each "pff_GAMEID" group
    data.sort(function(a, b) {
        if (a.pff_GAMEID !== b.pff_GAMEID) {
            return a.pff_GAMEID - b.pff_GAMEID;
        }
        return a.pff_PLAYID - b.pff_PLAYID;
    });

    const lastPlaysByGameId = {};
    const blitzCountsByGameId = {};
    const turnoverDifferentialByGameId = {};
    // Figure out how many blitzes per game
    data.forEach(function(d) {
        // Initialize the count for the game if it doesn't exist
        if (!blitzCountsByGameId[d.pff_GAMEID]) {
            blitzCountsByGameId[d.pff_GAMEID] = [0, 0];
        }

        // Increment the count if it's a blitz play
        if (d.pff_DEFTEAM === "TEN") {
            if(+d.pff_BLITZDOG === 1)
                blitzCountsByGameId[d.pff_GAMEID][0]++;
            blitzCountsByGameId[d.pff_GAMEID][1]++;
        }
    });
    console.log(blitzCountsByGameId);

    // Figure out turnover differential by game
    data.forEach(function(d) {
        // Initialize the count for the game if it doesn't exist
        if (!turnoverDifferentialByGameId[d.pff_GAMEID]) {
            turnoverDifferentialByGameId[d.pff_GAMEID] = 0;
        }

        // Increment the count if it's a blitz play
        if (d.pff_FUMBLE !== "" || d.pff_INTERCEPTION !== "") {
            if(d.pff_DEFTEAM === "TEN")
                turnoverDifferentialByGameId[d.pff_GAMEID]++;
            else{
                turnoverDifferentialByGameId[d.pff_GAMEID]--;
            }
        }
    });
    console.log(blitzCountsByGameId);
    console.log(turnoverDifferentialByGameId);

    // Iterate over the sorted data and update the lastPlaysByGameId object
    let week = 1;
    data.forEach(function(d) {
        lastPlaysByGameId[d.pff_GAMEID] = d;
    });
    // Use Object.values to iterate over the values of the object
    Object.values(lastPlaysByGameId).forEach(function(d) {
        d["weeknumber"] = week++;
    });


    // Create an array of objects with the last play for each pff_GAMEID
    const lastPlays = Object.values(lastPlaysByGameId);
    
    // Calculate blitz rate for each game and store it in the lastPlay object
    lastPlays.forEach(function(lastPlay) {
        const gameId = lastPlay.pff_GAMEID;
        const totalPlays = blitzCountsByGameId[gameId][1];
        const blitzCount = blitzCountsByGameId[gameId][0];
        const blitzRate = (blitzCount / totalPlays) * 100 || 0; // Convert to percentage, handle division by zero

        // Add the blitzRate property to the lastPlay object
        lastPlay.blitzRate = blitzRate.toFixed(2);
        lastPlay.turnoverDifferential = turnoverDifferentialByGameId[gameId]
    });

    // Sort by blitz rating
    lastPlays.sort(function(a, b) {
        return a.blitzRate - b.blitzRate;
    });
    // Create an ordered list to display the results
    const resultList = document.createElement('ol');
    // Iterate over lastPlays to generate list items and apply color coding
    lastPlays.forEach(function(lastPlay, index) {
        let add = 0;
        if (lastPlay.pff_DRIVEENDEVENT === "TOUCHDOWN") {
            add = 7;
        }
        if (lastPlay.pff_KICKRESULT.substring(0, 4) === "MADE") {
            add = 3;
        }
        // Create a list item
        const listItem = document.createElement('li');
        listItem.classList.add('game-list')

        // Set the text content of the list item
        if(lastPlay.pff_DEFTEAM === "TEN"){
            if(+lastPlay.pff_DEFSCORE - (+lastPlay.pff_OFFSCORE + add) > 0){
                listItem.style.color = 'green';
                listItem.innerHTML = `<p class=week_number>Week ${lastPlay.weeknumber}: Win vs. ${lastPlay.pff_OFFTEAM}</p>` +
                `<ul>` +
                `<li>Blitz Rate: ${lastPlay.blitzRate}%</li>` +
                `<li>Turnover Differential: ${lastPlay.turnoverDifferential}</li>` +
                `</ul>`;
            } else {
                listItem.style.color = 'red';
                listItem.innerHTML = `<p class=week_number>Week ${lastPlay.weeknumber}: Loss vs. ${lastPlay.pff_OFFTEAM}</p>` +
                                     `<ul>` +
                                     `<li>Blitz Rate: ${lastPlay.blitzRate}%</li>` +
                                     `<li>Turnover Differential: ${lastPlay.turnoverDifferential}</li>` +
                                     `</ul>`;
            }
        } 
        else {
            if ((+lastPlay.pff_OFFSCORE + add) - +lastPlay.pff_DEFSCORE > 0) {
                listItem.style.color = 'green';
                listItem.innerHTML = `<p class=week_number>Week ${lastPlay.weeknumber}: Win vs. ${lastPlay.pff_DEFTEAM}</p>` +
                                     `<ul>` +
                                     `<li>Blitz Rate: ${lastPlay.blitzRate}%</li>` +
                                     `<li>Turnover Differential: ${lastPlay.turnoverDifferential}</li>` +
                                     `</ul>`;
            } 
            else {
                listItem.style.color = 'red';
                listItem.innerHTML = `<p class=week_number>Week ${lastPlay.weeknumber}: Loss vs. ${lastPlay.pff_DEFTEAM}</p>` +
                                     `<ul>` +
                                     `<li>Blitz Rate: ${lastPlay.blitzRate}%</li>` +
                                     `<li>Turnover Differential: ${lastPlay.turnoverDifferential}</li>` +
                                     `</ul>`;
            }
        }

        // Append the list item to the ordered list
        resultList.appendChild(listItem);
    });
    console.log(lastPlays);

    // Display the ordered list in the HTML element with ID "display1"
    document.getElementById('data-display').appendChild(resultList);
});

// Function to display the selected image
function showImage(imagePath) {
    // Get the image container
    const imageContainer = document.getElementById('image-container');

    // Create an image element
    const imgElement = document.createElement('img');
    imgElement.src = imagePath;
    imgElement.alt = 'Selected Image';

    // Clear the container and append the new image
    imageContainer.innerHTML = '';
    imageContainer.appendChild(imgElement);
}