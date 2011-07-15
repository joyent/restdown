# restdown Changelog

## restdown 1.2.10 (not yet released)

- Fix bug in "-d|--define".

## restdown 1.2.9

- Add "-d|--define" option for providing metadata on the command line.


## restdown 1.2.8

- ["ohthejoy" brand] Fix issue with "current section" highlighting in the TOC:
  for the h1's the whole section would be highlighted instead of just the h1
  link.


## restdown 1.2.7

- Fix a bug handling an empty "apisections" metadatum.


## restdown 1.2.6

- [issue #2, "ohthejoy" brand] Add support for method h2's being in other of
  the following formats:

    1. "NAME (VERB PATH)", e.g. "ListMachines (GET /:login/machines)".
       Only NAME is shown in table of contents and used for the section anchor.
       Reasonable styling in content. Only "VERB PATH" is used in ".json" API
       summary file.
    2. "VERB PATH", e.g. "DELETE /zones/:uuid"
    3. "NAME", e.g. "DoIt"

  Note: It is possible the markup changes here break other brands.

- Add 'apisections' document metadatum. It is a comma-separated list of h1 section
  names that are to be considered the API endpoint sections (i.e. an h1 section
  in which h1's define REST API endpoints). If 'apisections' is not specified
  it is presumed that all sections except the first (presumed to be a preface
  section) are API sections. This is related to issue #2, but not a complete
  fix yet.
- Add support for 'mediaroot' document metadatum to control the URL from which
  brand media is pulled.


## restdown 1.2.5

- ["ohthejoy" brand] Switch to background gradient for current TOC item instead
  of arrow: easier to see than the arrow for larger APIs.
- ["ohthejoy" brand] Don't let TOC labels wrap (helpful for longer TOC titles)
- ["ohthejoy" brand] Give the TOC arrow header some scrolling slack.


## restdown 1.2.4

- Fix TOC handling to skip h2's in the intro section.


## restdown 1.2.3

- ["ohthejoy" brand] Fix print styling of pre.shell blocks.
- ["ohthejoy" brand] Reasonable default table styles.


## restdown 1.2.2

- New default "ohthejoy" brand. Improvements: 
    - Header styling for better section separation.
    - Fix TOC arrow to point all toc elements (also not be dependent on "VERB
      URLPATH" header text form).
    - Remove the fixed top-right section header: not that helpful, often
      broken. 
- Strip trailing whitespace in create api JSON file.


## restdown 1.2.1

- [issue #1] Allow h2 text (for endpoints) to NOT be the "VERB URLPATH" format.


## restdown 1.2.0

- Add "-b|--brand-dir DIR" option for specifying a local brand dir to use.


## restdown 1.1.0

(Started this changelog on 5 May 2011.)
