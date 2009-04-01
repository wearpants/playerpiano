#!/usr/bin/env python
# encoding: utf-8


try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

import doctest
from docutils.core import publish_cmdline, default_description
from docutils import nodes

class doctest_source(nodes.Inline, nodes.TextElement): pass
class doctest_want(nodes.Inline, nodes.TextElement): pass

nodes.doctest_source = doctest_source
nodes.doctest_want = doctest_want

nodes.node_class_names.append("doctest_source")
nodes.node_class_names.append("doctest_want")

def better_doctest_block(data):
   ret = nodes.doctest_block()
   # Step 1: Parse the doctest
   test = doctest.DocTestParser().get_doctest(data, {}, "name", "filename", 0)
   # Step 2: Loop over the sources (inputs) and wants (outputs)
   for example in test.examples:
       source = nodes.doctest_source(example.source, example.source)
       want = nodes.doctest_want(example.want, example.want)
       ret.children.append(source)
       ret.children.append(want)
   return ret
 
nodes.better_doctest_block = better_doctest_block

def __doctest(self, match, context, next_state):
    data = '\n'.join(self.state_machine.get_text_block())
    self.parent += nodes.better_doctest_block(data)
    return [], next_state, []

from docutils.parsers.rst import states
states.Body.doctest = __doctest

from docutils.writers import html4css1

raw_js = r"""
<script type="text/javascript" src="jquery-1.3.2.js"></script>
<script type="text/javascript" charset="utf-8">
	$(document).ready(function() {		
		var spanify = function(text) {

			var arr = ['<span class="hidden-source">&gt;&gt;&gt; </span>']
			for (var i = 0; i < text.length; i++) {
			    s = '<span class="hidden-source">'+text[i]
			    if (text[i] == '\n' && i != text.length-1) s+='... '
			    s += '</span>'
    		    arr.push(s)
		    }
	    return arr.join("");
    };
		
		
		$(".doctest-block").each(function(i) {
		    $(this).css("min-height", this.clientHeight+"px")
		    
                $(this).find("span").each(function(j) {
                        if ( $(this).hasClass("doctest-source") ) {
                            $(this).html(spanify($(this).text()))};
                        if ( $(this).hasClass("doctest-want") ) {
                            $(this).addClass("hidden-want")}
                    });
                });
        
        
        var waitNode = null;
        
		$(window).bind('keypress', function(e) {
		    // wait for an enter to show the want
            if (waitNode) {
                if (e.keyCode == 13) {
                waitNode.parent().next('.hidden-want').removeClass("hidden-want");
                waitNode = null;
                }
                return;
             }
            
		    node = $(".hidden-source").eq(0)
	        node.removeClass("hidden-source");

            // are we on the last source char?
	        if (node.next(".hidden-source").length < 1) {
	            waitNode = node
	           }

	    });
	});
</script>
"""

class MyTranslator(html4css1.HTMLTranslator):

    def __init__(self, *args, **kwargs):
        html4css1.HTMLTranslator.__init__(self, *args, **kwargs)
        self.head.append(raw_js)

    def visit_doctest_block(self, node):
        self.body.append(self.starttag(node, 'pre', CLASS='doctest-block'))

    def depart_doctest_block(self, node):
        self.body.append('</pre>\n')

    def visit_doctest_source(self, node):
        self.body.append(self.starttag(node, 'span', CLASS='doctest-source', suffix=''))

    def depart_doctest_source(self, node):
        self.body.append('</span>')

    def visit_doctest_want(self, node):
        self.body.append(self.starttag(node, 'span', CLASS='doctest-want', suffix=''))

    def depart_doctest_want(self, node):
        self.body.append('</span>')

writer = html4css1.Writer()
writer.translator_class = MyTranslator

description = ('Generates (X)HTML documents from standalone reStructuredText '
              'sources.  ' + default_description)

publish_cmdline(writer=writer, description=description)
