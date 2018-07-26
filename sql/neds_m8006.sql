--SQL Name: NEDS_M8006.sql
--Update History:
--2018-4-10: initial version by gaozw
--2018-7-25: update by gaozw for jiangxi drb issue monitoring

select
  lnbts_id
  ,lncel_id
  ,period_start_time
  --erab setup
  ,EPS_BEARER_SETUP_ATTEMPTS
  ,EPS_BEARER_SETUP_COMPLETIONS
  ,ERAB_INI_SETUP_FAIL_RNL_RRNA
  ,ERAB_INI_SETUP_FAIL_TNL_TRU
  ,ERAB_INI_SETUP_FAIL_RNL_UEL
  ,ERAB_INI_SETUP_FAIL_RNL_RIP
  ,ERAB_ADD_SETUP_FAIL_RNL_RRNA
  ,ERAB_ADD_SETUP_FAIL_TNL_TRU
  ,ERAB_ADD_SETUP_FAIL_RNL_UEL
  ,ERAB_ADD_SETUP_FAIL_RNL_RIP
  ,ERAB_ADD_SETUP_FAIL_UP
  ,ERAB_ADD_SETUP_FAIL_RNL_MOB
  --erab rel per cause for qci1
  ,ERAB_REL_ENB_QCI1
  ,ERAB_REL_ENB_RNL_INA_QCI1
  ,ERAB_REL_ENB_RNL_UEL_QCI1
  ,ERAB_REL_ENB_TNL_TRU_QCI1
  ,ERAB_REL_ENB_RNL_RED_QCI1
  ,ERAB_REL_ENB_RNL_EUGR_QCI1
  ,ERAB_REL_ENB_RNL_RRNA_QCI1
  ,ERAB_REL_HO_FAIL_TIM_QCI1
  ,ERAB_REL_EPC_PATH_SWITCH_QCI1
  ,ERAB_REL_ENB_TNL_UNSP_QCI1

from 
  NOKLTE_PS_LEPSB_MNC1_RAW
  
where 
  period_start_time >= to_date(&start_time, 'yyyymmddhh24') 
  and period_start_time <= to_date(&end_time, 'yyyymmddhh24')
