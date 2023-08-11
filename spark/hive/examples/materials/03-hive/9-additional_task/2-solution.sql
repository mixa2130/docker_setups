--/* Напишите запрос, выбирающий количество посещений от мужчин и от женщин по типам браузера (информацию о браузерах берём из таблицы логов). */

use velkerr;

select hitCount.browser, SUM(men) as c_men, SUM(women) as c_women
from (
    select browser, IF(gender='male', count(1), 0) AS men, IF(gender='female', count(1), 0) AS women
    from logs inner join (select gender, ip from users) as sel_users on logs.ip = sel_users.ip
    group by browser, gender
) as hitCount
group by hitCount.browser;
