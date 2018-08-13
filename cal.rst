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

    specified feed-rss will be checked and current event created only when new
    items there are detected.

  .. TODO: implement url/feed checks
  .. TODO: note on options with parameters for such event and feed checks.

- Hello Internet

  :ts-start: Tue Jan 2 2018
  :ts: every 3w interval
  :url: http://www.hellointernet.fm/
  :feed-rss: http://www.hellointernet.fm/podcast?format=rss

  Note:

    time interval specification with "ts-start" for a zero point.
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
