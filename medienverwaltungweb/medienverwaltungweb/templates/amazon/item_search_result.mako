<%inherit file="/layout-default.mako"/>\

<%def name="title()">Item Search Results</%def>

<%def name="content()">
<form id="signin-form" method="post" action="${h.url_for(query=None)}">
<p>
    Query: <input type="text" name="query" value="${c.query}" />
    <input type="submit" value="Search"/>
</p>
</form>

<form id="signin-form" method="post" name="list" action="${h.url_for(action='map_to_medium_post')}">
<table border=1 class='simple'>
    <tr>
        <td class='simple'>&nbsp;</td>
        <td class='simple'>${_('Image')}</td>
        <td class='simple'>${_('ASIN')}</td>
        <td class='simple'>${_('Title')}</td>
        <td class='simple'>${_('Actions')}</td>
    </tr>

    % for item in c.items:
    <tr>
        <td class='simple'>
            <input type="checkbox" name="item_id_${item.ASIN}" value="${item.ASIN}">
        </td>
        %if 'SmallImage' in dir(item):
        <td class='simple'>
            <a onclick="document.list.item_id_${item.ASIN}.checked = !document.list.item_id_${item.ASIN}.checked;">
                <img src="${unicode(item.SmallImage.URL)}" />
            </a>
        </td>
        %else:
        <td class='simple'>No image available</td>
        %endif
        <td class='simple'>${item.ASIN}</td>
        <td class='simple'>${unicode(item.ItemAttributes.Title)}</td>
        <td class='simple'><a href="${h.url_for(action='show_asin', id=item.ASIN)}">Details...</a></td>
    </tr>
    %endfor
</table>
<input type="hidden" name="media_id" value="${c.item.id}" />
<input type="submit" value="Attach to '${c.item}'"/>
</form>
</%def>


<%def name="side()">
	<div class="box">
        <h2>Actions:</h2>
        <ul>
        <li><a href="${h.url_for(controller='medium', action='next_without_image', id=c.item.id)}">Next w/o Image</a></li>
        </ul>
	</div>
</%def>
