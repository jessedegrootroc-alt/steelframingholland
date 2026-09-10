# -*- coding: utf-8 -*-
"""Bouwt de hele site opnieuw op uit de content in sfh/ en de copylagen.

    python3 bouw_alles.py

De HTML in de hoofdmap is gegenereerd; pas je daar met de hand iets aan, dan is
dat weg zodra dit script draait. Bronteksten wijzig je in _generator/sfh/ (de
contentexport van www.steelframingholland.nl), de formulering in
inhoud_copy.py, en de indeling in de bouwscripts hieronder.

De afbeeldingen worden hier NIET opnieuw omgezet; dat doet maak_assets.py en dat
hoeft alleen als er beeld bijkomt of verandert.
"""
# Eerst minificeren, dan pas de pagina's schrijven. De verwijzingen in de HTML
# krijgen een hash van het bestand dat de browser ophaalt, en die bestanden
# moeten er dus al staan; bouw_home schrijft index.html al bij het
# importeren, vandaar dat dit hierboven staat en niet onderaan.
import minify
minify.main()

import bouw_home
import bouw_dienst
import bouw_projecten
import bouw_bedrijf
import bouw_contact
import bouw_sitemap

bouw_dienst.main()
bouw_projecten.main()
bouw_bedrijf.main()
bouw_contact.main()
bouw_sitemap.main()
print('klaar')
