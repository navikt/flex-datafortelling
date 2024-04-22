def flexjar_svar_per_dag_query():
    return """

    SELECT
      DATE(`flex-prod-af40.flex_dataset.flexjar_feedback_view`.`opprettet`)
       AS `dag`,
      SUM(CASE WHEN `svar` = 'JA' THEN 1 ELSE 0 END) AS `antall_ja`,
      SUM(CASE WHEN `svar` = 'NEI' THEN 1 ELSE 0 END) AS `antall_nei`,
      SUM(CASE WHEN `svar` = 'FORBEDRING' THEN 1 ELSE 0 END) AS `antall_forbedring`
    FROM
      `flex-prod-af40.flex_dataset.flexjar_feedback_view`
    WHERE
      `flex-prod-af40.flex_dataset.flexjar_feedback_view`.`feedbackId` = 'ditt-sykefravaer-fant-du'
    GROUP BY
      `dag`
    ORDER BY
      `dag` DESC

    """