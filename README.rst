somenergia-dataexports
======================

Several scripts to retrieve information from OpenERP data.

``distribucio_de_socies.py``
----------------------------

Generates a csv file (tab separated) counting members for each
municipality.

Usage:

::

    $ distribucio_de_socies.py [<iso-date>]  >  <output.csv>

Example:

::

    $ distribucio_de_socies.py 2015-02-01 > DistribucioSocies-2015-02.csv

TODO's
~~~~~~

-  Historical unaccuracies

   -  deactivated members are not counted when they were still members
   -  Members who started as owner or payer, are counted as member since
      then

``mapa_socies.py``
------------------

Generates svg maps of the distribution of the members.

``mchimp-generationsocis.py``
-----------------------------

Generates csv to feed mailchimp mailings from OpenErp data
