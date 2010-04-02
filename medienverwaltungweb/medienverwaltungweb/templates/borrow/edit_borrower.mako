<%inherit file="/layout-default.mako"/>\
<%namespace name='medium_block' file='../medium/medium_block.mako' />

<%def name="title()">
    % if c.action == 'Add':
    Add new Borrower
    % else:
    Edit Borrower
    % endif
</%def>

<%def name="content()">
<form id="signin-form" method="post" action="${h.url_for(action='edit_borrower_post')}">
<table border=1 class='simple'>
    <tr>
        <td class='simple'><nobr>${_('First Name')}</nobr></td>
        <td class='simple'><input type="text" name="first_name" value="${c.item.first_name}" size=50 /></td>
    </tr>
    <tr>
        <td class='simple'><nobr>${_('Last Name')}</nobr></td>
        <td class='simple'><input type="text" name="last_name" value="${c.item.last_name}" size=50 /></td>
    </tr>
    <tr>
        <td class='simple'><nobr>${_('eMail')}</nobr></td>
        <td class='simple'><input type="text" name="email" value="${c.item.email}" size=50 /></td>
    </tr>
</table>
<p>
##<input type="hidden" name="return_to" value="${request.params.get('return_to')}"/>
<input type="submit" value="${c.action}"/>
</p>
</form>


<p>
<form id="signin-form" method="post" action="${h.url_for(action='delete_borrower_post')}">
    <input type="hidden" name="item_id_${c.item.id}" value="${c.item.id}" />
##    <input type="hidden" name="return_to" value="${request.params.get('return_to')}"/>
    <input type="submit" value="Delete"/>
</form>
</p>
</%def>

