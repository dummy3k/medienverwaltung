<%inherit file="/layout-default.mako"/>\

<%def name="title()">All Media</%def>

<%def name="content()">
<p>
<a href="${h.url_for(action='mass_add', id=None)}">Add Medium</a>
</p>

<table border=1 class='simple'>
    <tr>
        <td class='simple'>${_('Id')}</td>
        <td class='simple'>${_('Title')}</td>
##        <td class='simple'>${_('Actions')}</td>
    </tr>

    % for item in c.items:
    <tr>
        <td class='simple'>${item.id}</td>
        <td class='simple'>${item.title}</td>
##        <td class='simple'><a href="${h.url_for(action='add_asin', id=item.ASIN)}">Add this to db</a></td>
    </tr>
    %endfor
</table>
</%def>
