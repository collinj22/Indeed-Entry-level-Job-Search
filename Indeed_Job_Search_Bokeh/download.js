js_download = """
var csv = source.get('data');
var filetext = 'itemnum,storename,date,usage,netsales\\n';
for (i=0; i < csv['date'].length; i++) {
    var currRow = [csv['itemnum'][i].toString(),
                   csv['storename'][i].toString(),
                   csv['date'][i].toString(),
                   csv['usage'][i].toString(),
                   csv['netsales'][i].toString().concat('\\n')];

    var joined = currRow.join();
    filetext = filetext.concat(joined);
}

var filename = 'results.csv';
var blob = new Blob([filetext], { type: 'text/csv;charset=utf-8;' });
if (navigator.msSaveBlob) { // IE 10+
navigator.msSaveBlob(blob, filename);
} else {
var link = document.createElement("a");
if (link.download !== undefined) { // feature detection
    // Browsers that support HTML5 download attribute
    var url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
}""