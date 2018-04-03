--SQL Name: NEDS_LNADJ.sql
--Update History:
--2018-3-22: initial version by gaozw

select
co_lnadj.co_parent_gid lnbts_id
,substr(co_lnadj.co_dn, 11) co_dn
--LNADJ parameters
,lnadj.LNADJ_ADJ_ENB_ID adj_enb_id
,lnadj.LNADJ_C_PLANE_IP_ADDR adj_enb_ip
,lnadj.LNADJ_X_2_LINK_STAT x2_stat

from
ctp_common_objects co_lnadj
,c_lte_lnadj lnadj
 
where
lnadj.conf_id = 1 and lnadj.obj_gid = co_lnadj.co_gid
