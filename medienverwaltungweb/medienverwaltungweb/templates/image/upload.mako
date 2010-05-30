<%inherit file="/layout-default.mako"/>\

<%def name="title()">${_("Manually add Image to Media")}</%def>

<%def name="content()">

<h2>${_("Upload local File")}</h2>
<form method="post" action="${h.url_for(controller='image', action='upload_post', id=c.id)}" enctype="multipart/form-data">
<p><input type="file" name="myfile"></p>
<p><input type="submit" value="${_("Upload")}" class="button" /></p>
</form>

<h2>${_("Fetch URL")}</h2>
<form method="post" action="${h.url_for(controller='image', action='download_post', id=c.id)}" enctype="multipart/form-data">
<p><input type="text" name="url" size='90'></p>
<p><input type="submit" value="${_("Fetch")}" class="button"/></p>
</form>

</%def>
