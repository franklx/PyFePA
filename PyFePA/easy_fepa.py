#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyFePA import fepa, serializer

class easy_fepa(object):

    def __init__(self,  id_fattura,
                        azi_piva, azi_ragsoc, azi_indirizzo, azi_cap, azi_citta, azi_prov, azi_naz,
                        cli_cod, cli_pec,
                        cli_piva, cli_cfis, cli_ragsoc, cli_indirizzo, cli_cap, cli_citta, cli_prov, cli_naz,

                        doc_data, doc_numero, doc_totale,

                        doc_bollo = None,
                        is_nc = False,
                        is_pa = False,

                        rif_amm = None):

        self.__nbr = 0
        self.__npr = 0
        self.__nfr = 0
        self.__nar = 0
        self.__fname = '%s%s_%05i.xml' % (azi_naz, azi_piva, id_fattura)

        self.__f = fepa.FatturaElettronica(
            FatturaElettronicaHeader = fepa.FatturaElettronicaHeader(
                DatiTrasmissione = fepa.DatiTrasmissione(
                    IdTrasmittente = fepa.IdTrasmittente(
                        IdPaese = azi_naz,
                        IdCodice = azi_piva,
                    ),
                    ProgressivoInvio = id_fattura,
                    FormatoTrasmissione = is_pa and 'FPA12' or 'FPR12',
                    CodiceDestinatario = cli_cod or '0000000',
                    PECDestinatario = cli_pec,

                ),
                CedentePrestatore = fepa.CedentePrestatore(
                    DatiAnagrafici = fepa.DatiAnagraficiCP(
                        IdFiscaleIVA = fepa.IdFiscaleIVA(
                        IdPaese = azi_naz,
                        IdCodice = azi_piva,
                        ),
                        Anagrafica = fepa.Anagrafica(
                            Denominazione = azi_ragsoc,
                        ),
                        RegimeFiscale = 'RF01',
                        CodiceFiscale = azi_piva,
                        RiferimentoAmministrazione = rif_amm,
                    ),
                    Sede = fepa.Sede(
                        Indirizzo = azi_indirizzo,
                        CAP = azi_cap,
                        Comune = azi_citta,
                        Provincia = azi_prov,
                        Nazione = azi_naz,
                    ),
                ),
                CessionarioCommittente = fepa.CessionarioCommittente(
                    DatiAnagrafici = fepa.DatiAnagraficiCC(
                        Anagrafica = fepa.Anagrafica(
                            Denominazione = cli_ragsoc,
                        ),
                    ),
                    Sede = fepa.Sede(
                        Indirizzo = cli_indirizzo,
                        CAP = cli_cap,
                        Comune = cli_citta,
                        Provincia = cli_prov,
                        Nazione = cli_naz,
                    ),
                ),
            ),
            FatturaElettronicaBody = [
                fepa.FatturaElettronicaBody(
                    DatiGenerali = fepa.DatiGenerali(
                        DatiGeneraliDocumento = fepa.DatiGeneraliDocumento(
                            TipoDocumento = is_nc and 'TD04' or 'TD01',
                            Divisa = 'EUR',
                            Data = doc_data,
                            Numero = doc_numero,
                            ImportoTotaleDocumento = doc_totale,
                            #ScontoMaggiorazione
                        ),
                    ),
                    DatiBeniServizi = fepa.DatiBeniServizi(),
                    DatiPagamento = fepa.DatiPagamento(CondizioniPagamento = 'TP02'),
                )
            ],
        )

        if cli_piva:
            self.__f.FatturaElettronicaHeader.CessionarioCommittente.DatiAnagrafici.IdFiscaleIVA = fepa.IdFiscaleIVA(
                IdPaese = cli_naz,
                IdCodice = cli_piva,
            )
        else:
            self.__f.FatturaElettronicaHeader.CessionarioCommittente.DatiAnagrafici.CodiceFiscale = cli_cfis

        if doc_bollo:
            self.__f.FatturaElettronicaBody[0].DatiGenerali.DatiGeneraliDocumento.DatiBollo = fepa.DatiBollo(
                BolloVirtuale = 'SI',
                ImportoBollo = doc_bollo
            )
    @property
    def filename(self):
        return self.__fname

    @property
    def sepa(self):
        return self.__f

    @property
    def xml(self):
        return serializer.serializer(self.__f, 'xml')

    def append_body(self, art_cod, art_dsc, qta, um, prz_unit, iva_alq, iva_natura=None, prz_tot=None):
        self.__nbr += 1
        if not prz_tot:
            prz_tot = (prz_unit or 0) * (qta or 0)
        _rw = fepa.DettaglioLinee(
                    NumeroLinea = self.__nbr,
                    Descrizione = art_dsc,
                    Quantita = qta,
                    UnitaMisura = um,
                    PrezzoUnitario = prz_unit or 0,
                    AliquotaIVA = iva_alq,
                    PrezzoTotale = prz_tot,
                    Natura = iva_natura,
                    #ScontoMaggiorazione
                )
        if art_cod:
            _rw.CodiceArticolo = fepa.CodiceArticolo(CodiceTipo='', CodiceValore = art_cod)

        if self.__nbr == 1:
            self.__f.FatturaElettronicaBody[0].DatiBeniServizi.DettaglioLinee = [_rw]
        else:
            self.__f.FatturaElettronicaBody[0].DatiBeniServizi.DettaglioLinee.append(_rw)

    def append_foot(self, iva_alq, imponibile, imposta, iva_natura=None, iva_norma=None, arrot=0, iva_esig=None):
        self.__nfr += 1
        _rw = fepa.DatiRiepilogo(
                    AliquotaIVA = iva_alq,
                    ImponibileImporto = imponibile,
                    Imposta = imposta,
                    Arrotondamento = arrot,
                    EsigibilitaIVA = iva_esig,
                    Natura = iva_natura,
                    RiferimentoNormativo = iva_norma,
                )

        if self.__nfr == 1:
            self.__f.FatturaElettronicaBody[0].DatiBeniServizi.DatiRiepilogo = [_rw]
        else:
            self.__f.FatturaElettronicaBody[0].DatiBeniServizi.DatiRiepilogo.append(_rw)

    def append_pay(self, pag_cod, importo, iban=None, dt_scad=None, abi=None, cab=None, dsc_banca=None, bic=None, is_anti=None):
        self.__npr += 1
        if self.__npr > 1:
            self.__f.FatturaElettronicaBody[0].DatiPagamento.CondizioniPagamento = is_anti and 'TP01'
        else:
            self.__f.FatturaElettronicaBody[0].DatiPagamento.CondizioniPagamento = is_anti and 'TP03' or 'TP02'

        _rw =  fepa.DettaglioPagamento(
                        ModalitaPagamento = pag_cod, # MP01..12
                        ImportoPagamento = importo,
                        DataScadenzaPagamento = dt_scad,
                        IBAN = iban,
                        IstitutoFinanziario = dsc_banca,
                        ABI = abi,
                        CAB = cab,
                        BIC = bic,
                    )

        if self.__npr == 1:
            self.__f.FatturaElettronicaBody[0].DatiPagamento.DettaglioPagamento = [_rw]
        else:
            self.__f.FatturaElettronicaBody[0].DatiPagamento.DettaglioPagamento.append(_rw)

    def append_attach(self, nome, attachment, algoritmo=None, formato=None, descrizione=None):
        self.__nar += 1
        _rw =  fepa.Allegati(
                        NomeAttachment = nome,
                        AlgoritmoCompressione = algoritmo,
                        FormatoAttachment = formato,
                        DescrizioneAttachment = descrizione,
                        Attachment = attachment,
                    )

        if self.__nar == 1:
            self.__f.FatturaElettronicaBody[0].Allegati = [_rw]
        else:
            self.__f.FatturaElettronicaBody[0].Allegati.append(_rw)

#  vim: set ts=8 sts=4 sw=4 et sta :
