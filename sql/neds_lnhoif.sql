--SQL Name: NEDS_LNHOIF.sql
--Update History:
--2018-3-22: initial version by gaozw

select
co_lnhoif.co_parent_gid lncel_id
,substr(co_lnhoif.co_dn, 11) co_dn
--LNHOIF parameters
,lnhoif.LNHOIF_ECI_9 if_earfcn

--A3
,lnhoif.LNHOIF_A3ORI_1 if_a3_off
,lnhoif.LNHOIF_HA3ORI_10 if_hys_a3_off
,lnhoif.LNHOIF_A3RIRI_3 if_a3_rep_int
,lnhoif.LNHOIF_A3TRI_5 if_a3_ttt
--A5
,lnhoif.LNHOIF_THLD_3_IFREQ if_a5_th3
,lnhoif.LNHOIF_THLD_3_A_IFREQ if_a5_th3a
,lnhoif.LNHOIF_HT3I_12 if_hys_a5_th3
,lnhoif.LNHOIF_A5RII_7 if_a5_rep_int
,lnhoif.LNHOIF_A_5_TTT_IFREQ if_a5_ttt

,lnhoif.LNHOIF_MBNW_15 if_mbw

from
ctp_common_objects co_lnhoif
,c_lte_lnhoif lnhoif

where
lnhoif.conf_id = 1 and lnhoif.obj_gid = co_lnhoif.co_gid
