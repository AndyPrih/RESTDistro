import sys, select, os, os.path
from zipstream import ZipFile, ZIP_DEFLATED
from DescriptorEntry import DescriptorEntry, recursive_list

def stream_generator(descriptor_entry):
	rpipe, wpipe = os.pipe()
	pid = os.fork()
	if not pid:
		os.close(rpipe)
		zs = ZipFile(mode = 'w', compression = ZIP_DEFLATED)
		for fname in recursive_list(descriptor_entry):
			zs.write(fname.absolute, fname.relative)
		for chunk in zs:
			os.write(wpipe, chunk)
		return
	os.close(wpipe)
	r, _, _ = select.select([rpipe], [], [])
	while True:
		chunk = os.read(rpipe, 4096)
		if not chunk: break
		yield chunk

if __name__ == '__main__':
	if len(sys.argv) <= 1:
		print('use: python3 {script_path} /path/to/save/zip [ /path/that/needed/to/zip ]'.\
			format(script_path = os.path.abspath(__file__)))
	else:
		path_to_save_zip = sys.argv[1]
		path_to_zip = sys.argv[2] if len(sys.argv) >= 3 else ''
		if os.path.exists(path_to_save_zip) and os.path.isdir(path_to_save_zip):
			def zip_stream_reciever(stream):
				with open(os.path.join(path_to_save_zip, 'stream.zip'), 'wb') as fd:
					for chunk in stream:
						fd.write(chunk)
			zip_stream_reciever(stream_generator(DescriptorEntry(path_to_zip)))
