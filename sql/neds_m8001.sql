--SQL Name: NEDS_M8001.sql
--Update History:
--2018-4-10: initial version by gaozw

select
  lnbts_id
  ,lncel_id
  ,period_start_time
  --msg1/msg2 count
  ,RACH_STP_ATT_SMALL_MSG
  ,RACH_STP_ATT_LARGE_MSG
  ,RACH_STP_ATT_DEDICATED
  ,RACH_STP_COMPLETIONS

from 
  NOKLTE_PS_LCELLD_MNC1_RAW 
  
where 
  period_start_time >= to_date(&start_time, 'yyyymmddhh24') 
  and period_start_time <= to_date(&end_time, 'yyyymmddhh24')
