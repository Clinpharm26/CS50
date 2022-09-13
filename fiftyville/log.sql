-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Find out what information is available from the crime scene reports table:
SELECT * FROM crime_scene_reports WHERE day = 28 AND month = 7 AND year = 2020 AND street = "Chamberlin Street";
-- id | year | month | day | street | description
--295 | 2020 | 7 | 28 | Chamberlin Street | Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse.
--Interviews were conducted today with three witnesses who were present at the time — each of their interview transcripts mentions the courthouse.

-- Find out what activity took place at the courthouse around the time of the crime:
SELECT * FROM courthouse_security_logs WHERE day = 28 AND month = 7 AND hour = 10;
-- id | year | month | day | hour | minute | activity | license_plate
--258 | 2020 | 7 | 28 | 10 | 8 | entrance | R3G7486
--259 | 2020 | 7 | 28 | 10 | 14 | entrance | 13FNH73
--260 | 2020 | 7 | 28 | 10 | 16 | exit | 5P2BI95
--261 | 2020 | 7 | 28 | 10 | 18 | exit | 94KL13X
--262 | 2020 | 7 | 28 | 10 | 18 | exit | 6P58WS2
--263 | 2020 | 7 | 28 | 10 | 19 | exit | 4328GD8
--264 | 2020 | 7 | 28 | 10 | 20 | exit | G412CB7
--265 | 2020 | 7 | 28 | 10 | 21 | exit | L93JTIZ
--266 | 2020 | 7 | 28 | 10 | 23 | exit | 322W7JE
--267 | 2020 | 7 | 28 | 10 | 23 | exit | 0NTHK55
--268 | 2020 | 7 | 28 | 10 | 35 | exit | 1106N58
--269 | 2020 | 7 | 28 | 10 | 42 | entrance | NRYN856
--270 | 2020 | 7 | 28 | 10 | 44 | entrance | WD5M8I6
--271 | 2020 | 7 | 28 | 10 | 55 | entrance | V47T75I

-- Find out the information provided in the transcripts of the witnesses that were interviewed on the day of the crime:
SELECT * FROM interviews WHERE month = 7 AND day = 28;
-- 161 | Ruth | 2020 | 7 | 28 | Sometime within ten minutes of the theft, I saw the thief get into a car in the courthouse parking lot and drive away.
--If you have security footage from the courthouse parking lot, you might want to look for cars that left the parking lot in that time frame.
--162 | Eugene | 2020 | 7 | 28 | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at the courthouse,
--I was walking by the ATM on Fifer Street and saw the thief there withdrawing some money.
--163 | Raymond | 2020 | 7 | 28 | As the thief was leaving the courthouse, they called someone who talked to them for less than a minute.
--In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
--The thief then asked the person on the other end of the phone to purchase the flight ticket.

-- Find out who left the courthouse within 10 minutes of the crime:
SELECT name FROM people WHERE license_plate IN(SELECT license_plate FROM courthouse_security_logs WHERE month = 7 AND day = 28 AND hour  = 10 AND minute BETWEEN 15 AND 25 AND activity = "exit"
--Patrick
--Amber
--Elizabeth
--Roger
--Danielle
--Russell
--Evelyn
--Ernest*
-- Find out who made withdrawals from the ATM on Fifer Street on the day of the theft:
SELECT name FROM people WHERE id IN(SELECT person_id FROM bank_accounts WHERE account_number IN(SELECT account_number FROM atm_transactions WHERE month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw"));
--Bobby
--Elizabeth
--Victoria
--Madison
--Roy
--Danielle
--Russell
--Ernest*

--Find out who made a phone call on the day of the theft for a duration less than a minute:
SELECT name FROM people WHERE phone_number IN(SELECT caller FROM phone_calls WHERE month = 7 AND day = 28 AND duration < 60);
--Bobby
--Roger
--Victoria
--Madison
--Russell
--Evelyn
--Ernest*
--Kimberly

-- Find out who booked an early morning flight out of Fiftyville for the day after the theft:
SELECT name FROM people WHERE passport_number IN(SELECT passport_number FROM passengers WHERE flight_id IN(SELECT id FROM flights WHERE month = 7 AND day = 29 AND hour < 9 AND origin_airport_id IN(SELECT id FROM airports WHERE city = "Fiftyville")));
--Bobby
--Roger
--Madison
--Danielle
--Evelyn
--Edward
--Ernest*
--Doris

-- Find out who the accomplice is:
SELECT phone_number FROM people WHERE name = "Ernest";
SELECT name FROM people WHERE phone_number IN(SELECT receiver FROM phone_calls WHERE month = 7 AND day = 28 AND duration < 60 AND caller = "(367) 555-5533");
--Berthold


-- Find out which city the thief escaped to:
SELECT city FROM airports WHERE id IN(SELECT destination_airport_id FROM flights WHERE month = 7 AND day = 29 AND hour = 8);
--London
