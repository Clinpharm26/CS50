--SELECT phone_number FROM people WHERE name = "Ernest";

SELECT name FROM people WHERE phone_number IN(SELECT receiver FROM phone_calls WHERE month = 7 AND day = 28 AND duration < 60 AND caller = "(367) 555-5533");
