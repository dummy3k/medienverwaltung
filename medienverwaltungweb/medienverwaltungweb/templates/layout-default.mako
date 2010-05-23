<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

    <title>${self.title()} - ${config['page_title']}</title>

	<link href="/css/default.css" media="screen" rel="stylesheet" type="text/css" />
	<link href="/css/awesome-buttons.css" media="screen" rel="stylesheet" type="text/css" />
    <link href="/css/ui-lightness/jquery-ui-1.7.2.custom.css" media="screen" rel="stylesheet" type="text/css" />
    <link href="/css/minimalistic/style.css" rel="stylesheet" type="text/css" media="screen" />
    <script src="/js/jquery-1.4.2.min.js" type="text/javascript"></script>
	<script src="/js/application.js" type="text/javascript"></script>
    <link rel="shortcut icon" href="/css/book_open.ico" type="image/vnd.microsoft.icon">
    <link rel="icon" href="/css/book_open.ico" type="image/vnd.microsoft.icon">
    % for x in c.rss_feeds:
    <link rel="alternate" type="application/rss+xml" title="${x['title']}" href="${x['link']}" />
    % endfor
    ${self.html_head()}
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
    <li><a href="${h.url_for(controller='medium', action='list_gallery', id=None, page=None, type='books', tag=None)}">${_('Books')}</a></li>
    <li><a href="${h.url_for(controller='medium', action='list_gallery', id=None, page=None, type='dvds', tag=None)}">${_('DVDs')}</a></li>
    <li><a href="${h.url_for(controller='person', action='top_ten', id=None, page=None, type=None, tag=None)}">${_('Persons')}</a></li>
    <li><a href="${h.url_for(controller='borrow', action='list_borrowed_media', id=None, page=None, type=None, tag=None)}">${_('Borrow')}</a></li>
  </ul>
 </div>
</div>

<% flashes = h.flash.pop_messages() %>
% if flashes:
    % for flash in flashes:
        <div class="ui-state-highlight ui-corner-all">
            <span class="ui-icon ui-icon-info">&nbsp;</span>
            <span class="flash-text">${unicode(flash)|n}</span>
        </div>
    % endfor
% endif

<div id="content">

<div id="right">
    <h1>${self.title()}</h1>
    ${self.content()}
</div>
<div id="left">
    ${self.side()}
	<div class="box">
        <h2>${_("Todo")}:</h2>
        <ul>
        <li><a href="${h.url_for(controller='medium', action='mass_add', id=None, page=None, type=None, tag=None)}">${_("Add Media")}</a></li>
        <li><a href="${h.url_for(controller='medium', action='list_no_image', id=None, page=None, tag=None)}">${_("Media without Image")}</a></li>
        </ul>
	</div>
	<div class="box">
        <h2>${_("Search")}:</h2>
        <form id="signin-form" method="post" action="${h.url_for(controller='search', action='search_post', id=None, page=None, tag=None, type=None)}">
			<table border="0" cellspacing="0" cellpadding="0">
			<tr><td>
				<input type="text" name="query" style="width: 93%" />
			</td><td>
				<input type="submit" value="${_('Search')}" class="button" style="width: 100%"/>
</td></tr></table>
        </form>
	</div>
</div>
</div>

</body>
</html>

<%def name="side()">
</%def>

<%def name="html_head()">
</%def>

<%def name="confirm(text, url, question)">\
<a class="jslink" onclick="if (confirm('${question}')) {location.href = '${url}';}">${text}</a>
</%def>
