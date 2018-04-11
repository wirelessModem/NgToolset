--SQL Name: NEDS_IRFIM.sql
--Update History:
--2018-4-11: initial version by gaozw

select
co_irfim.co_parent_gid lncel_id
,substr(co_irfim.co_dn, 11) co_dn

--irfim parameters
,irfim.IRFIM_DL_CAR_FRQ_EUT if_earfcn
,irfim.IRFIM_ECRP_2 if_res_prio
,irfim.IRFIM_QRLMIF_10 if_rxlev_min
,irfim.IRFIM_INTER_FRQ_THR_L if_th_low
,irfim.IRFIM_INTER_FRQ_THR_H if_th_high 
,irfim.IRFIM_MEAS_BDW if_mbw

from
ctp_common_objects co_irfim
,c_lte_irfim irfim

where
irfim.conf_id = 1 and irfim.obj_gid = co_irfim.co_gid
