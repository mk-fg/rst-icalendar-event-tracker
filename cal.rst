One-off event reminders
-----------------------

Kept in the head of the doc, as stuff is added and removed here all the time.

- Make this rst-calendar parser thing

  :ts: 2018-07-20
  :url: https://github.com/mk-fg/rst-icalendar-event-tracker

  .. TODO: note on how dates/times are parsed, examples



AFK life event reminders
------------------------

- Same Date Every Year

  :ts: July 28

  .. Note: date will be parsed on each run, as "date -d 'July 28'" in this
     case, so it will get triggered every year, even when specified as a one-off
     date (without "every" prefix) due to how "date" parser works.

- Same Time Every Day

  :ts: 10am

  .. Note: parsed as "first 10am in the future".

- Weekend Days

  :ts: every sat-sun

  .. Note: "every <weekday>-<weekday>" spec, adding recurring event interval.

- New Year Bank Holidays

  :ts-start: Jan 1
  :ts-end: Jan 10

  .. Note: ts start/end interval spec for event instead of one fixed time.
  .. Note: start/end times can only be one-off, not "every X".



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

  .. Note: "every" spec with timezone of a specific place.

     Raw timezone can be used in time spec (e.g. "12pm PDT"), but it won't
     auto-change when daylight savings periods start/end, so e.g. BST (+1) won't
     turn into GMT (+0) when explicitly specified and vice-versa, but specifying
     [London] will account for such changes.

  .. Note: duration + ts spec instead of start/end.


Podcasts
````````

- Econtalk

  :ts: every Mon
  :url: http://www.econtalk.org/

  .. Note: simple "every <weekday>" spec.

- Bad Voltage

  :ts: every 2w interval
  :url: http://www.badvoltage.org/
  :feed-rss: http://www.badvoltage.org/feed/ogg/

  .. Note: specified feed-rss will be checked and current event created only
     when new items there are detected.

     TODO: note on options with parameters for such event and feed checks.

- Hello Internet

  :ts-start: Jan 2 2018
  :ts: every 3w interval
  :url: http://www.hellointernet.fm/
  :feed-rss: http://www.hellointernet.fm/podcast?format=rss

  .. Note: time interval specification with "ts-start" for a zero point.
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

  .. Note: multiple URLs to check.

     TODO: info on url-checking parameters.

- Stellaris mods

  :ts: every 1mo interval
  :url: https://steamcommunity.com/app/281990/workshop/
