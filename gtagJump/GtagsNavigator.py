#-*- coding:utf-8 -*-

import subprocess
import re
class GtagsNavigator:
	def getDefinitions(self, doc, identifier):
		try:
			ps_global = subprocess.Popen(["global", "-x"] + [identifier], stdout=subprocess.PIPE)
			for pathline in self.parse(ps_global, identifier):
				yield pathline
		except OSError:
			pass
		finally:
			if not ps_global is None:
				ps_global.stdout.close()
	def getReferences(self, doc, identifier):
		try:
			ps_global = subprocess.Popen(["global", "-rx"] + [identifier], stdout=subprocess.PIPE)
			for pathline in self.parse(ps_global, identifier):
				yield pathline
		except OSError:
			pass
		finally:
			if not ps_global is None:
				ps_global.stdout.close()
	def parse(self, ps_global, identifier):
		for line in ps_global.stdout:
			pathline = self.resultLineToLocation(identifier, line)
			if not pathline is None:
				yield pathline
	def resultLineToLocation(self, identifier, line):
		matchObj = re.search("^" + identifier + " +[0-9]+", line)
		if matchObj is None:
			return None
		l = int(matchObj.group(0)[len(identifier):])
		matchObj = re.search("^ *[^ ]+ *", line[matchObj.end():])
		if matchObj is None:
			return None
		path = matchObj.group(0).strip()
		return path, l, ""
