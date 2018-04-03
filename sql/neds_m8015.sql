--SQL Name: NEDS_M8015.sql
--Update History:
--2018-3-22: initial version by gaozw

select
  lnbts_id
  ,lncel_id
  ,eci_id
  ,period_start_time
  --intra-enb handover
  ,INTRA_HO_PREP_FAIL_NB
  ,INTRA_HO_ATT_NB
  ,INTRA_HO_SUCC_NB
  ,INTRA_HO_FAIL_NB
  --inter-enb handover
  ,INTER_HO_PREP_FAIL_OTH_NB
  ,INTER_HO_PREP_FAIL_TIME_NB
  ,INTER_HO_PREP_FAIL_AC_NB
  ,INTER_HO_PREP_FAIL_QCI_NB
  ,INTER_HO_ATT_NB
  ,INTER_HO_SUCC_NB
  ,INTER_HO_FAIL_NB
  --mro
  ,MRO_LATE_HO_NB
  ,MRO_EARLY_TYPE1_HO_NB
  ,MRO_EARLY_TYPE2_HO_NB
  ,MRO_PING_PONG_HO_NB
  --load balancing
  ,HO_LB_IF_ATT_NB
  ,HO_LB_IF_SUCC_NB

from 
  NOKLTE_PS_LNCELHO_DMNC1_RAW 
  
where 
  period_start_time >= to_date(&start_time, 'yyyymmddhh24') 
  and period_start_time <= to_date(&end_time, 'yyyymmddhh24')
  --only valid handover prep/att
  and (INTRA_HO_PREP_FAIL_NB + INTRA_HO_ATT_NB + INTER_HO_PREP_FAIL_OTH_NB + INTER_HO_PREP_FAIL_TIME_NB + INTER_HO_PREP_FAIL_AC_NB + INTER_HO_PREP_FAIL_QCI_NB + INTER_HO_ATT_NB) > 0
