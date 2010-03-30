<%inherit file="/layout-default.mako"/>\

<%def name="title()">Edit Item - "${c.item.title}"</%def>

<%def name="content()">
% if len(c.item.asins) > 0:
<div style="float:right">
<p><img src="${h.url_for(action='image', width=400, height=300)}" /><p>
</div>
% endif

<form id="signin-form" method="post" action="${h.url_for(action='edit_post', id=None)}">
<table border=1 class='simple'>
    <tr>
        <td class='simple'>${_('Id')}</td>
        <td class='simple'>${c.item.id}</td>
    </tr>
    <tr>
        <td class='simple'>${_('Title')}</td>
        <td class='simple'><input type="text" name="title" value="${c.item.title}" /></td>
    </tr>
    %for subitem in c.persons:
    <tr>
        <td class='simple'>${_(subitem)}</td>
        <td class='simple'><ul>
        %for subsubitem in c.persons[subitem]:
        <li><a href="${h.url_for(controller='person', action='index', id=subsubitem.id)}">
                ${subsubitem.name}
        </a></li>
        %endfor
        </ul></td>
    </tr>
    %endfor
    <tr>
    <td class='simple'>${_('Asins')}</td>
        <td class='simple'><ul>
        %for subitem in c.asins:
        <a href="${h.url_for(controller='amazon', action='show_asin', id=subitem)}">
        <li>${subitem}</li>
        %endfor
    </tr>
</table>
<input type="hidden" name="id" value="${c.item.id}" />
<p>
<input type="submit" value="Save"/>
</p>
</form>

<p>
<form id="signin-form" method="post" action="${h.url_for(action='delete', id=None)}">
    <input type="hidden" name="item_id_${c.item.id}" value="${c.item.id}">
    <input type="submit" value="Delete"/>
</form>
</p>
</%def>


<%def name="side()">
	<div class="box">
        <h2>Actions:</h2>
        <ul>
        <li><a href="${h.url_for(controller='amazon', action='map_to_medium', id=c.item.id)}">Attach to Amazon</a></li>
        <li><a href="${h.url_for(controller='medium', action='next_without_image', id=c.item.id)}">Next w/o Image</a></li>
        % if len(c.item.asins) > 0:
        <li><a href="${h.url_for(controller='amazon', action='query_actors', id=c.item.id)}">Query Amazon</a></li>
        <li><a href="${h.url_for(controller='amazon', action='query_images', id=c.item.id)}">Select image from Amazon</a></li>
        % endif
        </ul>
	</div>
</%def>
