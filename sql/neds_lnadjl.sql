--SQL Name: NEDS_LNADJL.sql
--Update History:
--2018-3-22: initial version by gaozw

select
co_lnadj.co_parent_gid lnbts_id
,substr(co_lnadjl.co_dn, 11) co_dn
--LNADJL parameters
,lnadjl.LNADJL_ECGI_ADJ_ENB_ID adj_enb_id
,lnadjl.LNADJL_ECGI_LCR_ID adj_lcr_id
,lnadjl.LNADJL_F_DL_EARFCN adj_earfcn
,lnadjl.LNADJL_PHY_CELL_ID adj_pci
,lnadjl.LNADJL_TAC adj_tac

from
ctp_common_objects co_lnadj
,ctp_common_objects co_lnadjl
,c_lte_lnadjl lnadjl
 
where
lnadjl.conf_id = 1 and lnadjl.obj_gid = co_lnadjl.co_gid
and co_lnadjl.co_parent_gid = co_lnadj.co_gid
