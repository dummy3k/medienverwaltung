<%inherit file="/layout-mobile.mako"/>\

<%def name="title()">${_("New Medium")} - "${c.response['title']}"</%def>

<%def name="content()">

<h1>${c.response['title']}</h1>

##<SCRIPT language="JavaScript">
##<!--
##document.write("width: " + window.innerWidth + "<br>");
##document.write("height: " + window.innerHeight + "<br>");
##//-->
##</SCRIPT>

% if c.response['image_url']:
<div style="float:right">
##    <a href="${h.url_for(controller='image', action='raw_image', id=c.item.id)}">
    <img src="${c.response['image_url']}" class="plain"/>
##    </a>
</div>
% endif

<span class='field_name'>${_('ISBN')}</span>
<span class='field_value'>${c.response['isbn']}</span>
% for person_type in c.response['persons'].keys():
<div>
<span class='field_name'>${_(person_type)}</span>
<span class='field_value'>${", ".join(c.response['persons'][person_type])}</span>
</div>
% endfor

</%def>
