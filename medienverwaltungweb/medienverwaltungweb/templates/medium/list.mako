<%inherit file="/layout-default.mako"/>\

<%def name="title()">All Media</%def>

<%def name="content()">
<p>
<a href="${h.url_for(action='mass_add', id=None)}">Add Medium</a>
</p>

<form id="signin-form" method="post" action="${h.url_for(action='delete')}">
<table border=1 class='simple'>
    <tr>
        <td class='simple'>&nbsp;</td>
        <td class='simple'>${_('Id')}</td>
        <td class='simple'>${_('Title')}</td>
##        <td class='simple'>${_('Actions')}</td>
    </tr>

    % for item in c.items:
    <tr>
        <td class='simple'>
            <input type="checkbox" name="item_id_${item.id}" value="${item.id}">
            <a href="${h.url_for(action='edit', id=item.id)}">Edit</a>
        </td>
        <td class='simple'>${item.id}</td>
        <td class='simple'>${item.title}</td>
##        <td class='simple'><a href="${h.url_for(action='add_asin', id=item.ASIN)}">Add this to db</a></td>
    </tr>
    %endfor
</table>

<p>
<input type="submit" value="Delete marked Media"/>
##<a href="${h.url_for(action='delete', id=None)}">Delete marked Media</a>
</p>
</form>
</%def>
