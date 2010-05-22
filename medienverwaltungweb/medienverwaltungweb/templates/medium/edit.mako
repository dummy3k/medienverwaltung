<%inherit file="/layout-default.mako"/>\
<%namespace name='person_snippets' file='/person/snippets.mako' />

<%def name="title()">${_("Edit Medium")} - "${c.item.title}"</%def>

<%def name="content()">
% if c.item.image_data:
<div style="float:right">
<p>
    <a href="${h.url_for(action='raw_image')}">
    <img src="${h.url_for(controller='image', action='thumbnail', width=200, height=300)}" class="plain"/>
    </a>
</p>
</div>
% endif

% if c.borrowed_by:
<p>
${_("This medium ist currently borrowed to %s") % h.tmpl('borrow/snippets.mako', 'link_to_borrower').render_unicode(item=c.borrowed_by, h=h) |n}
</p>
% endif
<form id="mainform" method="post" action="${h.url_for(controller='medium', action='edit_post', id=None)}">
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
    % if c.item.isbn:
    <tr>
        <td class='simple'>${_('ISBN')}</td>
        <td class='simple'>${c.item.isbn}</td>
    </tr>
    % endif
    %for subitem in c.persons:
    <tr>
        <td class='simple'>${_(subitem)}</td>
        <td class='simple'>
        ##<ul>
        % for subsubitem in c.persons[subitem]:
        ##<p>
            <input type="checkbox" name="person_id_${subsubitem.person.id}" value="${subsubitem.person.id}"/>
            ${person_snippets.link_to_person(subsubitem.person, h)}
            ${self.confirm("[X]",
                           h.url_for(controller='person', action='remove_from_media', id=subsubitem.id),
                           _("Do you really want to remove this person from the medium?"))}
        ##</p>
        <br>
        %endfor
        ##</ul>
        </td>
    </tr>
    %endfor
    <tr>
        <td class='simple'>${_('Created')}</td>
        <td class='simple'>${h.strftime(c.item.created_ts)}</td>
    </tr>
    <tr>
        <td class='simple'>${_('Updated')}</td>
        <td class='simple'>${h.strftime(c.item.updated_ts)}</td>
    </tr>
    %if c.asins:
    <tr>
    <td class='simple'>${_('Asins')}</td>
        <td class='simple'><ul>
        %for subitem in c.asins:
        <li>
            <a href="${h.url_for(controller='amazon', action='show_asin', id=subitem)}">
                ${subitem}
            </a>
            ${self.confirm("[X]",
                           h.url_for(controller='amazon', action='remove_asin', asin=subitem),
                           _("Do you really want to remove this ASIN from the medium?"))}
        </li>
        %endfor
    </tr>
    % endif
</table>
<input type="hidden" name="id" value="${c.item.id}" />
##<input type="hidden" name="return_to" value="${request.params.get('return_to')}"/>
<p><input type="submit" value="${_('Save')}" class="button"/></p>
</form>

<h2>${_("Add Person")}</h2>
<form id="signin-form" method="post" action="${h.url_for(controller='person', action='add_to_medium_post', id=c.item.id)}">
<table border=1 class='simple'>
    <tr>
        <td class='simple'>${_('Role')}</td>
        <td class='simple'><select name="role">
            <option value='actor'>${_('Actor')}</option>
            <option value='author'>${_('Author')}</option>
            <option value='director'>${_('Director')}</option>
        </select></td>
    </tr>
    <tr>
        <td class='simple'>${_('Name')}</td>
        <td class='simple'><input type="text" name="name" value="" size=50 /></td>
    </tr>
</table>
<p><input type="submit" value="${_('Add')}" class="button"/></p>
</form>
</%def>


<%def name="side()">
	<div class="box">
    <h2>${_('Actions')}:</h2>
        <ul>
        <li><a href="${h.url_for(controller='amazon', action='map_to_medium', id=c.item.id)}">${_("Attach to Amazon")}</a></li>
        ##FIXME <li><a href="${h.url_for(controller='medium', action='next_without_image', id=c.item.id, return_to=h.url_for())}">${_("Next w/o Image")}</a></li>
        % if len(c.item.asins) > 0:
        <li><a href="${h.url_for(controller='amazon', action='query_images', id=c.item.id)}">${_("Select image from Amazon")}</a></li>
        % endif
        % if c.item.image_data:
        <li><a href="${h.url_for(controller='medium', action='crop_image', id=c.item.id)}">${_("Crop Image")}</a></li>
        % endif
        <li><a href="${h.url_for(controller='borrow', action='checkout', id=c.item.id)}">${_("Borrow")}</a></li>
        ##<li><a style="cursor:pointer" onclick="if (confirm('${_("Really delete this medium?")}')) {location.href = '${h.url_for(controller='medium', action='delete_one')}';}">${_("Delete '%s'") % c.item.title}</a></li>
        <li>
            ${self.confirm(_("Delete '%s'") % c.item.title,
                           h.url_for(controller='medium', action='delete_one', return_to=request.params.get('return_to')),
                           _("Really delete this medium?"))}
        </li>
    </ul>
	</div>
	<div class="box">
    <h2>${_('Persons')}:</h2>
        % if len(c.item.asins) > 0:
        <li><a href="${h.url_for(controller='amazon', action='query_actors', id=c.item.id)}">${_("Query Amazon")}</a></li>
        % endif
        <li><a href="${h.url_for(controller='amazon', action='clear_persons', id=c.item.id)}">${_("Remove all Persons")}</a></li>
        ##FIXME <li><a class="jslink" onclick="document.forms['mainform'].action='${h.url_for(controller='person', action='merge', id=None, return_to=h.url_for())}';document.forms['mainform'].submit();return true;">${_("Merge marked Persons")}</a></li>
    </ul>
	</div>
    % if c.tags:
	<div class="box">
    <h2>${_("Tags")}:</h2>
        % for item in c.tags[:10]:
        <a href="${h.url_for(action='list', tag=item[0], page=None, id=None)}">${item[0]}&nbsp;(${item[1]})</a>
        % endfor
    </span>
	</div>
    % endif
</%def>
