--SQL Name: NEDS_M8005.sql
--Update History:
--2018-4-10: initial version by gaozw

select
  lnbts_id
  ,lncel_id
  ,period_start_time
  --avg rssi/sinr of pucch/pusch
  ,RSSI_PUCCH_AVG
  ,RSSI_PUSCH_AVG
  ,SINR_PUCCH_AVG
  ,SINR_PUSCH_AVG

from 
  NOKLTE_PS_LPQUL_MNC1_RAW 
  
where 
  period_start_time >= to_date(&start_time, 'yyyymmddhh24') 
  and period_start_time <= to_date(&end_time, 'yyyymmddhh24')
