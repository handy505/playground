SELECT DeviceID, MIN(LoggedDatetime), MAX(LoggedDatetime), (MAX(KWH) - MIN(KWH)) AS GenerateKWH
FROM inverter_minutely 
WHERE LoggedDatetime >= datetime("2020-05-05 05:00:00") and LoggedDatetime < datetime("2020-05-05 05:00:00", "+7 hours")
GROUP BY DeviceID
HAVING (MAX(KWH) - MIN(KWH)) < 100;