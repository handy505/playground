SELECT DeviceID, strftime("%H", LoggedDatetime) AS hour, (MAX(KWH) - MIN(KWH)) AS GenerateKWH
FROM inverter_minutely 
GROUP BY hour, DeviceID;