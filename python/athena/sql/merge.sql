INSERT INTO inverter_minutely(
	   DeviceID, LoggedDatetime, 
	   AlarmCode, ErrorCode,
	   DC1Voltage, DC2Voltage, DC3Voltage, DC4Voltage,
	   DC1Current, DC2Current, DC3Current, DC4Current,
	   DC1Power, DC2Power, DC3Power, DC4Power,
	   DC1Positive, DC1Negative,
	   InternalTemp, HeatSinkTemp,
	   AC1Voltage, AC2Voltage, AC3Voltage,
	   AC1Current, AC2Current, AC3Current,
	   ACFrequency, ACOutputPower, KWH
)
SELECT DeviceID, LoggedDatetime, 
	   AlarmCode, ErrorCode,
	   DC1Voltage, DC2Voltage, DC3Voltage, DC4Voltage,
	   DC1Current, DC2Current, DC3Current, DC4Current,
	   DC1Power, DC2Power, DC3Power, DC4Power,
	   DC1Positive, DC1Negative,
	   InternalTemp, HeatSinkTemp,
	   AC1Voltage, AC2Voltage, AC3Voltage,
	   AC1Current, AC2Current, AC3Current,
	   ACFrequency, ACOutputPower, KWH
FROM demo_2020_0506.inverter_minutely;