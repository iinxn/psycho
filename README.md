# psycho
# База данных
```SQL
ALTER TABLE status_request CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
```
 Команда для изменения типа символов
## Количество выполненных заявок
```SQL
SELECT COUNT(*) AS `Количество выполненных заказов`
FROM requests
JOIN status_request ON requests.status_id = status_request.status_id
WHERE status_request.name = 'Готово к выдаче';
```
## Среднее вермя выполнения заказа
```SQL
SELECT AVG(DATEDIFF(date_out, date_in)) AS `Средение время выполнения заказа`
FROM requests
JOIN status_request ON requests.status_id = status_request.status_id
WHERE status_request.name = 'Готово к выдаче';
```
## Статистика по типам несиправностей
```SQL
SELECT faults.name AS `Тип неисправности`, COUNT(requests.request_id) AS `Количество заявок`
FROM
    requests
JOIN
    faults ON requests.fault_id = faults.fault_id
GROUP BY
    faults.name;
```
