--SQL Name: NEDS_M8007.sql
--Update History:
--2018-7-25: initial version by gaozw

select
  lnbts_id
  ,lncel_id
  ,period_start_time
  --drb setup count
  ,DATA_RB_STP_ATT
  ,DATA_RB_STP_COMP
  ,DATA_RB_STP_FAIL

from
  NOKLTE_PS_LRDB_MNC1_RAW

where
  period_start_time >= to_date(&start_time, 'yyyymmddhh24')
  and period_start_time <= to_date(&end_time, 'yyyymmddhh24')