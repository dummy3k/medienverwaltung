<%inherit file="/layout-default.mako"/>\

<%def name="title()">${_("Amazon Search Results")}</%def>

<%def name="content()">
<form id="signin-form" method="post" action="${h.url_for(query=None)}">
<p>
    <input type="text" name="query" value="${c.query}" />
    <input type="submit" value="${_('Search')}" class="button"/>
</p>
</form>

<form id="signin-form" method="post" name="list" action="${h.url_for(action='map_to_medium_post')}">
<table border=1 class='simple'>
    <tr>
        <td class='simple'>&nbsp;</td>
        <td class='simple'>${_('Image')}</td>
        <td class='simple'>${_('Title')}</td>
        <td class='simple'>${_('ASIN')}</td>
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
        <td class='simple'><nobr>${_("No image available")}</nobr></td>
        %endif
        <td class='simple'>${unicode(item.ItemAttributes.Title)}</td>
        <td class='simple'><a href="${h.url_for(action='show_asin', id=item.ASIN)}">${item.ASIN}</a></td>
    </tr>
    %endfor
</table>
<input type="hidden" name="media_id" value="${c.item.id}" />
<p><input type="submit" value="${_("Attach to '%s'") % c.item.title}" class="button"/></p>
</form>
</%def>


<%def name="side()">
	<div class="box">
        <h2>${_("Actions")}:</h2>
        <ul>
        <li><a href="${h.url_for(controller='medium', action='next_without_image', id=c.item.id)}">${_("Next w/o Image")}</a></li>
        </ul>
	</div>
	<div class="box">
        <h2>${_("Hint")}:</h2>
        ${_("If you click on the small image the checkbox toggles.")}
	</div>
</%def>
