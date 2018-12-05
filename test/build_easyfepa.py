#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys; sys.path.append('..')

from datetime import date, datetime
from PyFePA.easy_fepa import easy_fepa

ft = easy_fepa(1, '04200640870', 'azienda srl', 'via azienda, 1', '00000', 'Citta Azienda', 'PV', 'IT',
                0, 'cliente@pec.it', '12345678901', None, 'cliente spa',  'via del cliente, 1', '12345', 'Citta Cliente', 'PC', 'IT',
                date.today(), '666/P', 246.00,
                doc_bollo=2.00)
ft.append_body('CODART', 'Descrizione articolo', 2, 'NR', 100.00, 22.00)
ft.append_body('CODESE', 'Descrizione articolo esente', 1, 'NR', 50.00, 0.00, 'N4')
ft.append_foot(22.00, 200.00, 44.00)
ft.append_foot(0.00, 50.00, 0.00, iva_natura='N4', iva_norma='ex art.10')
ft.append_pay('MP05', 146.00, 'IT91M0311153480000000004042', dt_scad=date.today(), dsc_banca='UBI Banca SpA', abi='03111', cab='53480')
ft.append_pay('MP05', 100.00, 'IT91M0311153480000000004042', dt_scad=date(2019,1,1), dsc_banca='UBI Banca SpA', abi='03111', cab='53480')

#from PyFePA import fepa
#w = fepa.DatiTrasporto(DataOraConsegna='2018-12-04T00')

with open(ft.filename, 'w') as fo:
    fo.write( ft.xml )

#  vim: set ts=8 sts=4 sw=4 et sta :
