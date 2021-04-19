import os, sys, time
import socket, subprocess, urllib.request, urllib.parse, urllib.error
import datetime, traceback

import nsUI
from nsUI.command import clear_old_results, get_opts_remote
from nsUI import config
def main():
	cmd_opts, args = get_opts_remote()
	config_obj = config.Configuration()
	config_obj.set_opts(cmd_opts)
	from nsUI import runtests
	print('--------------------------------------------------------------')
	print('starting nsUI...')

	cleanups = []

	if config_obj.options["xserver_headless"]:
		from nsUI.xvfbdisplay import Xvfb
		print('\nstarting virtual display...')
		display = Xvfb(width=1280, height=1024)
		display.start()
		cleanups.append(('\nstopping virtual display...', display.stop))

	if not cmd_opts.quiet:
		print('')
		print(('  date time: %s' \
			% datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
		print(('  test directory: %r' % config_obj.options["dir_name"]))
		print(('  report format: %r' % config_obj.options["report_format"]))
		print(('  browser type: %r' % config_obj.options["browser_type"]))
		print(('  javascript disabled: %r' % cmd_opts.javascript_disabled))
		print(('  shared directory: %r' % config_obj.options["shared_modules"]))
		print(('  screenshots on error: %r' % config_obj.options["screenshots_on"]))
		print(('  failfast: %r' % config_obj.options["failfast"]))
		print(('  debug: %r' % config_obj.options["debug"]))
		print(('  headless xserver: %r' % config_obj.options["xserver_headless"]))
		print('')

	if config_obj.options["cleanup"]:
		from nsUI.util.common import cleanup
		cleanup.testmachine_cleanup()

	try:
		from nsUI.util.common import racetrack
		clear_old_results()
		if config_obj.options["track_results"]:
			racetrack.start_tracking(config_obj)
		clear_old_results()
		runtests.runtests(
			args,
			config_obj
		)
	except Exception as e:
		print(e)
		import traceback
		traceback.print_exc()
	finally:
		if config_obj.options["track_results"]:
			racetrack.stop_tracking(config_obj)
		print('--------------------------------------------------------------')
		for desc, cmd in cleanups:
			# Run cleanups, displaying but not propagating exceptions
			try:
				print(desc)
				cmd()
			except Exception:
				print((traceback.format_exc()))

if __name__ == '__main__':
	main()
