#!/usr/bin/env python3

import itertools as it, operator as op, functools as ft
import os, sys, csv, contextlib, tempfile, zipfile, random
import collections as cs, pathlib as pl


# Disambiguations picked in a hurry
tza_picks = '''
	ACDT Australia/Adelaide
	ACST Australia/Adelaide
	AEDT Australia/Sydney
	AEST Australia/Sydney
	AHST America/Anchorage
	AKDT America/Anchorage
	AKST America/Anchorage
	AMT Europe/Amsterdam
	BST Europe/London
	CDT America/Chicago
	CEST Europe/Berlin
	CET Europe/Berlin
	CET Europe/Berlin
	CMT America/Argentina/Buenos_Aires
	CPT America/Chicago
	CST America/Chicago
	CWT America/Chicago
	EDT America/New_York
	EEST Europe/Sofia
	EET Europe/Sofia
	EPT America/New_York
	EST America/New_York
	EWT America/New_York
	GMT Europe/London
	HDT Pacific/Honolulu
	HST Pacific/Honolulu
	HMT Europe/Helsinki
	IDT Asia/Jerusalem
	IST Asia/Jerusalem
	IMT Europe/Istanbul
	JST Asia/Tokyo
	KMT Europe/Kiev
	KST Asia/Seoul
	MDT America/Phoenix
	MMT Europe/Moscow
	MSD Europe/Moscow
	MSK Europe/Moscow
	MST America/Phoenix
	NZDT Pacific/Auckland
	NZMT Pacific/Auckland
	NZST Pacific/Auckland
	PDT America/Los_Angeles
	PPT America/Los_Angeles
	PST America/Los_Angeles
	PWT America/Los_Angeles
	RMT Europe/Rome
	SAST Africa/Johannesburg
	SST Pacific/Midway
	TMT Asia/Tehran
	WAT Africa/Lagos
	WEMT Europe/Paris
	WEST Europe/Paris
	WET Europe/Paris
	WMT Europe/Warsaw
	YST America/Anchorage'''


def main(args=None):
	import argparse
	parser = argparse.ArgumentParser(
		description='Extract timezone abbreviation translation map from'
			' zipped csv files of https://timezonedb.com/download archive.')
	parser.add_argument('file', help='zip archive from https://timezonedb.com/download.')
	parser.add_argument('-a', '--all', action='store_true',
		help='Print a list of abbreviations that remain ambiguous.')
	opts = parser.parse_args(sys.argv[1:] if args is None else args)

	tza_dict = cs.defaultdict(set)

	with contextlib.ExitStack() as ctx:
		tmp_dir = pl.Path(ctx.enter_context(
			tempfile.TemporaryDirectory(prefix='tz-db.') ))
		with zipfile.ZipFile(opts.file) as src: src.extractall(tmp_dir)

		src_tza, src_zones = (
			ctx.enter_context((tmp_dir / k).open(encoding='utf-8-sig'))
			for k in ['timezone.csv', 'zone.csv'] )

		zone_names = dict()
		for row in csv.reader(src_zones):
			zone_id, cc, name = row[:3]
			zone_names[int(zone_id)] = name

		for row in csv.reader(src_tza):
			zone_id, tza = row[:2]
			if tza[0] in '+-': continue
			zone = zone_names.get(int(zone_id))
			if not zone:
				print(f'[{tza}] zone_id with no name: {zone_id}')
				continue
			tza_dict[tza].add(zone)

	tza_picks_map = dict(line.split() for line in tza_picks.splitlines() if line)
	tza_dict, tza_list = dict(), sorted(tza_dict.items(), key=op.itemgetter(0))

	for tza, zones in tza_list:
		if len(zones) > 1:
			if tza in tza_picks_map: zones = {tza_picks_map[tza]}
			else:
				if opts.all:
					print(f'Options for {tza}:')
					for zone in sorted(zones): print(f'  {zone}')
				continue
		tza_dict[tza], = zones

	line_len = 80
	tza_list = sorted((f'{k}={v}' for k,v in tza_dict.items()), key=len)
	while tza_list:
		line = ''
		while tza_list:
			random.shuffle(tza_list)
			for s in tza_list:
				if line_len - len(line) > len(s) + 1:
					line = f'{line} {s}'.strip()
					tza_list.remove(s)
					break
			else:
				print(line)
				break
	if line: print(line)

if __name__ == '__main__': sys.exit(main())
