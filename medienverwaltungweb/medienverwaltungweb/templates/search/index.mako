<%inherit file="/layout-default.mako"/>\

<%def name="title()">${_("Search")}</%def>

<%def name="content()">
<form id="signin-form" method="post" action="${h.url_for(controller='person', action='search_post')}">
    <input type="text" name="query"/>
    <input type="submit" value='${_("Find")}' class="button"/>
</form>
</%def>
