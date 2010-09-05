<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<link href="/css/mobile.css" media="screen" rel="stylesheet" type="text/css" />
    <link href="/css/awesome-buttons.css" media="screen" rel="stylesheet" type="text/css" />
    <meta name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1.0; user-scalable=0;"/>
    <title>${self.title()} - ${config['page_title']}</title>
</head>
<body>

<% flashes = h.flash.pop_messages() %>
% if flashes:
    % for flash in flashes:
        <div class="ui-state-highlight ui-corner-all">
            <span class="ui-icon ui-icon-info">&nbsp;</span>
            <span class="flash-text">${unicode(flash)|n}</span>
        </div>
    % endfor
% endif

${self.content()}

</body>
</html>

<%def name="html_head()">
</%def>
