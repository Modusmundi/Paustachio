# Paustachio!

Paustachio seeks to make querying LDAP datasources, and deriving useful information from them, a little bit easier.  The goals (For now) are straight forward:

1. Query a given LDAP datasource.
2. Return a count as well as the timestamp for when that search was completed.
3. Report this information to a CSV for easy reading, consumption by other tools, etc.

## Dependencies

Paustachio is written in Python and relies on the following libraries:

  * ldap3
  * json
  * csv
  * pathlib
  * time

All of which can be obtained from your friendly neighborhood pip install command, all of which being on PyPI or similar.

## Future

This is a re-write of an older project to force myself to learn more about PyTest and TDD in general.
It's still an **extremely rough** and initial release just to get some code up.

That said, here's a small list of TODOs that I want to work on.

  * Implement the capability to use TLS
  * Try to implement statisical analysis for the data against old data (This is probably too much given what little playing I have done)
  * Try to streamline the code a bit more (Always!)
  * Potential command-line options (At-runtime based file selection for config/search/output, etc.)
  * Make the code fail gracefully- Offer retries on connection failure, and so on.
  * ...  Maybe, just maybe, make it pretty and give it a GUI?