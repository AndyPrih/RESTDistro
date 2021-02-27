import re, sys, os, os.path
from itertools import count

DEFAULT_ROOT = r'T:\Downloads' if os.name == 'nt' else '/var/log'
ROOT = os.environ.get('MOUNT_POINT', DEFAULT_ROOT)

absolute_path = lambda relative_path: os.path.join(ROOT, relative_path)

class DescriptorEntry:
	def __init__(self, relative = ''):
		if re.match(re.compile(r'\.\.[\\\/]'), relative) or re.search(re.compile(r'[\\\/]\.\.[\\\/]'), relative):
			raise ValueError('Bad path %s' % relative)
		self._relative = relative
	def __iter__(self):
		if self.is_dir:
			self._files = os.listdir(self.absolute) or [self.absolute,]
		elif self.is_file:
			self._files = [self.absolute,]
		else:
			self._files = None
			raise ValueError('This is not file or Directory')
		self._iterator = count()
		return self
	def __next__(self):
		offset = next(self._iterator)
		if offset == len(self._files):
			raise StopIteration
		entry = self.__class__( os.path.join(self.relative, self._files[offset]) )
		if not entry.is_exists or entry.is_link:
			return next(self)
		return entry
	@property
	def relative(self):
		return self._relative
	@property
	def absolute(self):
		return absolute_path(self.relative)
	@property
	def is_dir(self):
		return os.path.isdir(self.absolute)
	@property
	def is_file(self):
		return os.path.isfile(self.absolute)
	@property
	def is_link(self):
		return os.path.islink(self.absolute)
	@property
	def is_exists(self):
		return os.path.exists(self.absolute)
	def __len__(self):
		if self.is_file:
			return 1
		elif self.is_dir:
			return len(os.listdir(self.absolute))
		else:
			return None
	def __str__(self):
		return self.relative

def recursive_list(descriptor_entry):
	for i in descriptor_entry:
		if i.is_dir:
			if len(i):
				yield from recursive_list(i)
			else:
				yield i
		elif i.is_file:
			yield i

if __name__ == '__main__':
	for i in recursive_list(DescriptorEntry()):
		print(i.absolute)