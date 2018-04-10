--SQL Name: NEDS_M8013.sql
--Update History:
--2018-4-10: initial version by gaozw

select
  lnbts_id
  ,lncel_id
  ,period_start_time
  --msg3/msg5 count
  ,SIGN_CONN_ESTAB_ATT_MO_S
  ,SIGN_CONN_ESTAB_ATT_MT
  ,SIGN_CONN_ESTAB_ATT_MO_D
  ,SIGN_CONN_ESTAB_ATT_EMG
  ,SIGN_CONN_ESTAB_ATT_HIPRIO
  ,SIGN_CONN_ESTAB_ATT_DEL_TOL
  ,SIGN_CONN_ESTAB_COMP

from 
  NOKLTE_PS_LUEST_MNC1_RAW 
  
where 
  period_start_time >= to_date(&start_time, 'yyyymmddhh24') 
  and period_start_time <= to_date(&end_time, 'yyyymmddhh24')
