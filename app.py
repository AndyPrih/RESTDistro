from flask import Flask, request, Response, abort
from DescriptorEntry import DescriptorEntry, recursive_list
from Zip import stream_generator

app = Flask('RESTDistributive')

def submit(relative, value = "скачать"):
	return """
	<form action="{relative}" method="POST" style="margin: auto;">
		<button type="submit">{value}</button>
	</form>
	""".format(**locals())

def link(relative, value):
	return """<a href ="{relative}">{value}</a>""".format(**locals())

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def landing(path):
	table = DescriptorEntry(path)
	if not table.is_exists:
		abort(404)
	if request.method == 'GET':
		# GET meth
		parent = '<tr><td width="75px"/><td><a href = "{relative}">..</a></td></tr>'.\
			format(relative = table.parent.relative) if not table.is_root else ''
		table_html = ''
		for i in table:
			_submit = submit(relative = i.relative)
			_link = link(relative = i.relative, value = str(i)) if i.is_dir else str(i)
			table_html += '<tr><td width="75px">{_submit}</td><td>{_link}</td></tr>'.format(**locals())
		download_all = '<tr><td colspan=2>%s</td></tr>' % \
			submit(relative = "", value = "скачать всё") if len(table) else ''
		return '<table>{parent}{table_html}{download_all}</table>'.format(**locals())
	# POST meth
	response = Response(stream_generator(table), mimetype='application/zip')
	response.headers['Content-Disposition'] = 'attachment; filename={name}.zip'.\
		format(name = str(table) or 'files')
	return response

if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 8080)