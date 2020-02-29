import os
import shutil

output_dir = str(os.getcwd()) + "/webpages"
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

def generateHTML(yearToCalculate, week, teamRankOrderSorted):
    fileToOpen = output_dir + "/rankings_" + str(yearToCalculate) + "_week_" + str(week) + "_webpage.html"
    with open(fileToOpen, "w") as htmlFile:
        htmlStart = """<!DOCTYPE html>
<html>
<head>
<style>
table {
    border-spacing: 0;
    width: 100%;
    border: 1px solid #ddd;
}

th {
    text-align: left;
    padding: 5px;
    border: 1px solid black;
    font-size: 20px;
}

td {
    text-align: left;
    padding: 5px;
    border: 1px solid black;
}

tr:nth-child(even) {
    background-color: #b9b8b8
}
</style>

<body>\n
"""
        htmlTitle = "<h1>Rankings: Week {} of {}</h1>\n".format(week, yearToCalculate)
        htmlContinued = """<h3>Click on the headers to sort!</h3>
<table id="rankingsTable">
    <thead>
        <tr>
            <th onclick="sortTable(0)" title="Overall rank">RANK</th>
            <th onclick="sortTable(1)" title="Team">TEAM</th>
            <th onclick="sortTable(2)" title="Conference the team plays in">CONFERENCE</th>
            <th onclick="sortTable(3)" title="Score by the system">POINTS</th>
        </tr>
    </thead>
    <tbody>
    """
        htmlFile.write(htmlStart)
        htmlFile.write(htmlTitle)
        htmlFile.write(htmlContinued)

        count = 1

        for team in teamRankOrderSorted:
            htmlFile.write("<tr>")
            htmlFile.write("<td>" + str(count) + "</td>")
            htmlFile.write("<td>" + team[1][0] + "</td>")
            htmlFile.write("<td>" + team[1][1] + "</td>")
            htmlFile.write("<td align=\"right\">" + str(team[1][2]) + "</td>")
            htmlFile.write("</tr>\n")
            count = count + 1

        htmlEnd = """
        </tbody>
</table>

<script>
    function sortTable(n) {
        var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
        table = document.getElementById("rankingsTable");
        switching = true;
        // Set the sorting direction to ascending:
        dir = "asc";
        /* Make a loop that will continue until
        no switching has been done: */
        while (switching) {
            // Start by saying: no switching is done:
            switching = false;
            rows = table.rows;
            /* Loop through all table rows (except the
            first, which contains table headers): */
            for (i = 1; i < (rows.length - 1); i++) {
                // Start by saying there should be no switching:
                shouldSwitch = false;
                /* Get the two elements you want to compare,
                one from current row and one from the next: */
                x = rows[i].getElementsByTagName("TD")[n];
                y = rows[i + 1].getElementsByTagName("TD")[n];
                /* Check if the two rows should switch place,
                based on the direction, asc or desc: */
                if (dir == "asc") {
                    if ((n != 3 && n != 0) && x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                        // If so, mark as a switch and break the loop:
                        shouldSwitch = true;
                        break;
                    } else if ((n == 3 || n == 0) && Number(x.innerHTML.valueOf()) > Number(y.innerHTML.valueOf())) {
                        // If so, mark as a switch and break the loop:
                        shouldSwitch = true;
                        break;
                    }
                } else if (dir == "desc") {
                    if ((n != 3 && n != 0) && x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                        // If so, mark as a switch and break the loop:
                        shouldSwitch = true;
                        break;
                    } else if ((n == 3 || n == 0) && Number(x.innerHTML.valueOf()) < Number(y.innerHTML.valueOf())) {
                        // If so, mark as a switch and break the loop:
                        shouldSwitch = true;
                        break;
                    }
                }
            }
            if (shouldSwitch) {
                /* If a switch has been marked, make the switch
                and mark that a switch has been done: */
                rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                switching = true;
                // Each time a switch is done, increase this count by 1:
                switchcount ++;
            } else {
                /* If no switching has been done AND the direction is "asc",
                set the direction to "desc" and run the while loop again. */
                if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
                }
            }
        }
    }
</script>
</body>
</head>
</html>
<!-- Special thanks to http://www.convertcsv.com/csv-to-html.htm for generating the table -->
<!-- And thanks to https://www.w3schools.com/howto/howto_js_sort_table.asp for the sorting -->
"""
        htmlFile.write(htmlEnd)

    shutil.copy(fileToOpen, "current-rankings.html")