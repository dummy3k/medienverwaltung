<%inherit file="/layout-default.mako"/>\
<%!
    import urllib
%>

<%def name="title()">Edit Iser '${unicode(c.item.name, errors='replace')}' (${c.item.id})</%def>

<%def name="content()">
<div style="float:right">
<iframe src="http://de.wikipedia.org/wiki/${urllib.quote(c.item.name)}" width="600" height="600" name="SELFHTML_in_a_box">
  <p>no iframe</a></p>
</iframe>
</div>

<form id="signin-form" method="post" action="${h.url_for(controller='person', action='edit_post', id=None)}">
<table border=1 class='simple'>
    <tr>
        <td class='simple'>${_('Id')}</td>
        <td class='simple'>${c.item.id}</td>
    </tr>
    <tr>
        <td class='simple'>${_('Name')}</td>
        <td class='simple'><input type="text" name="title" value="${unicode(c.item.name, errors='replace')}" /></td>
    </tr>
</table>
<input type="hidden" name="id" value="${c.item.id}" />
<input type="submit" value="Save"/>
</form>

##<a href="${h.url_for(controller='amazon', action='map_to_medium', id=c.item.id)}">Attach to Amazon</a>
##<a href="${h.url_for(controller='amazon', action='query_actors', id=c.item.id)}">Query Amazon</a>

<h2>Actor in...</h2>
<p>${c.page.pager()}</p>
<ul>
%for item in c.page.items:
    <li><a href="${h.url_for(controller='medium', action='edit', id=item.id)}">${item.title}</a></li>
%endfor
</ul>
<p>${c.page.pager()}</p>

</%def>
