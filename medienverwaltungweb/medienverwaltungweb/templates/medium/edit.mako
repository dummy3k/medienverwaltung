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
</table>
<input type="hidden" name="id" value="${c.item.id}" />
<input type="submit" value="Save"/>
</form>

</%def>
