import select
import sys
import os
import os.path
from zipstream import ZipFile, ZIP_DEFLATED  # type: ignore[import]
from DescriptorEntry import DescriptorEntry, recursive_list


def shrink(path, shrink_part):
    return path[path.find(shrink_part) + len(shrink_part):]


def stream_generator(descriptor_entry):
    rpipe, wpipe = os.pipe()
    pid = os.fork()
    if not pid:
        os.close(rpipe)
        zs = ZipFile(mode='w', compression=ZIP_DEFLATED)
        shrink_part = getattr(descriptor_entry.parent, 'relative', '')
        for fname in recursive_list(descriptor_entry):
            zip_path = (
                shrink(fname.relative, shrink_part)
                if shrink_part != '.'
                else fname.relative)
            zs.write(fname.absolute, zip_path)
        for chunk in zs:
            try:
                _ = os.write(wpipe, chunk)
            except (BrokenPipeError, IOError):
                break
        os.close(wpipe)
        return
    os.close(wpipe)
    try:
        while True:
            r, _, _ = select.select([rpipe], [], [], 15)
            if not r:
                break
            chunk = os.read(rpipe, 4096)
            if not chunk:
                break
            yield chunk
    finally:
        # fuck the zombies!
        os.close(rpipe)
        os.wait()


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print(
            (
                'use: python3 {script_path}'
                ' /path/to/save/zip'
                '[ /path/that/needed/to/zip ]'
            )
            .format(script_path=os.path.abspath(__file__))
        )
    else:
        path_to_save_zip = sys.argv[1]
        path_to_zip = sys.argv[2] if len(sys.argv) >= 3 else ''
        if (os.path.exists(path_to_save_zip)
                and os.path.isdir(path_to_save_zip)):
            def zip_stream_reciever(stream):
                with open(
                        os.path.join(path_to_save_zip, 'stream.zip'),
                        'wb') as fd:
                    for chunk in stream:
                        fd.write(chunk)
            zip_stream_reciever(stream_generator(DescriptorEntry(path_to_zip)))
