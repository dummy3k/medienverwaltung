<%inherit file="/layout-default.mako"/>\

<%def name="title()">Add Item to DB</%def>

<%def name="content()">
<h1>Add one</h1>

<form id="signin-form" method="post" action="${h.url_for(action='mass_add_post')}">
    <input type="text" name="title"/>
    <input type="submit" value="Process"/>
</form>

<h1>Add many</h1>

<form id="signin-form" method="post" action="${h.url_for(controller='login', action='signin_POST')}">
    <textarea name="user_eingabe" cols="50" rows="10"></textarea>
    ##<input type="text" name="openid" id="openid" class="openid-identifier" />
    <input type="submit" value="Process"/>
</form>

</%def>
