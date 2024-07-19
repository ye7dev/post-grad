# 1075. Project Employees I

Tags: Easy
Date: June 27, 2024

- AC 코드
    
    ```sql
    SELECT p.project_id, IFNULL(round(avg(e.experience_years), 2), 0) AS average_years
    FROM Project p
        LEFT JOIN Employee e
        ON p.employee_id = e.employee_id
    GROUP BY p.project_id;
    ```