<%inherit file="/layout-default.mako"/>\
<%namespace name='medium_block' file='../medium/medium_block.mako' />

<%def name="title()">Borrow - "${c.item.title}"</%def>

<%def name="content()">
% if c.item.image_data:
<div style="float:right">
<p><img src="${h.url_for(controller='medium', action='image', width=400, height=300, id=c.item.id)}" /><p>
<p>${c.item.title}</p>
</div>
% endif

<form id="signin-form" method="post" action="${h.url_for(action='checkout_post', id=None)}">
<table border=1 class='simple'>
    <tr>
        <td class='simple'>${_('Medium')}</td>
        <td class='simple' width="100%">
            ${medium_block.medium_block(c.item)}
        </td>
    </tr>
    <tr>
        <td class='simple'>${_('Borrower')}</td>
        <td class='simple'>
            <select name="borrower">
                <option value="-1">${_('Add New')}</option>
                % for item in c.borrowers:
                <option value="${item.id}">${item.first_name} ${item.last_name}</option>
                % endfor
            </select>
        </td>
    </tr>
</table>
<input type="hidden" name="media_id" value="${c.item.id}" />
<p>
##<input type="hidden" name="return_to" value="${request.params.get('return_to')}"/>
<input type="submit" value="Borrow"/>
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
