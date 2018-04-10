--SQL Name: NEDS_M8051.sql
--Update History:
--2018-4-10: initial version by gaozw

select
  lnbts_id
  ,lncel_id
  ,period_start_time
  --avg/max ue number
  ,RRC_CONNECTED_UE_AVG
  ,RRC_CONNECTED_UE_MAX
  ,CELL_LOAD_ACTIVE_UE_AVG
  ,CELL_LOAD_ACTIVE_UE_MAX

from 
  NOKLTE_PS_LUEQ_MNC1_RAW 
  
where 
  period_start_time >= to_date(&start_time, 'yyyymmddhh24') 
  and period_start_time <= to_date(&end_time, 'yyyymmddhh24')
