<%inherit file="/layout-default.mako"/>\
<%namespace name='medium_block' file='../medium/medium_block.mako' />

<%def name="title()">Add new Borrower</%def>

<%def name="content()">
<form id="signin-form" method="post" action="${h.url_for(action='add_borrower_post')}">
<table border=1 class='simple'>
    <tr>
        <td class='simple'><nobr>${_('First Name')}</nobr></td>
        <td class='simple'><input type="text" name="first_name" value="" size=50 /></td>
    </tr>
    <tr>
        <td class='simple'><nobr>${_('Last Name')}</nobr></td>
        <td class='simple'><input type="text" name="last_name" value="" size=50 /></td>
    </tr>
    <tr>
        <td class='simple'><nobr>${_('eMail')}</nobr></td>
        <td class='simple'><input type="text" name="email" value="" size=50 /></td>
    </tr>
</table>
<p>
##<input type="hidden" name="return_to" value="${request.params.get('return_to')}"/>
<input type="submit" value="Add"/>
</p>
</form>
</%def>


##<%def name="side()">
##	<div class="box">
##        <h2>Actions:</h2>
##        <ul>
##        <li><a href="${h.url_for(controller='amazon', action='map_to_medium', id=c.item.id)}">Attach to Amazon</a></li>
##        <li><a href="${h.url_for(controller='medium', action='next_without_image', id=c.item.id)}">Next w/o Image</a></li>
##        % if len(c.item.asins) > 0:
##        <li><a href="${h.url_for(controller='amazon', action='query_actors', id=c.item.id)}">Query Amazon</a></li>
##        <li><a href="${h.url_for(controller='amazon', action='query_images', id=c.item.id)}">Select image from Amazon</a></li>
##        % endif
##        <li><a href="${h.url_for(controller='borrow', action='borrow', id=c.item.id)}">Borrow</a></li>
##        </ul>
##	</div>
##</%def>
