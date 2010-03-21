<%inherit file="/layout-default.mako"/>\

<%def name="title()">Edit Item</%def>

<%def name="content()">

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
<input type="submit" value="Save"/>
</form>

<a href="${h.url_for(controller='amazon', action='map_to_medium', id=c.item.id)}">Attach to Amazon</a>
<a href="${h.url_for(controller='amazon', action='query_actors', id=c.item.id)}">Query Amazon</a>
</%def>
