// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

wn.provide('erpnext');

// add toolbar icon
$(document).bind('toolbar_setup', function() {
	wn.app.name = "Wamssler";
	
	var brand = ($("<div></div>").append(wn.boot.website_settings.brand_html).text() || '');
	$('.navbar-brand').html('<div style="display: inline-block;">\
			<img src="files/wamssler_logoi.png" alt="Smiley face" height="30" width="170">\
		</div>' + brand)
	.attr("title", brand)
	.addClass("navbar-icon-home")
	.css({
		"max-width": "200px",
		"overflow": "hidden",
		"text-overflow": "ellipsis",
		"white-space": "nowrap"
	});
});

wn.provide('wn.ui.misc');
wn.ui.misc.about = function() {
	if(!wn.ui.misc.about_dialog) {
		var d = new wn.ui.Dialog({title: wn._('About')})
	
		$(d.body).html(repl("<div>\
		<h2>Wamssler</h2>  \
		<p><strong>v" + wn.boot.app_version + "</strong></p>\
		<p>"+wn._("An open source ERP made for the web.</p>") +	"<p></div>", wn.app));
	
		wn.ui.misc.about_dialog = d;		
	}
	
	wn.ui.misc.about_dialog.show();
}
