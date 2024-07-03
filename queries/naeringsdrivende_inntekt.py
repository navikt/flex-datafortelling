from enum import Enum


class InntektsSporsmal(Enum):
    INNTEKTSOPPLYSNINGER_DRIFT_VIRKSOMHETEN_JA = 'INNTEKTSOPPLYSNINGER_DRIFT_VIRKSOMHETEN_JA'
    INNTEKTSOPPLYSNINGER_DRIFT_VIRKSOMHETEN_NEI = 'INNTEKTSOPPLYSNINGER_DRIFT_VIRKSOMHETEN_NEI'
    INNTEKTSOPPLYSNINGER_NY_I_ARBEIDSLIVET_JA = 'INNTEKTSOPPLYSNINGER_NY_I_ARBEIDSLIVET_JA'
    INNTEKTSOPPLYSNINGER_NY_I_ARBEIDSLIVET_NEI = 'INNTEKTSOPPLYSNINGER_NY_I_ARBEIDSLIVET_NEI'
    INNTEKTSOPPLYSNINGER_VARIG_ENDRING = 'INNTEKTSOPPLYSNINGER_VARIG_ENDRING'
    INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_OPPRETTELSE_NEDLEGGELSE = 'INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_OPPRETTELSE_NEDLEGGELSE'
    INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_ENDRET_INNSATS = 'INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_ENDRET_INNSATS'
    INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_OMLEGGING_AV_VIRKSOMHETEN = 'INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_OMLEGGING_AV_VIRKSOMHETEN'
    INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_ENDRET_MARKEDSSITUASJON = 'INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_ENDRET_MARKEDSSITUASJON'
    INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_ANNET = 'INNTEKTSOPPLYSNINGER_VARIG_ENDRING_BEGRUNNELSE_ANNET'
    INNTEKTSOPPLYSNINGER_VARIG_ENDRING_25_PROSENT = 'INNTEKTSOPPLYSNINGER_VARIG_ENDRING_25_PROSENT'


question_tags = tuple(tag.value for tag in InntektsSporsmal)


def naeringsdrivende_inntekt_foer_etter_endring() -> str:
    bq_tabell = '`flex-prod-af40.flex_dataset.sykepengesoknad_sporsmal_svar_view`'
    # noinspection SqlNoDataSourceInspection
    query = f"""
    WITH filtered_data AS (
        SELECT
            sykepengesoknad_uuid,
            sporsmal_tag,
            verdi,
            sendt,
            CASE
                WHEN sendt < TIMESTAMP '2024-04-05 13:05:00' AND sendt >= TIMESTAMP_SUB(TIMESTAMP '2024-04-05 13:05:00', INTERVAL 30 DAY) THEN 'foer'        
                WHEN sendt >= TIMESTAMP '2024-04-05 13:05:00' AND sendt < TIMESTAMP_ADD(TIMESTAMP '2024-04-05 13:05:00', INTERVAL 30 DAY) THEN 'etter'
                END AS period
        FROM
            {bq_tabell}
        WHERE
            sporsmal_tag IN {question_tags}
        AND sendt BETWEEN TIMESTAMP_SUB(TIMESTAMP '2024-04-05 13:05:00', INTERVAL 30 DAY) AND TIMESTAMP_ADD(TIMESTAMP '2024-04-05 13:05:00', INTERVAL 30 DAY)
        )
    
    SELECT
        sporsmal_tag,
        verdi,
        period,
        COUNT(*) AS count
    FROM
        filtered_data
    WHERE
        period IS NOT NULL
    GROUP BY
        sporsmal_tag,
        verdi,
        period
    ORDER BY
        sporsmal_tag,
        period,
        count DESC;


    """

    return query


def naeringsdrivende_inntekt_i_2024() -> str:
    bq_tabell = '`flex-prod-af40.flex_dataset.sykepengesoknad_sporsmal_svar_view`'
    # noinspection SqlNoDataSourceInspection
    query = f"""
    WITH filtered_data AS (
        SELECT
            sykepengesoknad_uuid,
            sporsmal_tag,
            verdi,
            sendt
        FROM
            {bq_tabell}
        WHERE
            sporsmal_tag IN ({', '.join([f"'{tag}'" for tag in question_tags])}, 'INNTEKTSOPPLYSNINGER_VIRKSOMHETEN_AVVIKLET_NEI', 'INNTEKTSOPPLYSNINGER_VIRKSOMHETEN_AVVIKLET_JA')
            AND sendt BETWEEN '2024-01-01 00:00:00' AND '2024-12-31 23:59:59'
    )
    
    SELECT
        CASE 
            WHEN sporsmal_tag IN ('INNTEKTSOPPLYSNINGER_VIRKSOMHETEN_AVVIKLET_NEI', 'INNTEKTSOPPLYSNINGER_DRIFT_VIRKSOMHETEN_JA') THEN 'INNTEKTSOPPLYSNINGER_VIRKSOMHETEN_AVVIKLET_NEI'
            WHEN sporsmal_tag IN ('INNTEKTSOPPLYSNINGER_VIRKSOMHETEN_AVVIKLET_JA', 'INNTEKTSOPPLYSNINGER_DRIFT_VIRKSOMHETEN_NEI') THEN 'INNTEKTSOPPLYSNINGER_VIRKSOMHETEN_AVVIKLET_JA'
            ELSE sporsmal_tag
        END AS sporsmal_tag,
        verdi,
        COUNT(*) AS count
    FROM
        filtered_data
    GROUP BY
        sporsmal_tag,
        verdi
    ORDER BY
        sporsmal_tag,
        count DESC;
"""
    return query
