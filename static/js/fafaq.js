   // SHOW/HIDE/TOGGLE script
    // ============
    // =TODO: Make links to local anchors (other FAQ questions) open the answer div on the same page - http://stackoverflow.com/questions/4648446/jquery-load-retrieve-page-div-by-id-in-anchor-link
            
    $(document).ready(function(){
        $("div.answer").hide();
        $("h3").click(function(){
            $(this).next().toggle("fast");
            // trying to get the H3 to turn black when clicking: http://api.jquery.com/toggleClass/
            $(this).toggleClass("darkheadings");
            // stopping local anchor from being followed so the page doesn't jump
            // return false;
        });

        // http://stackoverflow.com/questions/2848627/use-anchor-to-display-div
        $(function() {
            if(location.hash != "") {
                // $(location.hash + ":hidden").toggle('fast').prev("h3").toggleClass('darkheadings');
                $(location.hash).next("div").toggle("fast").prev("h3").toggleClass("darkheadings");
            }
        });

        // http://andylangton.co.uk/jquery-show-hidecomment by morvi on 10.01.2010 at 23:46
        $("a.hideall").click(function() {
            $("div.answer").hide("fast");
            $("h3").removeClass("darkheadings");
        });
        $("a.showall").click(function() {
            $("div.answer").show("fast");
            $("h3").addClass("darkheadings");
        });

    });



    // ANCHOR HIGHLIGHTER script - can't find author info for this script
    // ============

    // Highlighting FAQ's using anchors and the ever popular yellow-fade technique.
    // Including this script in a page will automatically do two things when the page loads:
    // 1. Highlight a target item from the URL (browser address bar) if one is present.
    // 2. Setup all anchor tags with targets pointing to the current page to cause a fade on the target element when clicked.

    // This is the amount of time (in milliseconds) that will lapse between each step in the fade
    var FadeInterval = 75;

    // This is where the fade will start, if you want it to be faster and start with a lighter color, make this number smaller
    // It corresponds directly to the FadeSteps below
    var StartFadeAt = 25;

    // This is list of steps that will be used for the color to fade out
    var FadeSteps = new Array();
    FadeSteps[1] = "ff";
    FadeSteps[2] = "ee";
    FadeSteps[3] = "dd";
    FadeSteps[4] = "cc";
    FadeSteps[5] = "bb";
    FadeSteps[6] = "aa";
    FadeSteps[7] = "99";
    // FadeSteps[8] = "99";
    // FadeSteps[9] = "aa";
    // FadeSteps[10] = "bb";
    // FadeSteps[11] = "cc";
    // FadeSteps[12] = "dd";
    // FadeSteps[13] = "ee";
    // FadeSteps[14] = "ee";
    // FadeSteps[15] = "ee";
    // FadeSteps[16] = "ee";
    // FadeSteps[17] = "dd";
    // FadeSteps[18] = "cc";
    // FadeSteps[19] = "bb";
    // FadeSteps[20] = "aa";
    FadeSteps[21] = "99";
    FadeSteps[22] = "99";
    FadeSteps[23] = "aa";
    FadeSteps[24] = "bb";
    FadeSteps[25] = "cc";
    FadeSteps[26] = "dd";
    FadeSteps[27] = "ee";
    FadeSteps[28] = "ff";

    // These are the lines that "connect" the script to the page.
    var W3CDOM = (document.createElement && document.getElementsByTagName);
    addEvent(window, 'load', initFades);

    // This function automatically connects the script to the page so that you do not need any inline script
    // See http://www.scottandrew.com/weblog/articles/cbs-events for more information
    function addEvent(obj, eventType,fn, useCapture)
    {
        if (obj.addEventListener) {
            obj.addEventListener(eventType, fn, useCapture);
            return true;
        } else {
            if (obj.attachEvent) {
                var r = obj.attachEvent("on"+eventType, fn);
                return r;
            }
        }
    }

    // The function that initializes the fade and hooks the script into the page
    function initFades()
    {
        if (!W3CDOM) return;

        // This section highlights targets from the URL (browser address bar)
        // Get the URL
        var currentURL = unescape(window.location);
        // If there is a '#' in the URL
        if (currentURL.indexOf('#')>-1) 
        // Highlight the target
        DoFade(StartFadeAt, currentURL.substring(currentURL.indexOf('#')+1,currentURL.length));

        // This section searches the page body for anchors and adds onclick events so that their targets get highlighted
        // Get the list of all anchors in the body
        var anchors = document.body.getElementsByTagName('a');
        // For each of those anchors
        for (var i=0;i<anchors.length;i++)
        // If there is a '#' in the anchors href
        if (anchors[i].href.indexOf('#')>-1)
        // Add an onclick event that calls the highlight function for the target
        anchors[i].onclick = function(){Highlight(this.href);return true};
    }

    // This function is just a small wrapper to use for the oncick events of the anchors
    function Highlight(target) {
        // Get the target ID from the string that was passed to the function
        var targetId = target.substring(target.indexOf('#')+1,target.length);
        DoFade(StartFadeAt, targetId);
    }

    // This is the recursive function call that actually performs the fade
    function DoFade(colorId, targetId) {
        if (colorId >= 1) {
            var target = document.getElementById(targetId);
            if (target) {
                target.style.backgroundColor = "#ffff" + FadeSteps[colorId];
                // If it's the last color, set it to transparent
                if (colorId==1) {
                    document.getElementById(targetId).style.backgroundColor = "transparent";
                }
                colorId--;
                // Wait a little bit and fade another shade
                setTimeout("DoFade("+colorId+",'"+targetId+"')", FadeInterval);
            }
        }
    }