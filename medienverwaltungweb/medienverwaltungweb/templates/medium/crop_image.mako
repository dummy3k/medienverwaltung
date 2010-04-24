<%inherit file="/layout-default.mako"/>\

<%def name="title()">${_("Crop Medium '%s' Image") % c.item.title}</%def>

<%def name="html_head()">
<script src="/js/jcrop/js/jquery.Jcrop.js"></script>
<link rel="stylesheet" href="/js/jcrop/css/jquery.Jcrop.css" type="text/css" />

<script language="Javascript">
    // Remember to invoke within jQuery(window).load(...)
    // If you don't, Jcrop may not initialize properly
    jQuery(document).ready(function(){

        jQuery('#cropbox').Jcrop({
            onChange: showCoords,
            onSelect: showCoords
        });

    });

    // Our simple event handler, called from onChange and onSelect
    // event handlers, as per the Jcrop invocation above
    function showCoords(c)
    {
        jQuery('#x').val(c.x);
        jQuery('#y').val(c.y);
        jQuery('#x2').val(c.x2);
        jQuery('#y2').val(c.y2);
        jQuery('#w').val(c.w);
        jQuery('#h').val(c.h);
    };

</script>
</%def>

<%def name="content()">
<form id="signin-form" method="post" action="${h.url_for(action='crop_image_post')}">
    <label>X1 <input type="text" size="4" id="x" name="x" /></label>
    <label>Y1 <input type="text" size="4" id="y" name="y" /></label>
    <label>X2 <input type="text" size="4" id="x2" name="x2" /></label>
    <label>Y2 <input type="text" size="4" id="y2" name="y2" /></label>
    <label>W <input type="text" size="4" id="w" name="w" /></label>
    <label>H <input type="text" size="4" id="h" name="h" /></label>
    <input type='submit' value='${_("Crop")}' class="button"/>
</form>

<p>
    <img src="${h.url_for(action='raw_image')}" id="cropbox"/>
</p>

</%def>
