<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

    <title>${self.title()} - Medienverwaltung</title>

	<link href="/css/default.css" media="screen" rel="stylesheet" type="text/css" />
    <link href="/css/ui-lightness/jquery-ui-1.7.2.custom.css" media="screen" rel="stylesheet" type="text/css" />
    <link href="/css/minimalistic/style.css" rel="stylesheet" type="text/css" media="screen" />
##    <link href="/css/minimalistic/bigright.css" rel="stylesheet" type="text/css" media="screen" />
    <script src="http://code.jquery.com/jquery-1.4.2.min.js" type="text/javascript"></script>
##    <script src="/js/jquery-1.3.2.min.js" type="text/javascript"></script>
##    % for x in c.rss_feeds:
##    <link rel="alternate" type="application/rss+xml" title="${x['title']}" href="${x['link']}" />
##    % endfor
</head>
<body>
<div id="header">
<div id="layoutImg"></div>
<div id="titel">
##    <a class ="titel" href="${h.url_for(controller='medium', action='list_gallery', id=None, page=None, type='books', tag=None)}">
    <a class ="titel" href="${h.url_for('/')}">
        Medienverwaltung
    </a>
</div>
 <div id="menu">
  <ul id="nav">
    <li><a href="${h.url_for(controller='medium', action='list_gallery', id=None, page=None, type='books', tag=None)}">Books</a></li>
    <li><a href="${h.url_for(controller='medium', action='list_gallery', id=None, page=None, type='dvds', tag=None)}">DVDs</a></li>
    <li><a href="${h.url_for(controller='person', action='list', id=None, page=None, type=None, tag=None)}">Persons</a></li>
  </ul>
 </div>
</div>

<% flashes = h.flash.pop_messages() %>
% if flashes:
    % for flash in flashes:
        <div class="ui-state-highlight ui-corner-all">
            <span class="ui-icon ui-icon-info">&nbsp;</span>
            <span class="flash-text">${flash}</span>
        </div>
    % endfor
% endif
        


##<div class="main">
##</div>

<div id="content">

<div id="right">
    <h1>${self.title()}</h1>
    ${self.content()}
</div>
<div id="left">
    ${self.side()}
    % if c.tags:
	<div class="box">
        <h2>Tags:</h2>
        <span class="tags">
        % for item in c.tags:
        <a href="${h.url_for(tag=item, page=None)}">${item}</a>
        % endfor
        </span>
	</div>
    % endif
	<div class="box">
        <h2>Todo:</h2>
        <ul>
        <li><a href="${h.url_for(controller='medium', action='mass_add', id=None, page=None, type=None, tag=None)}">Add Medium</a></li>
        <li><a href="${h.url_for(controller='medium', action='list_no_image', id=None, page=None, tag=None)}">Without Image</a></li>
        </ul>
	</div>
</div>
</div>

</body>
</html>

<%def name="side()">
</%def>
