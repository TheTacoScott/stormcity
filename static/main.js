// http://stackoverflow.com/questions/4810841/how-can-i-pretty-print-json-using-javascript
function syntaxHighlight(json) {
    if (typeof json != 'string') {
         json = JSON.stringify(json, undefined, 2);
    }
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        var cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'key';
            } else {
                cls = 'string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'boolean';
        } else if (/null/.test(match)) {
            cls = 'null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}



function StartWatching(url)
{
 console.log(url);
 var $postdata = JSON.stringify({"action":"results","param": url});
 $.post('/api', $postdata, function(response) {
   if (response["status"] == 0)
   {
     ShowResults(response["data"]) 
   }
   else
   {
    setTimeout(function() { StartWatching(url); }, 200);
   }
 }, 'json');
}

function ShowResults(data)
{
  $("#working").fadeOut(function() {
    $("#result").fadeOut(0,function() { 
      $(this).removeClass("hide").fadeIn(function() {
        $("#resultsjson").html("<pre>" + syntaxHighlight(data) + "</pre>");
      });
    });
  });
}

function SubmitFetch()
{
  $("#fetch").fadeOut(function() {
    $("#working").fadeOut(0,function() { 
      $(this).removeClass("hide").fadeIn(function() {
        var $fetch_url = $("#fetchurl").val();
        var $postdata = JSON.stringify({"action":"fetch","param": $fetch_url});
        $.post('/api', $postdata, function(response) {
          if (response["status"] == 0)
          {
            StartWatching($fetch_url);
          }
        }, 'json');
      });
    });
  });
}

$( document ).ready(function() {
  $("#fetchurl_button").click(SubmitFetch);
  $("#returnhome").click(function() { window.location="/"; });
});
