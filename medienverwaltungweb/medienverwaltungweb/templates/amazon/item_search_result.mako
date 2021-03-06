<%inherit file="/layout-default.mako"/>\

<%def name="title()">${c.title}</%def>

<%def name="content()">
<form id="signin-form" method="post" action="${h.url_for(controller='amazon', action='map_to_medium', id=c.item.id)}">
<p>
    <input type="text" name="query" value="${c.query}" />
    <input type="submit" value="${_('Search')}" class="button"/>
</p>
</form>

<form id="signin-form" method="post" name="list" action="${h.url_for(controller='amazon', action='map_to_medium_post', id=c.item.id, query=c.query)}">
<table border=1 class='simple'>
    <tr>
        <td class='simple'>&nbsp;</td>
        <td class='simple'>${_('Image')}</td>
        <td class='simple'>${_('Title')}</td>
        <td class='simple'>${_('Actors')}</td>
        <td class='simple'>${_('Director')}</td>
        <td class='simple'>${_('ASIN')}</td>
    </tr>
    % for item in c.selected_items:
    ${self.row(item, True)}
    %endfor
    % for item in c.items:
    ${self.row(item, False)}
    %endfor
</table>
<input type="hidden" name="media_id" value="${c.item.id}" />
<input type="hidden" name="page" value="${c.page}" />
<input type="hidden" name="query" value="${c.query}" />
<p>
    <input type="submit" value="${_("Attach to '%s'") % c.item.title}" class="button"/>
    % if len(c.items) > 0:
    <input type="submit" name='next_page' value="${_("Next Page")}" class="button"/>
    % endif
</p>
</form>
</%def>


<%def name="row(item, selected)">
<tr>
    <td class='simple'>
        <input type="checkbox" name="item_id_${item.ASIN}" value="${item.ASIN}" ${h.iif(selected, 'checked="true"', '')}>
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
    <td class='simple'>
        <p>${unicode(item.ItemAttributes.Title)}</p>
    </td>
    <td class='simple'>
        % if 'Actor' in item.ItemAttributes.__dict__:
        <ul>
            % for subitem in item.ItemAttributes.Actor:
            <li>${subitem}</li>
            % endfor
        </ul>
        % endif
    </td>
    <td class='simple'>
        % if 'Director' in item.ItemAttributes.__dict__:
        <ul>
            % for subitem in item.ItemAttributes.Director:
            <li>${subitem}</li>
            % endfor
        </ul>
        % endif
    </td>
    <td class='simple'><a href="${h.url_for(controller='amazon', action='show_asin', id=item.ASIN)}">${item.ASIN}</a></td>
</tr>
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
