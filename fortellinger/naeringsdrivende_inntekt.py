from typing import Union

import numpy as np
from rich.markdown import Markdown

from grafer_og_visninger.pie_chart import side_ved_side_pie_chart, enkel_pie_chart
from queries.naeringsdrivende_inntekt import naeringsdrivende_inntekt_foer_etter_endring, InntektsSporsmal, \
    naeringsdrivende_inntekt_i_2024


def hent_svarantall_for_sporsmal_tag_i_perioder(sporsmal_tag, data, perioder):
    """Hent svarantall for et spørsmål med gitte perioder."""
    if not perioder:
        return data
    return {periode: data[periode].get(sporsmal_tag, 0) for periode in perioder}


def filtrer_dataframe_etter_periode(df, periode):
    """Filtrer DataFrame for en spesifikk periode."""
    return df[df['period'] == periode]


def beregn_summer_for_sporsmal_tags(periode_df, sporsmal_tags):
    """Beregn summen av tellinger for hver sporsmal_tag i den gitte periode-DataFrame."""
    return {tag: periode_df[periode_df['sporsmal_tag'] == tag]['count'].sum() for tag in sporsmal_tags}


def summer_data_per_periode(df, perioder, sporsmal_tags) -> dict:
    """
    Summerer data etter gitte perioder og spørsmålstags.

    Args:
        df (pd.DataFrame): DataFrame som inneholder dataene.
        perioder (list): En liste over perioder for å filtrere DataFrame etter.
        sporsmal_tags (set): Et sett spørsmålstags for å filtrere DataFrame etter.

    Returns:
        dict: En ordbok der hver nøkkel er en periode, og verdien er en annen ordbok
              som inneholder summen av tellinger for hver spørsmålstag. Hvis 'perioder'
              er tom, returneres en ordbok som inneholder summen av tellinger for hver
              spørsmålstag over hele DataFrame-en.
    """
    if not perioder:
        return beregn_summer_for_sporsmal_tags(df, sporsmal_tags)

    summerte_data = {}

    for periode in perioder:
        periode_df = filtrer_dataframe_etter_periode(df, periode)
        summer = beregn_summer_for_sporsmal_tags(periode_df, sporsmal_tags)
        summerte_data[periode] = summer

    return summerte_data


def finn_antall_svar_for_tags_med_periode(bigquery_client, ingen_perioder=False):
    """Finn antall svar for tags med eller uten perioder."""
    # Inntektsmelding næringsdrivende
    naeringsdrivende_inntekt_query = naeringsdrivende_inntekt_foer_etter_endring() if not ingen_perioder else naeringsdrivende_inntekt_i_2024()
    df = bigquery_client.query(naeringsdrivende_inntekt_query).to_dataframe()

    df['sporsmal_tag'] = np.where(df['verdi'].isin(['JA', 'NEI']), df['sporsmal_tag'] + '_' + df['verdi'], df['sporsmal_tag'])
    modifiserte_tags = set(df['sporsmal_tag'])

    perioder = ['foer', 'etter'] if not ingen_perioder else []
    summert_data = summer_data_per_periode(df, perioder, modifiserte_tags)

    if ingen_perioder:
        return summert_data

    # Legger antall svar for hvert spørsmål sortert på perioder
    return {sporsmal_tag: hent_svarantall_for_sporsmal_tag_i_perioder(sporsmal_tag, summert_data, perioder) for sporsmal_tag in modifiserte_tags}


def fortelling_om_inntektssporsmal(antall_svar_for_sporsmal_i_periode, periode: Union['foer', 'etter']) -> Markdown:
    fortelling_inntektsopplysninger = """
**Drift i virksomheten:**
- **Ja:** {ja_drift} var antallet næringsdrivende som hadde drift i virksomheten frem til sykmelding.
- **Nei:** {nei_drift} hadde ikke drift i virksomheten.

**Ny i arbeidslivet:**
- **Ja:** {ja_ny} var antallet som svarte at de var ny i arbeidslivet.
- **Nei:** {nei_ny} svarte at de ikke var nye i arbeidslivet.

**Varig endring i inntekten:**
- **Ja:** {ja_varig_endring} var totalt antall som svarte ja på en varig endring i inntekten. 
- **Nei:** {nei_varig_endring} svarte nei.
- **Nedleggelse av virksomheten:** {nedleggelse} var antallet som svarte at de hadde lagt ned virksomheten.
- **Endret innsats:** {endret_innsats} svarte at de endret innsats i virksomheten.
- **Omlagt virksomheten:** {omlagt} svarte at de hadde omlagt virksomheten.
- **Endret markedssituasjon:** {endret_marked} svarte at det var endringer i markedssituasjonen.
- **Andre grunner:** {andre_grunner} svarte at det var andre grunner for endring.
- **Endring på minst 25%:** {ja_endring_25_prosent} næringsdrivende rapporterte en endring på minst 25% i sin virksomhet.
- **Ikke endring:** {nei_endring_25_prosent} svarte at de ikke hadde endring.
"""

    fortelling_med_data = fortelling_inntektsopplysninger.format(
        ja_drift=str(antall_svar_for_sporsmal_i_periode['INNTEKTSOPPLYSNINGER_DRIFT_VIRKSOMHETEN_JA'][periode]),
        nei_drift=str(antall_svar_for_sporsmal_i_periode['INNTEKTSOPPLYSNINGER_DRIFT_VIRKSOMHETEN_NEI'][periode]),
        ja_ny=str(antall_svar_for_sporsmal_i_periode['INNTEKTSOPPLYSNINGER_NY_I_ARBEIDSLIVET_JA'][periode]),
        nei_ny=str(antall_svar_for_sporsmal_i_periode['INNTEKTSOPPLYSNINGER_NY_I_ARBEIDSLIVET_NEI'][periode]),
        ja_varig_endring=str(antall_svar_for_sporsmal_i_periode['INNTEKTSOPPLYSNINGER_VARIG_ENDRING_JA'][periode]),
        nei_varig_endring=str(antall_svar_for_sporsmal_i_periode['INNTEKTSOPPLYSNINGER_VARIG_ENDRING_NEI'][periode]),
        nedleggelse=str(
            antall_svar_for_sporsmal_i_periode['INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_OPPRETTELSE_NEDLEGGELSE'][
                periode]),
        endret_innsats=str(
            antall_svar_for_sporsmal_i_periode['INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_ENDRET_INNSATS'][periode]),
        omlagt=str(
            antall_svar_for_sporsmal_i_periode['INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_OMLEGGING_AV_VIRKSOMHETEN'][
                periode]),
        endret_marked=str(
            antall_svar_for_sporsmal_i_periode['INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_ENDRET_MARKEDSSITUASJON'][
                periode]),
        andre_grunner=str(
            antall_svar_for_sporsmal_i_periode['INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_ANNET'][periode]),
        ja_endring_25_prosent=str(
            antall_svar_for_sporsmal_i_periode['INNTEKTSOPPLYSNINGER_VARIG_ENDRING_25_PROSENT_JA'][periode]),
        nei_endring_25_prosent=str(
            antall_svar_for_sporsmal_i_periode['INNTEKTSOPPLYSNINGER_VARIG_ENDRING_25_PROSENT_NEI'][periode])
    )

    return Markdown(fortelling_med_data)


def graf_foer_etter_endring(finn_antall_svar_for_sporsmal_tags_med_periode):
    ja_nei_kategorier = ['Ja', 'Nei']
    side_ved_side_pie_chart(ja_nei_kategorier,
                            [
                                finn_antall_svar_for_sporsmal_tags_med_periode[
                                    InntektsSporsmal.INNTEKTSOPPLYSNINGER_DRIFT_VIRKSOMHETEN_JA.value][
                                    'foer'],
                                finn_antall_svar_for_sporsmal_tags_med_periode[
                                    InntektsSporsmal.INNTEKTSOPPLYSNINGER_DRIFT_VIRKSOMHETEN_NEI.value][
                                    'foer']
                            ],
                            [
                                finn_antall_svar_for_sporsmal_tags_med_periode[
                                    InntektsSporsmal.INNTEKTSOPPLYSNINGER_DRIFT_VIRKSOMHETEN_JA.value][
                                    'etter'],
                                finn_antall_svar_for_sporsmal_tags_med_periode[
                                    InntektsSporsmal.INNTEKTSOPPLYSNINGER_DRIFT_VIRKSOMHETEN_NEI.value][
                                    'etter']
                            ])


def etter_ja_nei_bytte_graf():
    from oppsett.bigquery import init_bigquery_client

    bq_client = init_bigquery_client()

    def naeringsdrivende_inntekt_en_mnd_etter_ja_nei_bytte() -> str:
        bq_tabell = '`flex-prod-af40.flex_dataset.sykepengesoknad_sporsmal_svar_view`'
        question_tags = (
            'INNTEKTSOPPLYSNINGER_VIRKSOMHETEN_AVVIKLET_NEI', 'INNTEKTSOPPLYSNINGER_VIRKSOMHETEN_AVVIKLET_JA')
        query = f"""
            SELECT
                sykepengesoknad_uuid,
                sporsmal_tag,
                verdi,
                sendt,
            FROM
                {bq_tabell}
            WHERE
                sporsmal_tag IN {question_tags}
            AND sendt < TIMESTAMP_ADD(TIMESTAMP '2024-04-29 00:00:00', INTERVAL 30 DAY)
        """

        return query

    query = naeringsdrivende_inntekt_en_mnd_etter_ja_nei_bytte()
    df = bq_client.query(query).to_dataframe()
    sporsmal_tag_counts = df['sporsmal_tag'].value_counts()

    kategorier = sporsmal_tag_counts.index.tolist()
    verdier = sporsmal_tag_counts.values.tolist()

    kategorier_forenklet = [
        'Nei' if v == 'INNTEKTSOPPLYSNINGER_VIRKSOMHETEN_AVVIKLET_NEI' else 'Ja' if v == 'INNTEKTSOPPLYSNINGER_VIRKSOMHETEN_AVVIKLET_JA' else v
        for v in kategorier
    ]

    return enkel_pie_chart(kategorier_forenklet, verdier, 'Etter ja/nei bytte')


def fortelling_i_2024(antall_svar_for_sporsmal_tag_i_2024) -> Markdown:
    fortelling_inntektsopplysninger = """
**Avviklet virksomheten:** (inkluderer svar fra drift i virksomhet spørsmål)
- **Ja:** {ja_avviklet} var antallet næringsdrivende som hadde avviklet og slettet virksomheten.
- **Nei:** {nei_avviklet} hadde ikke avviklet virksomheten.

**Ny i arbeidslivet:**
- **Ja:** {ja_ny} var antallet som svarte at de var ny i arbeidslivet.
- **Nei:** {nei_ny} svarte at de ikke var nye i arbeidslivet.

**Varig endring i inntekten:**
- **Ja:** {ja_varig_endring} var totalt antall som svarte ja på en varig endring i inntekten.
- **Nei:** {nei_varig_endring} svarte nei.
- **Nedleggelse av virksomheten:** {nedleggelse} var antallet som svarte at de hadde lagt ned virksomheten.
- **Endret innsats:** {endret_innsats} svarte at de endret innsats i virksomheten.
- **Omlagt virksomheten:** {omlagt} svarte at de hadde omlagt virksomheten.
- **Endret markedssituasjon:** {endret_marked} svarte at det var endringer i markedssituasjonen.
- **Andre grunner:** {andre_grunner} svarte at det var andre grunner for endring.
- **Endring på minst 25%:** {ja_endring_25_prosent} næringsdrivende rapporterte en endring på minst 25% i sin virksomhet.
- **Ikke endring:** {nei_endring_25_prosent} svarte at de ikke hadde endring.
"""

    fortelling_med_data = fortelling_inntektsopplysninger.format(
        ja_avviklet=str(antall_svar_for_sporsmal_tag_i_2024['INNTEKTSOPPLYSNINGER_VIRKSOMHETEN_AVVIKLET_JA']),
        nei_avviklet=str(antall_svar_for_sporsmal_tag_i_2024['INNTEKTSOPPLYSNINGER_VIRKSOMHETEN_AVVIKLET_NEI']),
        ja_ny=str(antall_svar_for_sporsmal_tag_i_2024['INNTEKTSOPPLYSNINGER_NY_I_ARBEIDSLIVET_JA']),
        nei_ny=str(antall_svar_for_sporsmal_tag_i_2024['INNTEKTSOPPLYSNINGER_NY_I_ARBEIDSLIVET_NEI']),
        ja_varig_endring=str(antall_svar_for_sporsmal_tag_i_2024['INNTEKTSOPPLYSNINGER_VARIG_ENDRING_JA']),
        nei_varig_endring=str(antall_svar_for_sporsmal_tag_i_2024['INNTEKTSOPPLYSNINGER_VARIG_ENDRING_NEI']),
        nedleggelse=str(
            antall_svar_for_sporsmal_tag_i_2024[
                'INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_OPPRETTELSE_NEDLEGGELSE']),
        endret_innsats=str(
            antall_svar_for_sporsmal_tag_i_2024['INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_ENDRET_INNSATS']),
        omlagt=str(antall_svar_for_sporsmal_tag_i_2024[
                       'INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_OMLEGGING_AV_VIRKSOMHETEN']),
        endret_marked=str(
            antall_svar_for_sporsmal_tag_i_2024[
                'INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_ENDRET_MARKEDSSITUASJON']),
        andre_grunner=str(
            antall_svar_for_sporsmal_tag_i_2024['INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_ANNET']),
        ja_endring_25_prosent=str(
            antall_svar_for_sporsmal_tag_i_2024['INNTEKTSOPPLYSNINGER_VARIG_ENDRING_25_PROSENT_JA']),
        nei_endring_25_prosent=str(
            antall_svar_for_sporsmal_tag_i_2024['INNTEKTSOPPLYSNINGER_VARIG_ENDRING_25_PROSENT_NEI'])
    )

    return Markdown(fortelling_med_data)


if __name__ == '__main__':
    pass
