--SQL Name: NEDS_LNREL.sql
--Update History:
--2018-3-22: initial version by gaozw

select
co_lnrel.co_parent_gid lncel_id
,substr(co_lnrel.co_dn, 11) co_dn
--LNREL parameters
,lnrel.LNREL_ECGI_ADJ_ENB_ID adj_enb_id
,lnrel.LNREL_ECGI_LCR_ID adj_lcr_id
,lnrel.LNREL_CION_3 cio
,lnrel.LNREL_H_N_OVER_AL_L ho_allowed
,lnrel.LNREL_NR_STAT nr_stat

from
ctp_common_objects co_lnrel
,c_lte_lnrel lnrel

where
lnrel.conf_id = 1 and lnrel.obj_gid = co_lnrel.co_gid
