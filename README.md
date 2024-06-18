# Web Automation 
Dashboard Overview The Web Automation Dashboard is a sophisticated web application designed to automate and manage various web-based tasks. Developed using Python and the Flet framework, this project aims to provide a seamless experience for automating repetitive web actions, with a robust backend supported by ClickHouse for data storage.

Features- Task Automation: Users can configure and schedule tasks for automation.
- Real-Time Monitoring: Live updates and monitoring of task execution.
- Customizable Workflows: Flexibility to create custom automation sequences.
- Performance Analytics: Detailed reports and analytics on task performance.
- User Management: Admin panel for managing user access and roles.

Technologies- Python: The core programming language used for developing the application logic.
- Flet: Employs the Flet framework for building a modern, event-driven user interface.
- ClickHouse: Utilizes ClickHouse for its high-performance analytical database capabilities.
- Docker: Leverages Docker for consistent deployment and scalability.
- Git: Implements Git for source code management and version control.

Challenges- Scalability: Ensuring the application can handle a growing number of tasks and users.
- User Experience: Balancing between advanced features and maintaining an intuitive UI.
- Data Integrity: Guaranteeing the accuracy and consistency of data throughout the application.

Future Enhancements- API Integration: Expanding the application's capabilities by integrating with various APIs.
- Machine Learning: Incorporating machine learning algorithms to optimize task automation.
- Cross-Platform Support: Developing a cross-platform application for wider accessibility.
This project is a testament to the power of modern web technologies in creating efficient and user-friendly applications for task automation. It showcases the potential of Python and Flet in web development, while ClickHouse provides a solid foundation for data management. The use of Docker and Git further enhances the project's deployment and collaborative aspects, making it a robust solution for users and developers alike.


# Database query for this project
```SQL
ALTER TABLE status_request CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
```
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
