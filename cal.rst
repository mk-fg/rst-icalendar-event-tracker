Common Configuration
--------------------

This section can appear anywhere (maybe multiple times),
options in which apply to the whole file,
and is detected by having ``:config: 1`` value defined somewhere in it.

:config: 1

Feed options (e.g. ``:feed-rss:``):

  :feed-interval-checks: 5

  Make three *additional* checks within specified interval (if any),
  spaced exponentially from the end of it, when last check is made.

  For example, with 3 extra checks within 10-day interval,
  checks will be made after following number of days: 3, 7.7, 9.4, 10.

  This should always be set unless --time-start in the past is used,
  as otherwise there will never be past events eligible for feed checks.

  Default: 5

  :feed-check-before-fixed-ts: 1d

  Specifies when to do additional checks for fixed-time events.
  Same format as ``:duration:``. Only one successful check is performed for these.

  ``:feed-interval-checks:`` will be performed in this interval,
  using exponential backoff algo for spacing, in reverse to how they're
  spaced within interval between events.

  Same as with ``:feed-interval-checks:``, should be set unless --time-start is
  in the past, as otherwise these checks will always be missed, due to either
  event falling outside of processed time interval or check still in the future.

  Default: 1d

  :feed-check-after-fixed-ts: 1d

  | Same as ``:feed-check-before-fixed-ts:``, but for extra checks after event.
  | Only used if --time-start is set in the past.

  Default: 1d


Approaching-time notification options:

  These are notifications issued when ``:note-ts:`` tag is used for event,
  e.g. ``:note-ts: dnote`` to issue desktop notification (if these are enabled)
  at exact time of the event.

  Same as with other things, these only get issued for events that are filtered
  for display, i.e. not stuff too far in the past or future.

  :note-ts-window: 1h

  | When event is in the future, will issue notification up to specified window before event.
  | This should probably be set to be slightly more than interval between script runs, if any.

  Default: 1h

  :note-ts-window-past: 3d

  Same as ``:ts-note-window:`` above, but looking into past, and for events
  where intiial time was missed. I.e. with 3d - alert for events missed in the
  last 3 days, if script was never run at the time.

  Default: 3d


Desktop notification options:

  :dnote-enabled: true
  :dnote-icon: nwn
  :dnote-timeout: 0
  :dnote-app: riet
  :dnote-urgency: 2

  | Options for desktop notifications, as per D-Bus protocol spec.
  | Use ``:dnote-enabled: false`` to disable them entirely.
  | Default-enabled, options are protocol/daemon defaults.




One-off event reminders
-----------------------

Kept in the head of the doc, as stuff is added and removed here all the time.

- Make this rst-calendar parser thing

  :ts: 2018-07-20
  :url: https://github.com/mk-fg/rst-icalendar-event-tracker

  Notes on date/time format - anything that gets parsed by "date -d"
  (actually used as a fallback) will work.

  Example above shows iso8601 date, but pretty much any format should do,
  including standard dates/times around the world, weekdays, random human stuff
  like "next Mon", "now + 3 hours 30 minutes", "5pm July 29 PDT", etc.

  ``:ts:`` key in particular also accepts special "every ..." spec for recurring
  events, which is structured as follows::

    EVERY:
      "every" {
        [ ( NN[suffix][ "-" MM[suffix]] )+ | DELTA-DATE-SPEC ]
          [WD[-WD]]+
          ["at"] [TIME ["[" TZ "]"]]
        | DELTA-SPEC "interval" }
      suffix: st, nd, rd, th
      example: every 1st-11th at 5am UTC
    DELTA-SPEC:
      ( N || unit )+
      units:
        y, yr, year, mo, month, w, week, d, day,
        h, hr, hour, m, min, minute, s, sec, second
      example: 3mo 1d 5hrs 10minutes 30s
    DELTA-DATE-SPEC:
      subset of DELTA-SPEC wrt allowed units
      units: y, yr, year, mo, month, w, week, d, day
    WD:
      monday mon, tuesday tu tue tues, wednesday wed,
      thursday th thu thur thurs, friday fri, saturday sat, sunday sun
    TZ:
      ( "UTC" | ("+"|"-") HH:MM | region/place | abbrev )
      examples: +05:00, America/Los_Angeles, BST
        (anything that pytz can parse, basically)
    TIME:
      ( [H]H[:MM[:SS]] ["am"|"pm"] | "noon" | "midnight" )

  Gist is that something like "every Friday 13th at 9pm [US/Eastern]",
  "every Mon-Fri 19:45" or "every 12d interval" will just do what it says,
  starting any non-specific intervals at either ``:ts-start:`` or first time
  that event/spec was encountered for that rst (tracked in -d/--state-file).

  See more examples for all these below.

- Multiple appointments for same thing

  :ts: Tue 2018-08-14 19:15
  :ts: Thu 2018-08-16 13:00
  :ts: Sat 2018-08-18 15:30



Simple recurring events
-----------------------

Stuff that happens every day/week/month/year.

- Same Date Every Year

  :ts: July 28

  Note:

    date will be parsed on each run, as "date -d 'July 28'" in this case,
    so it will get triggered every year, even when specified as a one-off
    date (without "every" prefix) due to how "date" parser works.

- Same Time Every Day

  :ts: 10am

  | Note: parsed as "first 10am in the future".

- Weekend Days

  :ts: every sat-sun
  :conky: c_title=green

  | Note: "every <weekday>-<weekday>" spec, adding recurring event interval.
  | Note: ``:conky:`` key allows to override any -o/--conky-params per-item.

- New Year Bank Holidays

  :ts-start: Jan 1
  :ts-end: Jan 10
  :conky: c_title=green

  | Note: ts start/end interval spec for event instead of one fixed time.
  | Note: start/end times can only be one-off, not "every X".

- Workdays during New Year Bank Holidays

  :ts-start: Jan 1
  :ts-end: Jan 10
  :ts: every mon-fri
  :conky: c_title=gray

  | Note: same as above, but only matches mon-fri weekdays within that interval.

- Midnight on every Friday the 13th

  :ts: every 13th fri at midnight
  :conky: c_title=red c_date=red c_time=red c_weekday=red



Media and Distractions
----------------------

Media diet, mostly consisting of periodicals like video (tv, anime, etc) series,
scheduled twitch streams, audio podcasts, blogs (text series) and such.


Streams
```````

- Co-Optional podcast

  :ts: every tue at 12pm [America/Los_Angeles]
  :duration: 3h
  :url: https://twitch.tv/totalbiscuit/

  Note: "every" spec with timezone of a specific place.

    Raw timezone can be used in time spec (e.g. "12pm PDT"), but it might not
    flip correctly when daylight savings periods start/end, so e.g. BST (+1) won't
    turn into GMT (+0) when explicitly specified and vice-versa, while specifying
    [Europe/London] (see /usr/share/zoneinfo) will always account for such changes.

  Note: ``:duration:`` + ``:ts:`` spec instead of start/end.


Podcasts
````````

- Econtalk

  :ts: every Mon
  :url: http://www.econtalk.org/

  Note: simple "every <weekday>" spec.

- Bad Voltage

  :ts: every 2w interval
  :url: http://www.badvoltage.org/
  :feed-rss: http://www.badvoltage.org/feed/ogg/

  Note:

    Specified feed-rss will be checked only if event falls within output
    timespan. See also ``:feed-interval-checks:`` option.

  .. TODO: implement url/feed checks
  .. TODO: note on options with parameters for such event and feed checks.

- Hello Internet

  :ts-start: Tue Jan 2 2018 [US/Eastern]
  :ts: every 3w interval
  :url: http://www.hellointernet.fm/
  :feed-rss: http://www.hellointernet.fm/podcast?format=rss

  Note: timezone specified as "[zoneinfo]" in "ts-start" for reliable DST flipping.

  Note:

    Time interval specification with "ts-start" for a zero point.
    In this example, event will be added to every third Tue since ts-start date.
    ("Tue" because "Jan 2 2018" is a tue, "third" due to 3w spec)



Feedback on Projects
--------------------

Checks for various places where proper notification are either not implemented
or too annoying to use.

- Factorio mods

  :ts: every 2w interval
  :url: https://mods.factorio.com/mod/Will-o-the-Wisps_updated/discussion
  :url: https://mods.factorio.com/mod/Vehicle_Cruise_Control/discussion
  :url: https://mods.factorio.com/mod/Burner_Drill_4x4_Area/discussion

  Note: multiple URLs to check.

  .. TODO: info on url-checking parameters.

- Stellaris mods

  :ts: every 1mo interval
  :url: https://steamcommunity.com/app/281990/workshop/



Releases
--------

- Release of Some Interesting Thing

  :ts: 2018-11-20
  :feed-rss: http://some-thing.org/rss
  :feed-check-for: 10d

  Note:

    With a one-off (not "every X") timestamp, ``:feed-rss:`` is not used,
    unless ``:feed-check-for:`` interval (same as ``:duration:``) is specified
    for it or in the common config section, during/after which checks will be made.

- Some Important Event

  :ts: 2018-11-30 12:00
  :note-ts: dnote
  :dnote-icon: alarm

  Note: desktop notification will be issued at the time, with specified
  before/after time-window parameters (see above) and notification parameters.

- Important Recurring Event

  :ts: every 19th-21st
  :ts: every 23rd
  :note-ts: dnote
  :note-ts-interval: 7d

  Note:

    ``:note-ts-interval:`` will make sure that only one notification is issued
    for the whole timespan, even if it's discontinuous like that (4 separate days).

    Default interval is 0 - i.e. separate notification will be issued for evey
    ``:ts:`` or timespan.
