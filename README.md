# acm-service-toolkit
Scripts that have been written over the years to help with ACM-related service job

`acm_proceeding_citations.py `: scrapes the proceeding page from ACM Digital Library for all the papers published in that proceeding and its citation.

`post-r2-normalize-scores.py`: generates a normalized score for all the papers in-review and generate the bulk-update file that updates the tag of the submission with the normalized score to HotCRP.  (The score generated here does not affect the final results.)

`research_area_and_pldi_count_query.py`: query the research area and the pldi paper count of a person given their name and ACM profile URL.

`tpms_to_hotcrp.py`: given the paper matching results from TPMS, create a csv that used to update the HotCRP for paper assignment.

`tpms_gen.py`: given the information of paper bidding, create a csv that is accepted by the TPMS system.

`utils.py`, `flatten_rows.py`: random list/csv processing scripts that is helpful. 
