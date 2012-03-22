# restdown Changelog

## restdown 1.2.18

- [issue #11] "ohthejoy" brand: Avoid hang in jquery using '|=' selector on TOC
  elements which might have a single-quote. See
  <http://bugs.jquery.com/ticket/11505>.


## restdown 1.2.17

- [issue #10] "spartan" brand: Fix the TOC dropdown closing right away
  in Firefox.


## restdown 1.2.16

- Move to 'cutarelease.py' separate tool
- [issue #9] Fix breakage if there are no TOC sections, i.e. no second h1 in
  the input restdown content.


## restdown 1.2.15

- "spartan" brand: Fix path to jquery if using a "mediaroot" config value
  other than the defualt "/media".


## restdown 1.2.14

- [issue #4] "ohthejoy" brand: Text in tables should align to the top of the cells.
  Also some table top/bottom margins.
- [issue #3] "ohthejoy" brand: Bullets in lists should hang.


## restdown 1.2.13

- [issue #6] "spartan" brand: 
    - Blue default logo color, instead of pink.
    - TOC margin fix for narrow screens.
    - Support for "logo-color", "logo-font-family" and "header-font-family"
      metadata (see README.md for description).
    - Slightly wider (650px -> 700px).
    - Restore "pre.shell" styling from "ohthejoy" brand.


## restdown 1.2.12

- New "spartan" brand.
- If `%(toc_html)s` appears in the "header.html.in" or "footer.html.in" files,
  then the `<div id="sidebar">%(toc_html)s</div>` is excluded. This allows
  one to customize where the TOC html appears.
  Note: an metadata option should be added to more explicitly control this.


## restdown 1.2.11

- Add the "markdown2extras" metadata var to enable turning on markdown2
  extra syntax for the processed document. See
  <https://github.com/trentm/python-markdown2/wiki/Extras>.
- Upgrade to python-markdown2 1.0.1.19.
- Use `realpath` as appropriate so can run `restdown` as a symlink.

## restdown 1.2.10

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
