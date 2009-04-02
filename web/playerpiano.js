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



var display_example = function(example_num) {
    doctest = $(".doctest-block" ).eq(example_num)
    doctest.find(".doctest-char").removeClass("hidden");
};

var display_thru_char = function(char_num) {
    chars = $(".doctest-char")
    chars.slice(0, char_num).removeClass("hidden")
    next_block = $(chars[char_num-1]).parent().parent().prev('p')
    $.scrollTo(next_block, offset="-200px", duration=1.5)
    

};


var main = function() {
        var client = new STOMPClient();
        // Set up STOMP event handlers before connecting.
        client.onconnectedframe = function() {
            client.subscribe('/piano/keys');
        };
        client.onmessageframe = function(frame) {
            var vals = JSON.parse(frame.body)
            display_thru_char(vals.char_num)
        };
        
        client.connect('localhost', 61613);
		
		hide_nodes();
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