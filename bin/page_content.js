
if (phantom.args.length < 1) {
    console.log('Usage: <url>');
    phantom.exit();
}
else {
    var page = new WebPage();
    page.settings.userAgent = '_PHANTOMJS_BOT_';
    
    page.onLoadFinished = function (status) {
        var html = page.evaluate(function () {
            return document.getElementsByTagName('html')[0].innerHTML;
        });

        console.log('<html>' + html + '</html>');
        phantom.exit();
    };

    page.open(phantom.args[0]);
}
