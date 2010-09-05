<%inherit file="/layout-mobile.mako"/>\
<%namespace name='person_snippets' file='/person/snippets.mako' />

<%def name="title()">${_("Edit Medium")} - "${c.item.title}"</%def>

<%def name="content()">

<h1>${c.item.title}</h1>

##<SCRIPT language="JavaScript">
##<!--
##document.write("width: " + window.innerWidth + "<br>");
##document.write("height: " + window.innerHeight + "<br>");
##//-->
##</SCRIPT>


% if c.item.image_data and True:
<div style="float:right">
##<p>
    <a href="${h.url_for(controller='image', action='raw_image', id=c.item.id)}">
    <img src="${h.url_for(controller='image', action='thumbnail', id=c.item.id, width=100, height=300)}" class="plain"/>
    </a>
##</p>
</div>
% endif

% if c.borrowed_by:
<p>
${_("This medium ist currently borrowed to %s") % h.tmpl('borrow/snippets.mako', 'link_to_borrower').render_unicode(item=c.borrowed_by, h=h) |n}
</p>
% endif
<form id="mainform" method="post" action="${h.url_for(controller='medium', action='edit_post')}">
<table border=1 class='simple'>
    <tr>
        <td class='simple'>${_('Id')}</td>
        <td class='simple'>${c.item.id}</td>
    </tr>
    <tr>
        <td class='simple'>${_('Tags')}</td>
        <td class='simple'>${c.item.get_tagstring()}</td>
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

##<input type="hidden" name="id" value="${c.item.id}" />
##<input type="hidden" name="return_to" value="${request.params.get('return_to')}"/>
##<p><input type="submit" value="${_('Save')}" class="button"/></p>
</form>

</%def>
