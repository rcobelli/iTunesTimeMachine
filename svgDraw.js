function drawPath(svg, path, startX, startY, endX, endY) {
    // get the path's stroke width (if one wanted to be  really precize, one could use half the stroke size)
    var stroke =  parseFloat(path.attr("stroke-width"));

    // 1. move a bit down, 2. arch,  3. move a bit to the right, 4.arch, 5. move down to the end
    path.attr("d",  "M"  + startX + " " + startY +
    " h " + 10 +
    " a 10 10 0 0 1 10 10" +
    " v " + (endY - startY) +
    " a 10 10 0 0 0 10 10" +
    " h " + 10 );
}

function connectElements(path, startElem, endElem) {
    // var svgContainer= $("#svgContainer");

    // if first element is lower than the second, swap!
    if (startElem.offset().top > endElem.offset().top){
        var temp = startElem;
        startElem = endElem;
        endElem = temp;
    }

    // get (top, left) coordinates for the two elements
    var startCoord = startElem.offset();
    var endCoord   = endElem.offset();

    // calculate path's start (x,y)  coords
    // we want the x coordinate to visually result in the element's mid point
    var startX = startCoord.left + startElem.outerWidth() - 40    // x = left offset + 0.5*width - svg's left offset
    var startY = startCoord.top  + 0.5*startElem.outerHeight()        // y = top offset + height - svg's top offset

    // calculate path's end (x,y) coords
    var endX = endCoord.left
    var endY = endCoord.top

    // call function for drawing the path
    drawPath($("#svg1"), path, startX, startY, endX, endY);
}

function connectAll(text) {
    var paths = document.getElementsByTagName("path")
    for (i = 0; i < paths.length; i++) {
        drawPath($("#svg1"), $("#path" + i), 0, 0, 0, 0);
    }

    var aTags = document.getElementsByTagName("td");
    var found = [];

    for (var i = 0; i < aTags.length; i++) {
        if (aTags[i].textContent == text) {
            found.push(aTags[i].id)
        }
    }

    for (i = 1; i < found.length; i++) {
        connectElements($("#path" + i), $("#" + found[i-1]), $("#" + found[i]));
    }

    // TODO: Color the cells with a pipe
}

$(document).ready(function() {
    // reset svg each time
    $("#svgContainer").attr("height", document.body.scrollHeight);
    $("#svgContainer").attr("width", document.body.scrollWidth);
    $("#svg1").attr("height", document.body.scrollHeight);
    $("#svg1").attr("width", document.body.scrollWidth);

    document.querySelectorAll('.table td')
    .forEach(e => e.addEventListener("click", function() {
        connectAll(this.innerText)
    }));
});
