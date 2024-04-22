import os
from google.cloud import bigquery
from typing import Union

from grafer_og_visninger.pie_chart import side_ved_side_pie_chart
from queries.naeringsdrivende_inntekt import naeringsdrivende_inntekt_foer_etter_endring, InntektsSporsmal, \
    question_tags
from rich.markdown import Markdown

def init_bigquery_client():
    credentials_path = os.path.expanduser('~/.config/gcloud/application_default_credentials.json')

    authenticated_locally = os.path.isfile(credentials_path)
    running_in_prod = os.getenv('NAIS_CLUSTER_NAME', '').lower() == 'prod-gcp'

    if authenticated_locally or running_in_prod:  # Check if the file exists
        if authenticated_locally:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

        return bigquery.Client(project='flex-prod-af40')
    else:
        print("Credentials file not found OR not running in prod. Functionality requiring credentials/prod env will "
              "be skipped.")


def get_data_for_tag(tag, data, perioder):
    """Retrieve data for a specific tag across specified periods."""
    return {period: data[period].get(tag, 0) for period in perioder}


# Calculate sums for each period
def aggregate_data(df, periods, tags):
    """Aggregate data by periods and tags."""
    period_data = {}
    for period in periods:
        period_df = df[df['period'] == period]
        sums = {tag: period_df[period_df['sporsmal_tag'] == tag]['count'].sum() for tag in tags}
        period_data[period] = sums
    return period_data


def data_oversikt(bigquery_client):
    # Inntektsmelding næringsdrivende
    naeringsdrivende_inntekt_query = naeringsdrivende_inntekt_foer_etter_endring()
    df = bigquery_client.query(naeringsdrivende_inntekt_query).to_dataframe()

    perioder = ['foer', 'etter']
    periode_data = aggregate_data(df, perioder, question_tags)

    # Generating data for all tags
    return {tag: get_data_for_tag(tag, periode_data, perioder) for tag in question_tags}


def hent_data_om_inntektssporsmal(data_oversikt, periode: Union['foer', 'etter']) -> str:
    fortelling_inntektsopplysninger = """
**Drift i virksomheten:**
- **Ja:** {ja_drift} var antallet næringsdrivende som hadde drift i virksomheten frem til sykmelding.
- **Nei:** {nei_drift} hadde ikke drift i virksomheten.

**Ny i arbeidslivet:**
- **Ja:** {ja_ny} var antallet som svarte at de var ny i arbeidslivet.
- **Nei:** {nei_ny} svarte at de ikke var nye i arbeidslivet.

**Varig endring i inntekten:**
- **Ja:** {ja_varig_endring} var totalt antall som svarte ja på en varig endring i inntekten.
- **Nedleggelse av virksomheten:** {nedleggelse} var antallet som svarte at de hadde lagt ned virksomheten.
- **Endret innsats:** {endret_innsats} svarte at de endret innsats i virksomheten.
- **Omlagt virksomheten:** {omlagt} svarte at de hadde omlagt virksomheten.
- **Endret markedssituasjon:** {endret_marked} svarte at det var endringer i markedssituasjonen.
- **Andre grunner:** {andre_grunner} svarte at det var andre grunner for endring.
- **Endring på minst 25%:** {endring_25_prosent} næringsdrivende rapporterte en endring på minst 25% i sin virksomhet.
"""

    fortelling_med_data = fortelling_inntektsopplysninger.format(
        ja_drift=str(data_oversikt['INNTEKTSOPPLYSNINGER_DRIFT_VIRKSOMHETEN_JA'][periode]),
        nei_drift=str(data_oversikt['INNTEKTSOPPLYSNINGER_DRIFT_VIRKSOMHETEN_NEI'][periode]),
        ja_ny=str(data_oversikt['INNTEKTSOPPLYSNINGER_NY_I_ARBEIDSLIVET_JA'][periode]),
        nei_ny=str(data_oversikt['INNTEKTSOPPLYSNINGER_NY_I_ARBEIDSLIVET_NEI'][periode]),
        ja_varig_endring=str(data_oversikt['INNTEKTSOPPLYSNINGER_VARIG_ENDRING'][periode]),
        nedleggelse=str(
            data_oversikt['INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_OPPRETTELSE_NEDLEGGELSE'][periode]),
        endret_innsats=str(data_oversikt['INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_ENDRET_INNSATS'][periode]),
        omlagt=str(data_oversikt['INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_OMLEGGING_AV_VIRKSOMHETEN'][periode]),
        endret_marked=str(
            data_oversikt['INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_ENDRET_MARKEDSSITUASJON'][periode]),
        andre_grunner=str(data_oversikt['INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_ANNET'][periode]),
        endring_25_prosent=str(data_oversikt['INNTEKTSOPPLYSNINGER_VARIG_ENDRING_25_PROSENT'][periode])
    )

    return Markdown(fortelling_med_data)


def graf_foer_etter_endring(data_oversikt):
    ja_nei_kategorier = ['Ja', 'Nei']
    side_ved_side_pie_chart(ja_nei_kategorier,
                            [
                                data_oversikt[InntektsSporsmal.INNTEKTSOPPLYSNINGER_DRIFT_VIRKSOMHETEN_JA.value][
                                    'foer'],
                                data_oversikt[InntektsSporsmal.INNTEKTSOPPLYSNINGER_DRIFT_VIRKSOMHETEN_NEI.value][
                                    'foer']
                            ],
                            [
                                data_oversikt[InntektsSporsmal.INNTEKTSOPPLYSNINGER_DRIFT_VIRKSOMHETEN_JA.value][
                                    'etter'],
                                data_oversikt[InntektsSporsmal.INNTEKTSOPPLYSNINGER_DRIFT_VIRKSOMHETEN_NEI.value][
                                    'etter']
                            ])
