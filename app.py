from flask import Flask, request, Response, abort
from DescriptorEntry import DescriptorEntry, recursive_list
from Zip import stream_generator

app = Flask('RESTDistributive')

@app.route('/download/', defaults={'path': ''})
@app.route('/download/<path:path>')
def download(path):
	table = DescriptorEntry(path)
	if not table.is_exists:
		abort(404)
	response = Response(stream_generator(table), mimetype='application/zip')
	response.headers['Content-Disposition'] = 'attachment; filename={name}.zip'.\
		format(name = str(table) or 'files')
	return response

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def landing(path):
	ul = ''
	table = DescriptorEntry(path)
	if not table.is_exists:
		abort(404)
	parent = '<li><a href = "{relative}">..</a></li>'.\
		format(relative = table.parent.relative) if not table.is_root else ''
	for i in table:
		if i.is_dir:
			ul += '<li><a href = "/download/{relative}">скачать</a> <a href = "{relative}">{name}</a></li>'.\
				format(relative = i.relative, name = i)
			continue
		ul += '<li><a href = "download/{relative}">скачать</a> {name}</li>'.\
			format(relative = i.relative, name = i)
	download_all = '<a href = "/download/{relative}">скачать все файлы</a>'.\
		format(relative = table.relative) if len(table) else ''
	return '<ul>{parent}{ul}{download_all}</ul>'.format(**locals())

if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 8080)