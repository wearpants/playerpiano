// SPANify
var spanify = function(text, hide) {

	var arr = []
	for (var i = 0; i < text.length; i++)
	{
	    s = '<span class="hidden doctest-char">'+text[i]
	    //if (text[i] == '\n' && i != text.length-1) s+='... '
	    s += '</span>'
	    arr.push(s)
    }
    return arr.join("");
};

var hide_nodes = function() {
    $(".doctest-block").each(function(i) {
    $(this).css("min-height", this.clientHeight+"px")
    
    $(this).find("span").each(function(j) {
        if ( $(this).hasClass("doctest-source") ) {
            $(this).html(spanify($(this).text()))};
        if ( $(this).hasClass("doctest-want") ) {
            $(this).html(spanify($(this).text()))
            //$(this).addClass("hidden")
            }
        });
    });
};

var main = function() {
        var client = new STOMPClient();
        // Set up STOMP event handlers before connecting.
        client.onconnectedframe = function() {
            client.subscribe('/piano/keys');
        };
        client.onmessageframe = function(frame) {
            var vals = JSON.parse(frame.body)
            display_thru_char(vals.example_num, vals.char_num)
        };
        
        client.connect('localhost', 61613);
		
		hide_nodes();
};

var display_example = function(example_num) {
    doctest = $(".doctest-block" ).eq(example_num)
    doctest.find(".doctest-char").removeClass("hidden");
};

var display_thru_char = function(example_num, char_num) {
    doctest =$(".doctest-block" ).eq(example_num)
    hiddens = doctest.find(".doctest-char")
    console.log("hiddens "+hiddens.length+" charnum "+char_num+" example "+example_num)
    for (var i = 0; i < char_num; i++) {
        $(hiddens[i]).removeClass("hidden")
    
    };
};


// var main2 = function() {        
//     $(window).bind('keypress', function(e) {handle_keypress(e.keyCode)}; );
//  
//         
//     var waitNode = null;
// 
//  
//  var handle_keypress = function(keycode) {
//      // wait for an enter to show the want
//         if (waitNode) {
//             if (keycode == 13) {
//             waitNode.parent().next('.hidden-want').removeClass("hidden-want");
//             waitNode = null;
//             }
//             return;
//          }
//         
//      node = $(".hidden-source").eq(0)
//         node.removeClass("hidden-source");
// 
//         // are we on the last source char?
//         if (node.next(".hidden-source").length < 1) {
//             waitNode = node
//            }
//     };
// };