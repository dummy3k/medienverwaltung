<%inherit file="/layout-default.mako"/>\

<%def name="title()">${_("Edit Medium")} - "${c.item.title}"</%def>

<%def name="content()">
% if c.item.image_data:
<div style="float:right">
<p><img src="${h.url_for(action='image', width=400, height=300)}" /><p>
</div>
% endif

% if c.borrowed_by:
<p>
${_("This medium ist currently borrowed to %s") % h.tmpl('borrow/snippets.mako', 'link_to_borrower').render(item=c.borrowed_by, h=h) |n}
</p>
% endif

<form id="signin-form" method="post" action="${h.url_for(action='edit_post', id=None)}">
<table border=1 class='simple'>
    <tr>
        <td class='simple'>${_('Id')}</td>
        <td class='simple'>${c.item.id}</td>
    </tr>
    <tr>
        <td class='simple'>${_('Title')}</td>
        <td class='simple'><input type="text" name="title" value="${c.item.title}" size=50 /></td>
    </tr>
    <tr>
        <td class='simple'>${_('Tags')}</td>
        <td class='simple'><input type="text" name="tags" value="${c.item.get_tagstring()}" size=50 /></td>
    </tr>
    <tr>
        <td class='simple'>${_('Created')}</td>
        <td class='simple'>${c.item.created_ts}</td>
    </tr>
    <tr>
        <td class='simple'>${_('Updated')}</td>
        <td class='simple'>${c.item.updated_ts}</td>
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
    %if c.asins:
    <tr>
    <td class='simple'>${_('Asins')}</td>
        <td class='simple'><ul>
        %for subitem in c.asins:
        <li>
            <a href="${h.url_for(controller='amazon', action='show_asin', id=subitem)}">
                ${subitem}
            </a>
            <a href="${h.url_for(controller='amazon', action='remove_asin', asin=subitem)}">
                [X]
            </a>
        </li>
        %endfor
    </tr>
    % endif
</table>
<input type="hidden" name="id" value="${c.item.id}" />
<input type="hidden" name="return_to" value="${request.params.get('return_to')}"/>
<p><input type="submit" value="${_('Save')}"/></p>
</form>

<h2>Add Person</h2>
<form id="signin-form" method="post" action="${h.url_for(controller='person', action='add_to_medium_post')}">
<table border=1 class='simple'>
    <tr>
        <td class='simple'>${_('Role')}</td>
        <td class='simple'><select name="role">
            <option value='actor'>${_('Actor')}</option>
            <option value='actor'>${_('Author')}</option>
            <option value='actor'>${_('Director')}</option>
        </select></td>
    </tr>
    <tr>
        <td class='simple'>${_('Name')}</td>
        <td class='simple'><input type="text" name="name" value="" size=50 /></td>
    </tr>
</table>
<p><input type="submit" value="${_('Add')}"/></p>

</form>

##<p>
##
##    <input type="hidden" name="item_id_${c.item.id}" value="${c.item.id}" />
##    <input type="hidden" name="return_to" value="${request.params.get('return_to')}"/>
##    <input type="submit" value="Delete"/>
##</form>
##</p>
</%def>


<%def name="side()">
	<div class="box">
        <h2>${_('Actions')}:</h2>
        <ul>
        <li><a href="${h.url_for(controller='amazon', action='map_to_medium', id=c.item.id)}">${_("Attach to Amazon")}</a></li>
        <li><a href="${h.url_for(controller='medium', action='next_without_image', id=c.item.id)}">${_("Next w/o Image")}</a></li>
        % if len(c.item.asins) > 0:
        <li><a href="${h.url_for(controller='amazon', action='query_actors', id=c.item.id)}">${_("Query Amazon")}</a></li>
        <li><a href="${h.url_for(controller='amazon', action='query_images', id=c.item.id)}">${_("Select image from Amazon")}</a></li>
        % endif
        % if c.item.image_data:
        <li><a href="${h.url_for(controller='medium', action='crop_image', id=c.item.id)}">${_("Crop Image")}</a></li>
        % endif
        <li><a href="${h.url_for(controller='borrow', action='checkout', id=c.item.id)}">${_("Borrow")}</a></li>
        <li><a style="cursor:pointer" onclick="if (confirm('${_("Really delete this medium?")}')) {location.href = '${h.url_for(controller='medium', action='delete_one')}';}">${_("Delete '%s'") % c.item.title}</a></li>
        <li><a href="${h.url_for(controller='amazon', action='clear_persons', id=c.item.id)}">${_("Clear Persons")}</a></li>
        </ul>
	</div>
    % if c.tags:
	<div class="box">
        <h2>${_("Tags")}:</h2>
        <span class="tags">
        % for item in c.tags[:10]:
        <a href="${h.url_for(action='list', tag=item[0], page=None, id=None)}">${item[0]}&nbsp;(${item[1]})</a>
        % endfor
        </span>
	</div>
    % endif
</%def>
